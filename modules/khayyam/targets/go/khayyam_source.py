"""Reading Khayyam text, and writing the one Khayyam method line every mode shares.

Khayyam is read here at two scales. The token scale parses a file into its
declarations, the way the inverse direction needs to see one. The line scale reads
a file as the source-rewrite rules need to see it: each `tp` and the lines it
spans, the end-of-file Go clue block and where it begins, and a comment's words
without its markers. Also the rule that a Khayyam file is addressed from the
repository root as written, and the list of Khayyam files a pass over a corpus
reads."""

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence

from failures import SourceFailure
from comments import strip_comments
from names import archive_module
from go_source import (
    Token,
    lex_source,
    matching,
    split_segments,
)


@dataclass
class KhayyamParameter:
    name: str
    type_text: str


@dataclass
class KhayyamDeclaration:
    kind: str
    name: str
    path: str
    line: int
    parameters: list[KhayyamParameter] = field(default_factory=list)
    influencing: list[KhayyamParameter] = field(default_factory=list)
    influenced: list[KhayyamParameter] = field(default_factory=list)
    owner: list[KhayyamParameter] = field(default_factory=list)
    composition: list[str] = field(default_factory=list)
    body_present: bool = False
    body_tokens: list[Token] = field(default_factory=list)


KEYWORDS = {"tp", "vr", "in", "cp", "mt", "ab", "sc"}


TP_LINE = re.compile(r"^tp[ \t]+(\S+)[ \t]+(ab|mt|cp|sc|in)\b(.*)$")
GO_MIGRATE_LINE = re.compile(r"^\s*//\s*TODO\(go-migrate\)")


def render_khayyam_method(
    name: str,
    owner: str,
    influencing: Sequence[KhayyamParameter],
    influenced: Sequence[KhayyamParameter],
) -> str:
    first = ", ".join(f"{parameter.name} {parameter.type_text}" for parameter in influencing)
    second = ", ".join(f"{parameter.name} {parameter.type_text}" for parameter in influenced)
    return f"tp {name} mt (self {owner}) ({first}) ({second})"


