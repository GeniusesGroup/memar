"""Reading a Go file: its tokens, its declarations, and the span of each top-level
construct in the lines it occupies.

The lexer is the only scanner here and it reads Khayyam too, so the token and
delimiter helpers belong with it; `lex_source` says which of the two it is reading.
Above the tokens sit the declarations a Go corpus is made of -- interfaces with
their methods and embeddings, types, methods with their receivers, and the imports
a package names -- and the workspace that loads an imported package on demand.
Above those sit the constructs, each with the lines it spans, for a tool that must
quote a Go file back line by line."""

import re
import ast
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence

from failures import (
    BridgeFailure,
    SourceFailure,
)
from comments import (
    CommentIndex,
    extract_comment_blocks,
)


@dataclass(frozen=True)
class Token:
    text: str
    kind: str
    line: int


@dataclass
class Parameter:
    name: str | None
    type_text: str
    variadic: bool = False


@dataclass
class InterfaceEntry:
    name: str
    parameters: list[Parameter]
    results: list[Parameter]
    generic: bool
    line: int
    doc: list[str] = field(default_factory=list)
    type_params: list[str] = field(default_factory=list)
    declaration_line: int = 0


@dataclass
class Composition:
    text: str
    line: int
    doc: list[str] = field(default_factory=list)
    arguments: list[str] = field(default_factory=list)
    constraint: bool = False
    anonymous: bool = False


@dataclass
class GoInterface:
    name: str
    entries: list[InterfaceEntry]
    compositions: list[Composition]
    generic: bool
    path: str
    line: int
    doc: list[str] = field(default_factory=list)
    type_params: list[str] = field(default_factory=list)


@dataclass
class GoType:
    name: str
    kind: str
    underlying: str
    generic: bool
    alias: bool
    path: str
    line: int
    doc: list[str] = field(default_factory=list)
    type_params: list[str] = field(default_factory=list)


@dataclass
class GoMethod:
    owner: str
    name: str
    parameters: list[Parameter]
    results: list[Parameter]
    generic: bool
    path: str
    line: int
    doc: list[str] = field(default_factory=list)
    declaration_line: int = 0
    receiver_arguments: list[str] = field(default_factory=list)


@dataclass
class GoSource:
    path: str
    package: str
    imports: dict[str, str]
    interfaces: list[GoInterface]
    types: list[GoType]
    methods: list[GoMethod]
    comments: list["CommentBlock"] = field(default_factory=list)


@dataclass
class GoModel:
    sources: list[GoSource]
    imports: dict[str, str]
    interfaces: list[GoInterface]
    types: dict[str, GoType]
    methods: dict[str, list[GoMethod]]
    root: Path | None
    module: str | None

    @classmethod
    def from_sources(
        cls,
        sources: list[GoSource],
        root: Path | None = None,
        module: str | None = None,
    ) -> "GoModel":
        imports: dict[str, str] = {}
        interfaces: list[GoInterface] = []
        types: dict[str, GoType] = {}
        methods: dict[str, list[GoMethod]] = {}
        for source in sources:
            imports.update(source.imports)
            interfaces.extend(source.interfaces)
            for declaration in source.types:
                previous = types.get(declaration.name)
                if previous and (previous.kind, previous.underlying) != (
                    declaration.kind,
                    declaration.underlying,
                ):
                    raise SourceFailure(
                        f"{declaration.path}: conflicting declarations for type {declaration.name}"
                    )
                types[declaration.name] = declaration
            for method in source.methods:
                methods.setdefault(method.owner, []).append(method)
        return cls(sources, imports, interfaces, types, methods, root, module)


@dataclass
class ResolvedType:
    text: str
    is_interface: bool
    model: GoModel | None = None
    declaration: GoType | None = None
    promotion_name: str | None = None


@dataclass
class PromotedType:
    name: str
    model: GoModel
    source_name: str
    methods: list[GoMethod] = field(default_factory=list)


NO_SPACE_AFTER = {"(", "[", ".", "*", "&", "<", "..."}
NO_SPACE_BEFORE = {".", ",", ")", "]", ">", "<"}
MULTI_OPERATORS = ("...", "<-", "->", ":=", "<<", ">>", "==", "!=", "<=", ">=", "&&", "||")
TYPE_PREFIXES = {"chan", "map", "func", "interface", "struct"}