@dataclass
class KhayyamParser:
    path: str
    tokens: list[Token]
    index: int = 0

    def current(self) -> Token:
        return self.tokens[self.index]

    def take(self) -> Token:
        token = self.current()
        self.index += 1
        return token

    def skip_newlines(self) -> None:
        # A blank line is no declaration and is no fault, wherever it falls. A
        # declaration is ended by the line's break, so a line holding nothing
        # holds none -- the same whether it opens the file, closes it, or sits
        # between two declarations. `docs/khayyam/khayyam.md`, Declaration
        # separator.
        while self.current().kind == "newline":
            self.take()

    def expect(self, text: str) -> Token:
        token = self.current()
        if token.text != text:
            raise SourceFailure(f"{self.path}:{token.line}: expected {text!r}, got {token.text!r}")
        return self.take()

    def name(self) -> Token:
        token = self.current()
        if token.kind != "ident" or token.text in KEYWORDS:
            raise SourceFailure(f"{self.path}:{token.line}: expected a name")
        return self.take()

    def type_reference(self) -> str:
        token = self.name()
        result = token.text
        while self.current().text == ".":
            self.take()
            result += "." + self.name().text
        return result

    def uri(self) -> str:
        """The URI an `in` names. The path of an inclusion is a URI and not a
        value the reader can resolve: what a URI is written as is the resolver's
        and its manifest's business, and a bare name is not one --
        `docs/khayyam/khayyam.md`, The path is a URI. So a name there is refused
        by name, the same answer a type inclusion gives it."""
        token = self.current()
        if token.kind != "string":
            raise SourceFailure(f"{self.path}:{token.line}: import path must be a string")
        return self.take().text

    def block(self) -> list[Token] | None:
        if self.current().text != "{":
            return None
        self.take()
        end = matching(self.tokens, self.index - 1, "{", "}")
        body = self.tokens[self.index : end]
        self.index = end + 1
        return body

    def params(self) -> list[KhayyamParameter]:
        self.expect("(")
        if self.current().text == ")":
            self.take()
            return []
        result: list[KhayyamParameter] = []
        while True:
            name = self.name().text
            type_text = self.type_reference()
            result.append(KhayyamParameter(name, type_text))
            if self.current().text == ",":
                self.take()
                continue
            self.expect(")")
            break
        return result

    def composition(self, body: Sequence[Token]) -> list[str]:
        result: list[str] = []
        for entry in split_segments(body, {"\n", ";"}):
            meaningful = [token for token in entry if token.text not in {"{", "}"}]
            if not meaningful:
                continue
            if len(meaningful) != 1 or meaningful[0].kind != "ident":
                raise SourceFailure(f"{self.path}:{meaningful[0].line}: invalid abstraction composition")
            result.append(meaningful[0].text)
        return result

    def declaration(self) -> KhayyamDeclaration:
        token = self.take()
        if token.text == "vr":
            name = self.name().text
            following = self.current()
            if following.kind == "ident" and following.text == "in":
                # The Variable Inclusion form, `vr {name} in "{path}"`: a
                # file-level variable included from another file, and the path is
                # the URI naming that file rather than a type the name is bound
                # to -- `docs/khayyam/khayyam.md`, Import Mechanism (`in`),
                # Variable Inclusion, and `docs/khayyam/variable.md`, Variable
                # Scope and Visibility. It is read as the inclusion it is, under
                # the name the frontend's own realization gives it (`vr-in` in
                # `modules/khayyam/core/src/sr.ts` and `parse.ts`), which is the
                # name this module's line scale below already gives it too, so
                # one declaration of the language is one declaration here. The
                # URI is the value slot, the way it is for a type inclusion.
                self.take()
                return KhayyamDeclaration(
                    "vr-in", name, self.path, token.line, [], [], [], [], [self.uri()]
                )
            type_text = self.type_reference()
            return KhayyamDeclaration("vr", name, self.path, token.line, [], [], [], [], [type_text])
        if token.text != "tp":
            raise SourceFailure(f"{self.path}:{token.line}: expected tp or vr")
        name = self.name().text
        subtype = self.take()
        if subtype.text == "in":
            return KhayyamDeclaration("in", name, self.path, token.line, [], [], [], [], [self.uri()])
        if subtype.text == "ab":
            body = self.block()
            return KhayyamDeclaration(
                "ab",
                name,
                self.path,
                token.line,
                [],
                [],
                [],
                [],
                self.composition(body or []),
                bool(body is not None),
                body or [],
            )
        if subtype.text == "mt":
            owner = self.params()
            influencing = self.params()
            influenced = self.params()
            body = self.block()
            return KhayyamDeclaration(
                "mt",
                name,
                self.path,
                token.line,
                [],
                influencing,
                influenced,
                owner,
                [],
                body is not None,
                body or [],
            )
        if subtype.text in {"cp", "sc"}:
            body = self.block()
            if body is None:
                raise SourceFailure(f"{self.path}:{token.line}: {subtype.text} requires a block")
            return KhayyamDeclaration(
                subtype.text,
                name,
                self.path,
                token.line,
                [],
                [],
                [],
                [],
                [],
                True,
                body,
            )
        raise SourceFailure(f"{self.path}:{subtype.line}: unsupported subtype {subtype.text!r}")


def body_is_bodyless(body: Sequence[Token]) -> bool:
    """Whether a method's block holds no content, which is the body-less method
    the language has: `tp {name} mt (self {owner}) (...) (...) { }`, admitted for
    an abstraction's contract and for FFI -- `docs/khayyam/method.md`, Body-less
    Methods (FFI and Contracts), and `docs/khayyam/khayyam.md`, Method. A block
    holding something is a method with a body, and no Go interface method has
    one."""
    return not any(
        token.kind not in {"newline", "eof"} and token.text not in {"{", "}"}
        for token in body
    )


def parse_khayyam_source(path: str, source: str) -> list[KhayyamDeclaration]:
    # A byte-order mark is not a character of the program: it is how the bytes
    # announce their encoding, and the grammar has no form for it. It is neither
    # read past nor deleted here -- the reader says what it is, and the owner
    # removes it -- because a mark this folder quietly dropped would be a file it
    # reports as clean and the Khayyam frontend refuses
    # (`modules/khayyam/core/src/scan.ts`, an unexpected character).
    if source.startswith("\ufeff"):
        raise SourceFailure(f"{path}:1: a byte-order mark is not valid Khayyam")
    try:
        tokens = lex_source(source, False)
    except SourceFailure as error:
        raise SourceFailure(f"{path}: {error}") from error
    parser = KhayyamParser(path, tokens)
    declarations: list[KhayyamDeclaration] = []
    parser.skip_newlines()
    while parser.current().kind != "eof":
        declaration = parser.declaration()
        declarations.append(declaration)
        if parser.current().kind == "newline":
            parser.take()
            parser.skip_newlines()
            continue
        if parser.current().text == ";":
            raise SourceFailure(f"{path}:{parser.current().line}: semicolons are not valid Khayyam")
        if parser.current().kind != "eof":
            raise SourceFailure(
                f"{path}:{parser.current().line}: expected a declaration separator, got {parser.current().text!r}"
            )
    return declarations