def lex_source(source: str, go: bool) -> list[Token]:
    tokens: list[Token] = []
    index = 0
    line = 1
    while index < len(source):
        character = source[index]
        if character == "\n":
            tokens.append(Token("\n", "newline", line))
            line += 1
            index += 1
            continue
        if character in " \t\r\f\v":
            index += 1
            continue
        if source.startswith("//", index):
            end = source.find("\n", index)
            index = len(source) if end < 0 else end
            continue
        if source.startswith("/*", index):
            end = source.find("*/", index + 2)
            if end < 0:
                raise SourceFailure(f"line {line}: unterminated block comment")
            line += source.count("\n", index, end + 2)
            index = end + 2
            continue
        if character == '"' or (go and character == "`"):
            quote = character
            end = index + 1
            while end < len(source):
                if quote == '"' and source[end] == "\\":
                    end += 2
                    continue
                if source[end] == quote:
                    break
                if source[end] == "\n" and quote == '"':
                    raise SourceFailure(f"line {line}: unterminated string")
                end += 1
            if end >= len(source):
                raise SourceFailure(f"line {line}: unterminated string")
            text = source[index + 1 : end]
            if quote == '"':
                try:
                    text = ast.literal_eval('"' + text + '"')
                except (SyntaxError, ValueError):
                    pass
            tokens.append(Token(text, "string", line))
            line += source.count("\n", index, end)
            index = end + 1
            continue
        if go and character == "'":
            end = index + 1
            while end < len(source):
                if source[end] == "\\":
                    end += 2
                    continue
                if source[end] == "'":
                    break
                end += 1
            if end >= len(source):
                raise SourceFailure(f"line {line}: unterminated rune")
            tokens.append(Token(source[index : end + 1], "rune", line))
            index = end + 1
            continue
        if character.isalpha() or character == "_":
            end = index + 1
            while end < len(source) and (source[end].isalnum() or source[end] == "_"):
                end += 1
            tokens.append(Token(source[index:end], "ident", line))
            index = end
            continue
        if character.isdigit():
            end = index + 1
            while end < len(source) and (source[end].isalnum() or source[end] in "._"):
                end += 1
            tokens.append(Token(source[index:end], "number", line))
            index = end
            continue
        operator = next((item for item in MULTI_OPERATORS if source.startswith(item, index)), None)
        if operator is not None:
            tokens.append(Token(operator, "punct", line))
            index += len(operator)
            continue
        tokens.append(Token(character, "punct", line))
        index += 1
    tokens.append(Token("", "eof", line))
    return tokens


def token_text(tokens: Sequence[Token]) -> str:
    if not tokens:
        return ""
    result = ""
    for index, token in enumerate(tokens):
        if index and token.text not in NO_SPACE_BEFORE:
            previous = tokens[index - 1].text
            if previous not in NO_SPACE_AFTER:
                result += " "
        result += token.text
    return result


def split_segments(tokens: Sequence[Token], separators: set[str]) -> list[list[Token]]:
    segments: list[list[Token]] = []
    current: list[Token] = []
    parentheses = 0
    brackets = 0
    braces = 0
    for token in tokens:
        if token.text == "(":
            parentheses += 1
        elif token.text == ")":
            parentheses -= 1
        elif token.text == "[":
            brackets += 1
        elif token.text == "]":
            brackets -= 1
        elif token.text == "{":
            braces += 1
        elif token.text == "}":
            braces -= 1
        if token.text in separators and parentheses == 0 and brackets == 0 and braces == 0:
            if current:
                segments.append(current)
                current = []
            continue
        current.append(token)
    if current:
        segments.append(current)
    return segments


def matching(tokens: Sequence[Token], start: int, opening: str, closing: str) -> int:
    if start >= len(tokens) or tokens[start].text != opening:
        raise SourceFailure("internal delimiter mismatch")
    depth = 0
    for index in range(start, len(tokens)):
        if tokens[index].text == opening:
            depth += 1
        elif tokens[index].text == closing:
            depth -= 1
            if depth == 0:
                return index
    raise SourceFailure("unbalanced delimiter")


def top_level_keyword_positions(tokens: Sequence[Token], keyword: str) -> list[int]:
    positions: list[int] = []
    parentheses = 0
    brackets = 0
    braces = 0
    for index, token in enumerate(tokens):
        if parentheses == 0 and brackets == 0 and braces == 0 and token.text == keyword:
            positions.append(index)
        if token.text == "(":
            parentheses += 1
        elif token.text == ")":
            parentheses -= 1
        elif token.text == "[":
            brackets += 1
        elif token.text == "]":
            brackets -= 1
        elif token.text == "{":
            braces += 1
        elif token.text == "}":
            braces -= 1
    return positions


def top_level_value_names(tokens: Sequence[Token], keyword: str) -> list[str]:
    """Names a top-level `const` or `var` declaration introduces."""
    names: list[str] = []
    for position in top_level_keyword_positions(tokens, keyword):
        start = position + 1
        if start >= len(tokens):
            continue
        if tokens[start].text == "(":
            try:
                end = matching(tokens, start, "(", ")")
            except SourceFailure:
                continue
            segments = split_segments(tokens[start + 1 : end], {"\n", ";"})
        else:
            segments = [list(tokens[start : declaration_end(tokens, start)])]
        for segment in segments:
            cursor = 0
            while cursor < len(segment) and segment[cursor].kind == "ident":
                names.append(segment[cursor].text)
                if cursor + 1 < len(segment) and segment[cursor + 1].text == ",":
                    cursor += 2
                    continue
                break
    return names


def is_type_parameter_bracket(tokens: Sequence[Token], start: int) -> bool:
    if start >= len(tokens) or tokens[start].text != "[":
        return False
    try:
        end = matching(tokens, start, "[", "]")
    except SourceFailure:
        return False
    inner = tokens[start + 1 : end]
    if not inner or inner[0].kind == "number" or inner[0].text in {"...", "]"}:
        return False
    if any(token.text in {"any", "comparable", "~", "|", ","} for token in inner):
        return True
    return len(inner) >= 2 and inner[0].kind == "ident" and inner[1].kind == "ident"


def declaration_end(tokens: Sequence[Token], start: int) -> int:
    parentheses = 0
    brackets = 0
    braces = 0
    for index in range(start, len(tokens)):
        token = tokens[index].text
        if token == "(":
            parentheses += 1
        elif token == ")":
            parentheses -= 1
        elif token == "[":
            brackets += 1
        elif token == "]":
            brackets -= 1
        elif token == "{":
            braces += 1
        elif token == "}":
            braces -= 1
        elif (token in {";", "\n"}) and not (parentheses or brackets or braces):
            return index
    return len(tokens)


def type_name(text: str) -> str:
    value = text.strip()
    while value.startswith("(") and value.endswith(")"):
        value = value[1:-1].strip()
    value = value.lstrip("*")
    value = value.split("[", 1)[0]
    if "." in value:
        value = value.rsplit(".", 1)[1]
    return value


def receiver_type_name(tokens: Sequence[Token]) -> str:
    values = list(tokens)
    while values and values[0].text in {"(", ")"}:
        values.pop(0)
    if values and values[0].text == "*":
        values = values[1:]
    if values and values[0].kind == "ident" and len(values) > 1:
        values = values[1:]
    return type_name(token_text(values))


def is_empty_interface(tokens: Sequence[Token]) -> bool:
    values = [token.text for token in tokens]
    return values == ["any"] or values in (["interface", "{", "}"], ["interface", "{", "\n", "}"])


def has_unmappable_type(tokens: Sequence[Token]) -> str | None:
    text = token_text(tokens)
    if "*" in text:
        return "pointer"
    if "..." in text:
        return "variadic"
    if "map[" in text or re.search(r"\bmap\s*\[", text):
        return "map"
    if re.search(r"\bchan\b", text) or "<-" in text or "->" in text:
        return "channel"
    if "[" in text or "]" in text:
        if re.search(r"\binterface\b", text) and "[" not in text:
            return None
        if text.startswith("[]"):
            return "slice"
        if text.startswith("["):
            return "array"
        return "generic"
    if re.search(r"\bfunc\b", text):
        return "function"
    if text.startswith("~") or "|" in text:
        return "type constraint"
    return None


def parse_parameters(tokens: Sequence[Token], line: int) -> list[Parameter]:
    if not tokens:
        return []
    segments = split_segments(tokens, {","})
    if not segments:
        return []
    parameters: list[Parameter] = []
    pending: list[str] = []
    for segment in segments:
        segment = [token for token in segment if token.text != ";"]
        if not segment:
            continue
        variadic = False
        type_start = 0
        if segment[0].text == "...":
            variadic = True
            type_start = 1
            if len(segment) == 1:
                raise SourceFailure(f"line {line}: variadic parameter has no type")
        explicit_name: str | None = None
        if not variadic and segment[0].kind == "ident":
            if len(segment) == 1:
                pending.append(segment[0].text)
                continue
            if (
                len(segment) > 1
                and segment[0].text not in TYPE_PREFIXES
                and segment[1].text not in {".", "("}
            ):
                explicit_name = segment[0].text
                type_start = 1
        type_tokens = list(segment[type_start:])
        if not type_tokens:
            if pending:
                names = pending
                pending = []
                parameters.extend(Parameter(None, name) for name in names)
                continue
            raise SourceFailure(f"line {line}: parameter has no type")
        if explicit_name is not None:
            names = pending + [explicit_name]
            pending = []
        elif pending:
            names = pending
            pending = []
        else:
            names = [None]
        type_text = token_text(type_tokens)
        for name in names:
            parameters.append(Parameter(name, type_text, variadic))
    for name in pending:
        parameters.append(Parameter(None, name))
    return parameters