def khayyam_uri(relative: str) -> str:
    """`modules/a/b.kh` is addressed from the repository root as written,
    `modules/a/b.kh` -- the import address rule,
    `modules/khayyam/rules/import-address/`."""
    return relative


KHAYYAM_TP = re.compile(r"^[ \t]*tp[ \t]+(\S+)[ \t]+(ab|mt|cp|sc|in)\b(.*)$", re.M)
KHAYYAM_VR = re.compile(r"^[ \t]*vr[ \t]+(\S+)[ \t]+(\S+)", re.M)
KHAYYAM_OWNER = re.compile(r"^\s*\(\s*\S+\s+([^\s,()]+)\s*\)")
KHAYYAM_URI = re.compile(r'^\s*"([^"]*)"')
KHAYYAM_INCLUSION = re.compile(r'\bin\s+"([^"]+\.kh)"')


def khayyam_declarations(text: str) -> list[tuple[str, str, str]]:
    """(name, kind, detail) of every declaration in Khayyam `text`: the owner
    of an `mt`, the URI of an `in`."""
    code = strip_comments(text)
    found: list[tuple[str, str, str]] = []
    for match in KHAYYAM_TP.finditer(code):
        name, kind, rest = match.group(1), match.group(2), match.group(3)
        detail = ""
        if kind == "mt":
            owner = KHAYYAM_OWNER.match(rest)
            detail = owner.group(1) if owner else ""
        elif kind == "in":
            uri = KHAYYAM_URI.match(rest)
            detail = uri.group(1) if uri else ""
        found.append((name, kind, detail))
    for match in KHAYYAM_VR.finditer(code):
        found.append((match.group(1), "vr-in" if match.group(2) == "in" else "vr", ""))
    return found


@dataclass
class EndBlock:
    """One end-of-file Go clue block, as indexes into the file's lines."""

    marker: int
    body: int
    close: int
    last: int
    sealed: bool


@dataclass
class KhDecl:
    name: str
    kind: str
    line: int
    end: int
    rest: str
    groups: list[list[tuple[str, str]]] = field(default_factory=list)
    members: list[tuple[str, str]] = field(default_factory=list)
    body: bool = False

    @property
    def owner(self) -> str:
        if self.kind == "mt" and self.groups and self.groups[0]:
            return self.groups[0][0][1]
        return ""

    @property
    def uri(self) -> str:
        match = KHAYYAM_URI.match(self.rest) if self.kind == "in" else None
        return match.group(1) if match else ""

    def group(self, index: int) -> list[tuple[str, str]]:
        return self.groups[index] if index < len(self.groups) else []


def end_blocks(lines: Sequence[str]) -> list[EndBlock]:
    """Every end-of-file Go clue block: a `// TODO(go-migrate):` line directly
    above `/*`, or above a `// --- go-source:` header and its `/*`."""
    blocks: list[EndBlock] = []
    index = 0
    while index + 1 < len(lines):
        following = lines[index + 1].strip()
        sealed = following.startswith("// --- go-source: ")
        if not GO_MIGRATE_LINE.match(lines[index]) or (following != "/*" and not sealed):
            index += 1
            continue
        opening = index + 2 if sealed else index + 1
        if opening >= len(lines) or lines[opening].strip() != "/*":
            index += 1
            continue
        close = opening + 1
        while close < len(lines) and lines[close].strip() != "*/":
            close += 1
        if close >= len(lines):
            break
        last = close
        if sealed and close + 1 < len(lines) and lines[close + 1].startswith("// --- end go-source: "):
            last = close + 1
        blocks.append(EndBlock(index, opening + 1, close, last, sealed))
        index = last + 1
    return blocks


def comment_mask(lines: Sequence[str]) -> list[bool]:
    """True for a line that opens or lies inside a `/* ... */` comment."""
    mask: list[bool] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if inside:
            mask.append(True)
            inside = "*/" not in line
            continue
        if stripped.startswith("/*"):
            mask.append(True)
            inside = "*/" not in stripped[2:]
            continue
        mask.append(False)
    return mask