def parse_signature(
    tokens: Sequence[Token],
    start: int,
    line: int,
    limit: int | None = None,
) -> tuple[list[Parameter], list[Parameter], int, bool]:
    boundary = len(tokens) if limit is None else limit
    if start >= boundary or tokens[start].text != "(":
        raise SourceFailure(f"line {line}: method parameters are missing")
    end = matching(tokens, start, "(", ")")
    parameters = parse_parameters(tokens[start + 1 : end], line)
    cursor = end + 1
    if cursor < boundary and is_type_parameter_bracket(tokens, cursor):
        type_parameter_end = matching(tokens, cursor, "[", "]")
        cursor = type_parameter_end + 1
        generic = True
    else:
        generic = False
    if cursor < boundary and tokens[cursor].text == "(":
        result_end = matching(tokens, cursor, "(", ")")
        results = parse_parameters(tokens[cursor + 1 : result_end], line)
        cursor = result_end + 1
    elif cursor < boundary:
        results = [Parameter(None, token_text(tokens[cursor:boundary]))]
        cursor = boundary
    else:
        results = []
    return parameters, results, cursor, generic


def type_parameter_names(tokens: Sequence[Token]) -> list[str]:
    """The declared type parameter names of a `[A, B any]` type parameter list."""
    names: list[str] = []
    for segment in split_segments(tokens, {","}):
        segment = [token for token in segment if token.text != ";"]
        if not segment or segment[0].text == "~":
            continue
        if segment[0].kind == "ident":
            names.append(segment[0].text)
    return names


def type_arguments(tokens: Sequence[Token]) -> list[str]:
    """The concrete type arguments of an instantiation `Name[A, B]`."""
    arguments: list[str] = []
    for segment in split_segments(tokens, {","}):
        segment = [token for token in segment if token.text != ";"]
        if not segment:
            continue
        arguments.append("".join(token.text for token in segment))
    return arguments


def parse_interface_entry(
    entry: list[Token],
    comments: CommentIndex | None = None,
) -> InterfaceEntry | str | None:
    if not entry:
        return None
    if entry[0].text == ";":
        return None
    line = entry[0].line
    # A union element such as `~int | string` or `Integer | Float` is a type
    # constraint, not a method: the check must precede the identifier check
    # because `~` scans as punctuation.
    if entry[0].text == "~" or "|" in {token.text for token in entry}:
        return "type constraint"
    if entry[0].kind != "ident":
        return "invalid interface entry"
    if len(entry) > 1 and entry[1].text == "[":
        try:
            end = matching(entry, 1, "[", "]")
        except SourceFailure:
            return "generic interface entry"
        parameters = type_parameter_names(entry[2:end])
        cursor = end + 1
        if cursor < len(entry) and entry[cursor].text == "(":
            arguments, results, _, _ = parse_signature(entry, cursor, line)
            return InterfaceEntry(
                entry[0].text,
                arguments,
                results,
                True,
                line,
                comments.documenting(line) if comments else [],
                parameters,
                line,
            )
        return "generic interface entry"
    if len(entry) > 1 and entry[1].text == "(":
        name = entry[0].text
        parameters, results, _, generic = parse_signature(entry, 1, entry[0].line)
        return InterfaceEntry(
            name,
            parameters,
            results,
            generic,
            entry[0].line,
            comments.documenting(entry[0].line) if comments else [],
            [],
            entry[0].line,
        )
    return None


def parse_composition(entry: Sequence[Token], comments: CommentIndex | None) -> Composition:
    line = entry[0].line
    text = "".join(token.text for token in entry)
    arguments: list[str] = []
    constraint = entry[0].text == "~" or "|" in {token.text for token in entry}
    if len(entry) > 1 and entry[1].text == "[":
        try:
            end = matching(entry, 1, "[", "]")
        except SourceFailure:
            end = 1
        arguments = type_arguments(entry[2:end])
    return Composition(
        text,
        line,
        comments.documenting(line) if comments else [],
        arguments,
        constraint,
        text.startswith("interface") and "{" in text,
    )


def parse_interface_body(
    body: Sequence[Token],
    path: str,
    line: int,
    name: str,
    comments: CommentIndex | None = None,
) -> tuple[list[InterfaceEntry], list[Composition], bool]:
    methods: list[InterfaceEntry] = []
    compositions: list[Composition] = []
    generic = False
    for entry in split_segments(body, {"\n", ";"}):
        parsed = parse_interface_entry(entry, comments)
        if isinstance(parsed, InterfaceEntry):
            methods.append(parsed)
            generic = generic or parsed.generic
            continue
        if parsed in {"generic interface entry", "type constraint"}:
            generic = True
            if entry:
                compositions.append(parse_composition(entry, comments))
            continue
        if parsed is not None:
            raise SourceFailure(f"{path}:{line}: {parsed}")
        if entry:
            compositions.append(parse_composition(entry, comments))
    return methods, compositions, generic


def parse_import_segment(segment: Sequence[Token]) -> tuple[str, str] | None:
    segment = [token for token in segment if token.text not in {";", "\n"}]
    if not segment:
        return None
    if len(segment) == 1 and segment[0].kind == "string":
        path = segment[0].text
        alias = path.rstrip("/").split("/")[-1]
        return alias, path
    if len(segment) >= 2 and segment[0].kind == "ident" and segment[1].kind == "string":
        return segment[0].text, segment[1].text
    return None


def parse_go_source(path: str, source: str) -> GoSource:
    try:
        tokens = lex_source(source, True)
    except SourceFailure as error:
        raise SourceFailure(f"{path}: {error}") from error
    blocks = extract_comment_blocks(source)
    comments = CommentIndex(blocks)
    package = ""
    package_positions = top_level_keyword_positions(tokens, "package")
    if package_positions:
        index = package_positions[0] + 1
        if index < len(tokens) and tokens[index].kind == "ident":
            package = tokens[index].text
    imports: dict[str, str] = {}
    for position in top_level_keyword_positions(tokens, "import"):
        start = position + 1
        if start >= len(tokens):
            continue
        if tokens[start].text == "(":
            end = matching(tokens, start, "(", ")")
            segments = split_segments(tokens[start + 1 : end], {"\n", ";"})
        else:
            end = declaration_end(tokens, start)
            segments = [tokens[start:end]]
        for segment in segments:
            parsed = parse_import_segment(segment)
            if parsed:
                imports[parsed[0]] = parsed[1]
    types: list[GoType] = []
    interfaces: list[GoInterface] = []
    for position in top_level_keyword_positions(tokens, "type"):
        start = position + 1
        if start >= len(tokens):
            continue
        if tokens[start].text == "(":
            end = matching(tokens, start, "(", ")")
            entries = split_segments(tokens[start + 1 : end], {"\n", ";"})
            for entry in entries:
                declaration = parse_go_type_entry(entry, path, comments)
                if declaration:
                    types.append(declaration[0])
                    if declaration[1]:
                        interfaces.append(declaration[1])
            continue
        end = declaration_end(tokens, start)
        entry = tokens[start:end]
        declaration = parse_go_type_entry(entry, path, comments)
        if declaration:
            types.append(declaration[0])
            if declaration[1]:
                interfaces.append(declaration[1])
    methods: list[GoMethod] = []
    for position in top_level_keyword_positions(tokens, "func"):
        start = position + 1
        if start >= len(tokens) or tokens[start].text != "(":
            continue
        receiver_end = matching(tokens, start, "(", ")")
        receiver_tokens = tokens[start + 1 : receiver_end]
        receiver = receiver_type_name(receiver_tokens)
        receiver_arguments: list[str] = []
        for position_in_receiver, token in enumerate(receiver_tokens):
            if token.text != "[":
                continue
            try:
                receiver_end_of_arguments = matching(receiver_tokens, position_in_receiver, "[", "]")
            except SourceFailure:
                break
            receiver_arguments = type_arguments(
                receiver_tokens[position_in_receiver + 1 : receiver_end_of_arguments]
            )
            break
        if receiver_end + 1 >= len(tokens) or tokens[receiver_end + 1].kind != "ident":
            continue
        name_index = receiver_end + 1
        name = tokens[name_index].text
        cursor = name_index + 1
        generic = any(token.text == "[" for token in receiver_tokens)
        if cursor < len(tokens) and is_type_parameter_bracket(tokens, cursor):
            generic = True
            cursor = matching(tokens, cursor, "[", "]") + 1
        if cursor >= len(tokens) or tokens[cursor].text != "(":
            continue
        limit = cursor
        parentheses = 0
        brackets = 0
        braces = 0
        while limit < len(tokens):
            value = tokens[limit].text
            if value == "{" and not (parentheses or brackets or braces):
                break
            if value == "(":
                parentheses += 1
            elif value == ")":
                parentheses -= 1
            elif value == "[":
                brackets += 1
            elif value == "]":
                brackets -= 1
            elif value == "{":
                braces += 1
            elif value == "}":
                braces -= 1
            limit += 1
        try:
            parameters, results, _, _ = parse_signature(tokens, cursor, tokens[name_index].line, limit)
        except SourceFailure:
            continue
        methods.append(
            GoMethod(
                receiver,
                name,
                parameters,
                results,
                generic,
                path,
                tokens[name_index].line,
                comments.documenting(tokens[position].line),
                tokens[position].line,
                receiver_arguments,
            )
        )
    return GoSource(path, package, imports, interfaces, types, methods, blocks)