def split_comment(line: str) -> tuple[str, str | None]:
    """The code of a line and the text of its `//` comment, if it has one."""
    quoted = False
    for index, character in enumerate(line):
        if character == '"':
            quoted = not quoted
        elif not quoted and line.startswith("//", index):
            return line[:index], line[index + 2 :]
    return line, None


def normalize_comment(text: str) -> str:
    value = text.strip()
    while value.startswith("//"):
        value = value[2:].strip()
    return " ".join(value.split())


def paren_groups(text: str) -> tuple[list[str], str]:
    """The leading `( ... )` groups of `text` and what follows them."""
    groups: list[str] = []
    index = 0
    while True:
        while index < len(text) and text[index] in " \t":
            index += 1
        if index >= len(text) or text[index] != "(":
            break
        depth = 0
        close = -1
        for cursor in range(index, len(text)):
            if text[cursor] == "(":
                depth += 1
            elif text[cursor] == ")":
                depth -= 1
                if depth == 0:
                    close = cursor
                    break
        if close < 0:
            break
        groups.append(text[index + 1 : close])
        index = close + 1
    return groups, text[index:]


def khayyam_parameters(group: str) -> list[tuple[str, str]]:
    items: list[str] = []
    depth = 0
    current = ""
    for character in group:
        if character in "([{":
            depth += 1
        elif character in ")]}":
            depth -= 1
        if character == "," and depth == 0:
            items.append(current)
            current = ""
            continue
        current += character
    items.append(current)
    parameters: list[tuple[str, str]] = []
    for item in items:
        parts = item.split()
        if not parts:
            continue
        parameters.append(("", parts[0]) if len(parts) == 1 else (parts[0], " ".join(parts[1:])))
    return parameters


def khayyam_head(lines: Sequence[str]) -> list[KhDecl]:
    """The `tp` declarations of Khayyam lines, each with the lines it spans."""
    mask = comment_mask(lines)
    declarations: list[KhDecl] = []
    index = 0
    while index < len(lines):
        if mask[index]:
            index += 1
            continue
        code, _ = split_comment(lines[index])
        match = TP_LINE.match(code.rstrip())
        if not match:
            index += 1
            continue
        name, kind, rest = match.groups()
        declaration = KhDecl(name, kind, index, index, rest)
        tail = rest
        if kind == "mt":
            groups, tail = paren_groups(rest)
            declaration.groups = [khayyam_parameters(group) for group in groups]
        if "{" in tail:
            declaration.body = True
            depth = 0
            end = len(lines) - 1
            for cursor in range(index, len(lines)):
                text = tail if cursor == index else split_comment(lines[cursor])[0]
                depth += text.count("{") - text.count("}")
                if depth <= 0:
                    end = cursor
                    break
            declaration.end = end
            if kind in {"ab", "cp"}:
                for cursor in range(index + 1, end):
                    parts = split_comment(lines[cursor])[0].split()
                    if parts:
                        declaration.members.append((parts[0], " ".join(parts[1:])))
        declarations.append(declaration)
        index = declaration.end + 1
    return declarations


def khayyam_comment_texts(lines: Sequence[str]) -> set[str]:
    mask = comment_mask(lines)
    texts: set[str] = set()
    for index, line in enumerate(lines):
        if mask[index]:
            text = line.strip()
            if text.startswith("/*"):
                text = text[2:]
            if text.endswith("*/"):
                text = text[:-2]
            texts.add(normalize_comment(text))
            continue
        _, comment = split_comment(line)
        if comment is not None:
            texts.add(normalize_comment(comment))
    return texts


def kh_module(relative: str) -> str:
    parent = relative.rsplit("/", 1)[0] if "/" in relative else ""
    return archive_module(parent)


def tidy_paths(values: Sequence[str], memar_root: Path, excludes: Sequence[str]) -> list[str]:
    found: set[str] = set()
    for value in values or ["modules"]:
        path = (memar_root / value).resolve()
        candidates = [path] if path.is_file() else sorted(path.rglob("*.kh")) if path.is_dir() else []
        for candidate in candidates:
            if candidate.suffix != ".kh" or "node_modules" in candidate.parts:
                continue
            relative = candidate.relative_to(memar_root).as_posix()
            if any(relative.startswith(prefix) for prefix in excludes):
                continue
            found.add(relative)
    return sorted(found)