def parse_go_type_entry(
    entry: Sequence[Token],
    path: str,
    comments: CommentIndex | None = None,
) -> tuple[GoType, GoInterface | None] | None:
    entry = [token for token in entry if token.text != ";"]
    if not entry or entry[0].kind != "ident":
        return None
    name = entry[0].text
    cursor = 1
    generic = False
    type_params: list[str] = []
    if cursor < len(entry) and is_type_parameter_bracket(entry, cursor):
        generic = True
        try:
            end = matching(entry, cursor, "[", "]")
        except SourceFailure:
            return None
        type_params = type_parameter_names(entry[cursor + 1 : end])
        cursor = end + 1
    alias = False
    if cursor < len(entry) and entry[cursor].text == "=":
        alias = True
        cursor += 1
    documentation = comments.documenting(entry[0].line) if comments else []
    if cursor >= len(entry):
        return (
            GoType(
                name, "named", "", generic, alias, path, entry[0].line, documentation, type_params
            ),
            None,
        )
    if entry[cursor].text == "interface" and cursor + 1 < len(entry) and entry[cursor + 1].text == "{":
        end = matching(entry, cursor + 1, "{", "}")
        methods, compositions, body_generic = parse_interface_body(
            entry[cursor + 2 : end], path, entry[0].line, name, comments
        )
        declaration = GoType(
            name,
            "interface",
            "interface {}",
            generic or body_generic,
            alias,
            path,
            entry[0].line,
            documentation,
            type_params,
        )
        interface = GoInterface(
            name,
            methods,
            compositions,
            declaration.generic,
            path,
            entry[0].line,
            documentation,
            type_params,
        )
        return declaration, interface
    if entry[cursor].text == "struct" and cursor + 1 < len(entry) and entry[cursor + 1].text == "{":
        end = matching(entry, cursor + 1, "{", "}")
        underlying = token_text(entry[cursor : end + 1])
        return (
            GoType(
                name, "struct", underlying, generic, alias, path, entry[0].line, documentation, type_params
            ),
            None,
        )
    underlying = token_text(entry[cursor:])
    kind = "named"
    return (
        GoType(
            name, kind, underlying, generic, alias, path, entry[0].line, documentation, type_params
        ),
        None,
    )


def find_module(paths: Sequence[Path]) -> tuple[Path | None, str | None]:
    for path in paths:
        current = path if path.is_dir() else path.parent
        for candidate in (current, *current.parents):
            go_mod = candidate / "go.mod"
            if go_mod.exists():
                try:
                    first = go_mod.read_text(encoding="utf-8").splitlines()
                except OSError:
                    continue
                for line in first:
                    match = re.match(r"\s*module\s+(\S+)", line)
                    if match:
                        return candidate, match.group(1)
    common: Path | None
    if not paths:
        return None, None
    common = paths[0] if paths[0].is_dir() else paths[0].parent
    for path in paths[1:]:
        candidate = path if path.is_dir() else path.parent
        while common != candidate and common not in candidate.parents:
            common = common.parent
    return common, None


def source_paths(values: Sequence[str], suffix: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    for value in values:
        if value == "-":
            result.append(("<stdin>", sys.stdin.read()))
            continue
        path = Path(value)
        if not path.exists():
            raise BridgeFailure([f"input path does not exist: {value}"])
        if path.is_dir():
            files = sorted(
                item
                for item in path.rglob(f"*{suffix}")
                if item.is_file() and not item.name.endswith("_test.go")
            )
            if not files:
                raise BridgeFailure([f"input directory has no {suffix} files: {value}"])
            for item in files:
                result.append((str(item), item.read_text(encoding="utf-8")))
        else:
            result.append((str(path), path.read_text(encoding="utf-8")))
    return result


class GoWorkspace:
    def __init__(self, main_model: GoModel):
        self.main_model = main_model
        self.cache: dict[str, GoModel | None] = {}

    def import_directory(self, import_path: str, source_model: GoModel) -> Path | None:
        candidates: list[Path] = []
        if source_model.root and source_model.module:
            if import_path == source_model.module:
                candidates.append(source_model.root)
            elif import_path.startswith(source_model.module + "/"):
                candidates.append(source_model.root / import_path[len(source_model.module) + 1 :])
        if source_model.root:
            candidates.append(source_model.root / import_path)
        for source in source_model.sources:
            base = Path(source.path).parent
            candidates.append(base / import_path)
        for candidate in candidates:
            if candidate.is_dir():
                return candidate
        return None

    def load_import(self, import_path: str, source_model: GoModel) -> GoModel | None:
        directory = self.import_directory(import_path, source_model)
        if directory is None:
            return None
        key = str(directory.resolve())
        if key in self.cache:
            return self.cache[key]
        files = sorted(
            item for item in directory.glob("*.go") if item.is_file() and not item.name.endswith("_test.go")
        )
        if not files:
            self.cache[key] = None
            return None
        try:
            sources = [parse_go_source(str(item), item.read_text(encoding="utf-8")) for item in files]
            root, module = find_module(files)
            model = GoModel.from_sources(sources, root, module)
        except (OSError, SourceFailure) as error:
            self.cache[key] = None
            return None
        self.cache[key] = model
        return model


def source_model(sources: list[GoSource]) -> GoModel:
    paths = [Path(source.path) for source in sources if source.path != "<stdin>"]
    root, module = find_module(paths)
    return GoModel.from_sources(sources, root, module)


def type_name(text: str) -> str:
    value = text.strip()
    while value.startswith("(") and value.endswith(")"):
        value = value[1:-1].strip()
    value = value.lstrip("*")
    value = value.split("[", 1)[0]
    if "." in value:
        value = value.rsplit(".", 1)[1]
    return value


def receiver_type_name(tokens: Sequence[Token]) -> str:
    values = list(tokens)
    while values and values[0].text in {"(", ")"}:
        values.pop(0)
    if values and values[0].text == "*":
        values = values[1:]
    if values and values[0].kind == "ident" and len(values) > 1:
        values = values[1:]
    return type_name(token_text(values))


def is_empty_interface(tokens: Sequence[Token]) -> bool:
    values = [token.text for token in tokens]
    return values == ["any"] or values in (["interface", "{", "}"], ["interface", "{", "\n", "}"])


def has_unmappable_type(tokens: Sequence[Token]) -> str | None:
    text = token_text(tokens)
    if "*" in text:
        return "pointer"
    if "..." in text:
        return "variadic"
    if "map[" in text or re.search(r"\bmap\s*\[", text):
        return "map"
    if re.search(r"\bchan\b", text) or "<-" in text or "->" in text:
        return "channel"
    if "[" in text or "]" in text:
        if re.search(r"\binterface\b", text) and "[" not in text:
            return None
        if text.startswith("[]"):
            return "slice"
        if text.startswith("["):
            return "array"
        return "generic"
    if re.search(r"\bfunc\b", text):
        return "function"
    if text.startswith("~") or "|" in text:
        return "type constraint"
    return None


@dataclass
class GoValue:
    """One top-level `var` or `const` spec, kept whole for the transfer."""

    keyword: str
    names: list[str]
    type_text: str
    value_text: str
    grouped: bool
    iota: bool
    start: int
    end: int


def parse_go_values(tokens: Sequence[Token]) -> list[GoValue]:
    """Every top-level `var` and `const` spec -- the specs whose names
    `top_level_value_names` lists -- with its type, initial value, and line span."""
    values: list[GoValue] = []
    for keyword in ("const", "var"):
        for position in top_level_keyword_positions(tokens, keyword):
            start = position + 1
            if start >= len(tokens):
                continue
            if tokens[start].text == "(":
                try:
                    end = matching(tokens, start, "(", ")")
                except SourceFailure:
                    continue
                inner = tokens[start + 1 : end]
                segments = split_segments(inner, {"\n", ";"})
                grouped = True
                iota = any(token.text == "iota" for token in inner)
            else:
                segment = list(tokens[start : declaration_end(tokens, start)])
                segments = [segment]
                grouped = False
                iota = any(token.text == "iota" for token in segment)
            for segment in segments:
                names: list[str] = []
                cursor = 0
                while cursor < len(segment) and segment[cursor].kind == "ident":
                    names.append(segment[cursor].text)
                    cursor += 1
                    if cursor < len(segment) and segment[cursor].text == ",":
                        cursor += 1
                        continue
                    break
                if not names:
                    continue
                rest = segment[cursor:]
                equals = next((index for index, token in enumerate(rest) if token.text == "="), None)
                type_tokens = rest if equals is None else rest[:equals]
                value_tokens = [] if equals is None else rest[equals + 1 :]
                values.append(
                    GoValue(
                        keyword,
                        names,
                        token_text(type_tokens),
                        token_text(value_tokens),
                        grouped,
                        iota,
                        segment[0].line,
                        segment[-1].line,
                    )
                )
    return sorted(values, key=lambda value: value.start)


@dataclass
class GoConstruct:
    """A top-level Go construct and the lines it occupies, doc comment first."""

    kind: str
    name: str
    start: int
    head: int
    end: int
    body: int = 0
    value: GoValue | None = None
    declaration: GoType | None = None


def doc_comment_starts(text: str) -> dict[int, int]:
    """The line a doc comment documents -> the first line of that comment."""
    return {
        block.end + 1: block.start for block in extract_comment_blocks(text) if not block.trailing
    }


def go_constructs(text: str, tokens: Sequence[Token], source: GoSource) -> list[GoConstruct]:
    starts = doc_comment_starts(text)
    values = parse_go_values(tokens)
    types = {(declaration.name, declaration.line): declaration for declaration in source.types}
    constructs: list[GoConstruct] = []
    for keyword in ("package", "import", "type", "func", "var", "const"):
        for position in top_level_keyword_positions(tokens, keyword):
            # `var f = func() {...}` puts a `func` at the top level too; a
            # construct opens a line.
            if position and tokens[position - 1].text not in {"\n", ";"}:
                continue
            head = tokens[position].line
            last_index = declaration_end(tokens, position) - 1
            while last_index > position and tokens[last_index].kind == "eof":
                last_index -= 1
            last = tokens[last_index].line
            begin = starts.get(head, head)
            following = tokens[position + 1] if position + 1 < len(tokens) else None
            if keyword in {"package", "import"}:
                constructs.append(
                    GoConstruct(keyword, following.text if following else "", begin, head, last)
                )
                continue
            if keyword == "type":
                if following is not None and following.text == "(":
                    close = matching(tokens, position + 1, "(", ")")
                    for segment in split_segments(tokens[position + 2 : close], {"\n", ";"}):
                        if not segment or segment[0].kind != "ident":
                            continue
                        line = segment[0].line
                        constructs.append(
                            GoConstruct(
                                "type",
                                segment[0].text,
                                starts.get(line, line),
                                line,
                                segment[-1].line,
                                declaration=types.get((segment[0].text, line)),
                            )
                        )
                    continue
                if following is None or following.kind != "ident":
                    continue
                constructs.append(
                    GoConstruct(
                        "type",
                        following.text,
                        begin,
                        head,
                        last,
                        declaration=types.get((following.text, following.line)),
                    )
                )
                continue
            if keyword in {"var", "const"}:
                for value in values:
                    if value.keyword != keyword or not head <= value.start <= last:
                        continue
                    if value.grouped:
                        first = starts.get(value.start, value.start)
                        constructs.append(
                            GoConstruct(
                                keyword, ", ".join(value.names), first, value.start, value.end, value=value
                            )
                        )
                    else:
                        constructs.append(
                            GoConstruct(keyword, ", ".join(value.names), begin, head, last, value=value)
                        )
                continue
            body = 0
            if tokens[last_index].text == "}":
                depth = 0
                for index in range(last_index, position, -1):
                    if tokens[index].text == "}":
                        depth += 1
                    elif tokens[index].text == "{":
                        depth -= 1
                        if depth == 0:
                            body = tokens[index].line
                            break
            name = following.text if following is not None else ""
            kind = "func"
            if following is not None and following.text == "(":
                kind = "method"
                try:
                    close = matching(tokens, position + 1, "(", ")")
                except SourceFailure:
                    close = position + 1
                receiver = receiver_type_name(tokens[position + 2 : close])
                name = f"{receiver}.{tokens[close + 1].text}" if close + 1 < len(tokens) else receiver
            constructs.append(GoConstruct(kind, name, begin, head, last, body=body))
    return sorted(constructs, key=lambda construct: (construct.head, construct.start))


def balanced_end(code_lines: Sequence[str], line: int) -> int:
    """The last line of a construct opening at `line` (1-based), by bracket depth."""
    depth = 0
    for index in range(line - 1, len(code_lines)):
        for character in code_lines[index]:
            if character in "([{":
                depth += 1
            elif character in ")]}":
                depth -= 1
        if depth <= 0:
            return index + 1
    return line
