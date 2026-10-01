"""`tidy`: four source-rewrite rules of `modules/khayyam/rules/` applied in place to the
ported corpus, in this order:
  commented-generic-bindings  a Go method that names a type parameter of its
                              interface becomes a Khayyam method, the
                              parameter resolved through its binding;
  go-clue-residue             the end-of-file Go clue block loses the license
                              and every declaration the Khayyam side already
                              holds, and goes when nothing else is left;
  result-parameter-names      `result0`, `arg1`, ... take the first letter of
                              their type;
  method-separation           one blank line between method declarations in a
                              file that carries comments.
No Khayyam declaration is deleted, no Go declaration without a Khayyam counterpart
leaves the block, and a second run over the output changes nothing.

`TIDY_EXCLUDES` is the prefix every pass over a corpus leaves alone unless it is told
otherwise."""

import re
import argparse
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence

from failures import SourceFailure
from names import (
    counterpart_tiers,
    field_accessor_options,
    normalize_module,
    pick_counterpart,
    split_field_name,
)
from go_source import (
    InterfaceEntry,
    Token,
    declaration_end,
    is_type_parameter_bracket,
    lex_source,
    matching,
    parse_import_segment,
    parse_interface_entry,
    receiver_type_name,
    split_segments,
    token_text,
    top_level_keyword_positions,
    type_name,
)
from khayyam_source import (
    GO_MIGRATE_LINE,
    KEYWORDS,
    KHAYYAM_URI,
    TP_LINE,
    comment_mask,
    end_blocks,
    kh_module,
    khayyam_comment_texts,
    khayyam_head,
    normalize_comment,
    paren_groups,
    split_comment,
    tidy_paths,
)
from go_source_block import CORPUS_LICENSE_TEXT


# ---------------------------------------------------------------------------
# Tidy: four source-rewrite rules of `modules/khayyam/rules/` applied in place
# to the ported corpus, in this order:
#   commented-generic-bindings  a Go method that names a type parameter of its
#                               interface becomes a Khayyam method, the
#                               parameter resolved through its binding;
#   go-clue-residue             the end-of-file Go clue block loses the license
#                               and every declaration the Khayyam side already
#                               holds, and goes when nothing else is left;
#   result-parameter-names      `result0`, `arg1`, ... take the first letter of
#                               their type;
#   method-separation           one blank line between method declarations in a
#                               file that carries comments.
# No Khayyam declaration is deleted, no Go declaration without a Khayyam
# counterpart leaves the block, and a second run over the output changes
# nothing.
# ---------------------------------------------------------------------------

TIDY_RULES = (
    "commented-generic-bindings",
    "go-clue-residue",
    "result-parameter-names",
    "method-separation",
)
TIDY_EXCLUDES = ("modules/khayyam/",)


SYNTHETIC_PARAMETER = re.compile(r"^(?:result|arg)\d+$")
GO_TYPE_REFERENCE = re.compile(r"^[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?$")
GO_MODULE = "memar"
GO_TOP_LEVEL = ("type", "func", "var", "const")
OPEN_CONSTRAINTS = {"", "any", "comparable", "interface{}"}


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


@dataclass
class GoMember:
    kind: str
    name: str
    first: int
    last: int
    comments: list[str]
    entry: InterfaceEntry | None = None
    names: list[str] = field(default_factory=list)
    generic: bool = False


@dataclass
class GoBlockType:
    name: str
    kind: str
    first: int
    head: int
    last: int
    comments: list[str]
    bindings: list[tuple[str, str]]
    members: list[GoMember]


@dataclass
class GoBlock:
    lines: list[str]
    imports: dict[str, str]
    types: list[GoBlockType]
    license: tuple[int, int] | None
    package: int | None
    import_ranges: list[tuple[int, int]]
    heads: list[int]
    receivers: set[str]


@dataclass
class TidyReport:
    relative: str
    blank_lines: int = 0
    licenses_removed: int = 0
    members_removed: list[str] = field(default_factory=list)
    types_removed: list[str] = field(default_factory=list)
    blocks_removed: int = 0
    blocks_shrunk: int = 0
    methods_realized: list[str] = field(default_factory=list)
    imports_added: list[str] = field(default_factory=list)
    renames: list[str] = field(default_factory=list)
    unresolved: list[dict[str, str]] = field(default_factory=list)
    open_parameters: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    def changed_by(self) -> list[str]:
        rules = []
        if self.methods_realized:
            rules.append("commented-generic-bindings")
        if self.licenses_removed or self.members_removed or self.types_removed or self.blocks_removed:
            rules.append("go-clue-residue")
        if self.renames:
            rules.append("result-parameter-names")
        if self.blank_lines:
            rules.append("method-separation")
        return rules


def has_license(lines: Sequence[str]) -> bool:
    first = next((line.strip() for line in lines if line.strip()), "")
    return first.startswith("/*") and "license" in first.lower()


def go_bindings(tokens: Sequence[Token]) -> list[tuple[str, str]]:
    """(name, constraint) of every type parameter a `[...]` list declares."""
    bindings: list[tuple[str, str]] = []
    pending: list[str] = []
    for segment in split_segments(tokens, {","}):
        segment = [token for token in segment if token.text not in {";", "\n"}]
        if not segment:
            continue
        if len(segment) == 1 and segment[0].kind == "ident":
            pending.append(segment[0].text)
            continue
        constraint = token_text(segment[1:]).replace(" [", "[")
        for name in [*pending, segment[0].text]:
            bindings.append((name, constraint))
        pending = []
    for name in pending:
        bindings.append((name, ""))
    return bindings


def go_doc_lines(lines: Sequence[str], line: int, floor: int) -> list[int]:
    """The `//` lines directly above `line`, down to but excluding `floor`."""
    doc: list[int] = []
    cursor = line - 1
    while cursor > floor and lines[cursor].strip().startswith("//"):
        doc.insert(0, cursor)
        cursor -= 1
    return doc


def inline_block_comments(line: str) -> list[str]:
    return [normalize_comment(text) for text in re.findall(r"/\*(.*?)\*/", line)]


def line_starts(tokens: Sequence[Token], keyword: str) -> list[int]:
    return [
        position
        for position in top_level_keyword_positions(tokens, keyword)
        if position == 0 or tokens[position - 1].text in {"\n", ";"}
    ]


def parse_go_block(lines: Sequence[str]) -> GoBlock:
    """Parse the Go text a clue block carries; `* /` is read as `*/`."""
    restored = [line.replace("* /", "*/") for line in lines]
    tokens = lex_source("\n".join(restored), True)
    package_positions = line_starts(tokens, "package")
    package = tokens[package_positions[0]].line - 1 if package_positions else None
    license: tuple[int, int] | None = None
    first = next((index for index, line in enumerate(restored) if line.strip()), None)
    if (
        first is not None
        and restored[first].strip().startswith("/*")
        and CORPUS_LICENSE_TEXT.lower() in restored[first].lower()
        and (package is None or first < package)
    ):
        close = first
        while close < len(restored) and "*/" not in restored[close][2 if close == first else 0 :]:
            close += 1
        license = (first, min(close, len(restored) - 1))
    imports: dict[str, str] = {}
    import_ranges: list[tuple[int, int]] = []
    for position in line_starts(tokens, "import"):
        start = position + 1
        if start < len(tokens) and tokens[start].text == "(":
            end = matching(tokens, start, "(", ")")
            segments = split_segments(tokens[start + 1 : end], {"\n", ";"})
            last = tokens[end].line
        else:
            end = declaration_end(tokens, start)
            segments = [list(tokens[start:end])]
            last = tokens[max(end - 1, start)].line
        import_ranges.append((tokens[position].line - 1, last - 1))
        for segment in segments:
            parsed = parse_import_segment(segment)
            if parsed:
                imports[parsed[0]] = parsed[1]
    heads = sorted(tokens[position].line - 1 for keyword in GO_TOP_LEVEL for position in line_starts(tokens, keyword))
    receivers: set[str] = set()
    for position in line_starts(tokens, "func"):
        if position + 1 < len(tokens) and tokens[position + 1].text == "(":
            try:
                close = matching(tokens, position + 1, "(", ")")
            except SourceFailure:
                continue
            receivers.add(receiver_type_name(tokens[position + 2 : close]))
    types: list[GoBlockType] = []
    for position in line_starts(tokens, "type"):
        declared = parse_go_block_type(tokens, position, restored)
        if declared is not None:
            types.append(declared)
    return GoBlock(list(lines), imports, types, license, package, import_ranges, heads, receivers)


def parse_go_block_type(tokens: Sequence[Token], position: int, lines: Sequence[str]) -> GoBlockType | None:
    head = tokens[position].line - 1
    doc = go_doc_lines(lines, head, -1)
    first = doc[0] if doc else head
    comments = [normalize_comment(lines[index]) for index in doc]
    following = tokens[position + 1] if position + 1 < len(tokens) else None
    if following is None or following.kind != "ident":
        end = declaration_end(tokens, position + 1)
        last = tokens[max(end - 1, position)].line - 1
        return GoBlockType("", "grouped", first, head, last, comments, [], [])
    cursor = position + 2
    bindings: list[tuple[str, str]] = []
    if is_type_parameter_bracket(tokens, cursor):
        close = matching(tokens, cursor, "[", "]")
        bindings = go_bindings(tokens[cursor + 1 : close])
        cursor = close + 1
    kind = tokens[cursor].text if cursor < len(tokens) else ""
    if kind not in {"interface", "struct"} or cursor + 1 >= len(tokens) or tokens[cursor + 1].text != "{":
        end = declaration_end(tokens, position)
        last = tokens[max(end - 1, position)].line - 1
        return GoBlockType(following.text, "other", first, head, last, comments, bindings, [])
    opening = cursor + 1
    closing = matching(tokens, opening, "{", "}")
    open_line = tokens[opening].line - 1
    last = tokens[closing].line - 1
    members: list[GoMember] = []
    claimed: set[int] = set()
    for segment in split_segments(tokens[opening + 1 : closing], {"\n", ";"}):
        segment = [token for token in segment if token.text != ";"]
        if not segment:
            continue
        start = segment[0].line - 1
        end_line = segment[-1].line - 1
        doc_lines = go_doc_lines(lines, start, open_line)
        claimed.update(doc_lines)
        claimed.update(range(start, end_line + 1))
        member_comments = [normalize_comment(lines[index]) for index in doc_lines]
        trailing = split_comment(lines[end_line])[1]
        if trailing is not None:
            member_comments.append(normalize_comment(trailing))
        member_first = doc_lines[0] if doc_lines else start
        if kind == "interface":
            try:
                parsed = parse_interface_entry(list(segment))
            except SourceFailure:
                parsed = "invalid interface entry"
            if isinstance(parsed, InterfaceEntry):
                members.append(
                    GoMember("method", parsed.name, member_first, end_line, member_comments, entry=parsed)
                )
                continue
            text = token_text(segment)
            members.append(
                GoMember(
                    "composition",
                    type_name(text),
                    member_first,
                    end_line,
                    member_comments,
                    generic=parsed is not None or "[" in text,
                )
            )
            continue
        values = [token for token in segment if token.kind != "string"]
        texts = [token.text for token in values]
        embedded = (
            (len(values) == 1 and values[0].kind == "ident")
            or (texts[:1] == ["*"] and len(values) in {2, 4})
            or (len(values) == 3 and texts[1] == ".")
        )
        if embedded:
            members.append(
                GoMember("embedded", type_name(token_text(values)), member_first, end_line, member_comments)
            )
            continue
        names: list[str] = []
        index = 0
        while index < len(values) and values[index].kind == "ident":
            names.append(values[index].text)
            if index + 1 < len(values) and values[index + 1].text == ",":
                index += 2
                continue
            break
        members.append(
            GoMember("field", ", ".join(names), member_first, end_line, member_comments, names=names)
        )
    for index in range(head, last + 1):
        text = lines[index]
        if index in claimed and index not in {head, open_line, last}:
            continue
        stripped = text.strip()
        if stripped.startswith("//"):
            if index not in claimed:
                comments.append(normalize_comment(stripped))
            continue
        if index in {head, open_line, last}:
            comments.extend(inline_block_comments(text))
            trailing = split_comment(text)[1]
            if trailing is not None:
                comments.append(normalize_comment(trailing))
    return GoBlockType(following.text, kind, first, head, last, comments, bindings, members)


def kh_method_for(declarations: Sequence[KhDecl], owner: str, entry: InterfaceEntry) -> KhDecl | None:
    """The Khayyam method on `owner` that is the Go method `entry`: the same
    operation, bare, behind its owner's name, or -- on a field abstraction --
    spelled by `field_accessor_options`, with as many parameters and results."""
    for declaration in declarations:
        if declaration.kind != "mt" or declaration.owner != owner:
            continue
        names = {entry.name, f"{owner}_{entry.name}"}
        names.update(field_accessor_options(owner, entry.name, [text for _, text in declaration.group(2)]))
        if declaration.name not in names:
            continue
        if len(declaration.group(1)) == len(entry.parameters) and len(declaration.group(2)) == len(entry.results):
            return declaration
    return None


def go_member_module(member: GoMember, block: GoBlock, module: str, text: str) -> str:
    alias = text.split(".", 1)[0] if "." in text else ""
    path = block.imports.get(alias, "")
    if path.startswith(GO_MODULE + "/"):
        return normalize_module(path[len(GO_MODULE) + 1 :])
    return module


def member_represented(
    member: GoMember,
    counterpart: KhDecl,
    declarations: Sequence[KhDecl],
    block: GoBlock,
    module: str,
) -> bool:
    if member.kind == "method" and member.entry is not None:
        return counterpart.kind == "ab" and kh_method_for(declarations, counterpart.name, member.entry) is not None
    if member.kind == "field":
        fields = {name[:1].lower() + name[1:] for name, type_text in counterpart.members if type_text}
        return counterpart.kind == "cp" and all(name[:1].lower() + name[1:] in fields for name in member.names)
    if member.generic:
        return False
    entries = [name for name, type_text in counterpart.members if not type_text]
    source = block.lines[member.first : member.last + 1]
    text = next((line.strip() for line in source if not line.strip().startswith("//")), member.name)
    home = go_member_module(member, block, module, text.lstrip("*"))
    return any(counterpart_tiers(member.name, entries, home))


def delete_lines(lines: Sequence[str], deletions: set[int]) -> list[str]:
    """`lines` without `deletions`; a blank line a deletion left beside the
    edge of a body, or beside another blank line, goes with it."""
    kept = [(index, line) for index, line in enumerate(lines) if index not in deletions]
    result: list[str] = []
    for position, (index, line) in enumerate(kept):
        touched = (index - 1) in deletions or (index + 1) in deletions
        if touched and not line.strip():
            previous = result[-1] if result else None
            following = next((text for _, text in kept[position + 1 :]), None)
            if (
                previous is None
                or not previous.strip()
                or previous.rstrip().endswith(("{", "("))
                or following is None
                or following.strip().startswith(("}", ")"))
            ):
                continue
        result.append(line)
    return result


def shrink_go_lines(
    go_lines: Sequence[str],
    head: Sequence[str],
    relative: str,
    report: TidyReport | None = None,
) -> list[str] | None:
    """The go-clue-residue rule over one block's Go lines: the lines that stay,
    or None when nothing but the package clause, the imports, and comments the
    Khayyam file already carries would be left."""
    block = parse_go_block(go_lines)
    declarations = khayyam_head(head)
    carried = khayyam_comment_texts(head) | {""}
    module = kh_module(relative)
    deletions: set[int] = set()
    removed_members: list[str] = []
    removed_types: list[str] = []
    licenses = 0
    if block.license is not None and has_license(head):
        deletions.update(range(block.license[0], block.license[1] + 1))
        licenses = 1
    kinds = {"interface": "ab", "struct": "cp"}
    for declared in block.types:
        if declared.kind not in kinds:
            continue
        candidates = [item.name for item in declarations if item.kind == kinds[declared.kind]]
        name, _ = pick_counterpart(declared.name, candidates, module)
        counterpart = next((item for item in declarations if item.name == name and item.kind == kinds[declared.kind]), None)
        if counterpart is None:
            continue
        eligible = [
            member
            for member in declared.members
            if member_represented(member, counterpart, declarations, block, module)
            and all(text in carried for text in member.comments)
        ]
        whole = (
            len(eligible) == len(declared.members)
            and all(text in carried for text in declared.comments)
            and not (declared.kind == "struct" and declared.name in block.receivers)
        )
        if whole:
            deletions.update(range(declared.first, declared.last + 1))
            removed_types.append(f"{declared.name} -> {counterpart.name}")
            removed_members.extend(f"{declared.name}.{member.name}" for member in declared.members)
            continue
        for member in eligible:
            deletions.update(range(member.first, member.last + 1))
            removed_members.append(f"{declared.name}.{member.name}")
    remaining = delete_lines(go_lines, deletions) if deletions else list(go_lines)
    kept = parse_go_block(remaining)
    structural: set[int] = set()
    if kept.package is not None:
        structural.add(kept.package)
    for start, end in kept.import_ranges:
        structural.update(range(start, end + 1))
    residue = [
        line.strip()
        for index, line in enumerate(kept.lines)
        if line.strip() and index not in structural
    ]
    gone = not kept.heads and all(
        line.startswith("//") and normalize_comment(line) in carried for line in residue
    )
    if report is not None:
        report.licenses_removed += licenses
        report.members_removed.extend(removed_members)
        report.types_removed.extend(removed_types)
    if gone:
        return None
    while remaining and not remaining[0].strip():
        remaining.pop(0)
    return remaining


def resolve_go_reference(
    reference: str,
    imports: dict[str, str],
    relative: str,
    memar_root: Path,
) -> tuple[tuple[str, str] | None, str]:
    """((Khayyam name, repository-relative file), "") for a Go type reference
    `pkg.Name` or `Name`, found among the abstractions of the module the
    reference names; (None, why) when there is not exactly one."""
    if "." in reference:
        alias, identifier = reference.split(".", 1)
        path = imports.get(alias)
        if path is None:
            return None, f"the block imports no package `{alias}`"
        if not path.startswith(GO_MODULE + "/"):
            return None, f"`{path}` is outside the `{GO_MODULE}` module"
        module = normalize_module(path[len(GO_MODULE) + 1 :])
    else:
        identifier = reference
        module = kh_module(relative)
    if not identifier[:1].isupper():
        return None, f"`{identifier}` is a Go predeclared or unexported type"
    directory = memar_root / "modules" / module
    homes: dict[str, list[str]] = {}
    for path in sorted(directory.glob("*.kh")) if directory.is_dir() else []:
        lines = path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n").split("\n")
        blocks = end_blocks(lines)
        head = lines[: blocks[0].marker] if blocks else lines
        for declaration in khayyam_head(head):
            if declaration.kind == "ab":
                homes.setdefault(declaration.name, []).append(path.relative_to(memar_root).as_posix())
    for tier in counterpart_tiers(identifier, homes, module):
        unique = sorted(set(tier))
        if len(unique) == 1:
            files = homes[unique[0]]
            if len(files) == 1:
                return (unique[0], files[0]), ""
            return None, f"`{unique[0]}` is declared in more than one file: " + ", ".join(files)
        if unique:
            return None, "more than one abstraction stands for it: " + ", ".join(unique)
    return None, f"no abstraction in `modules/{module}` stands for `{identifier}`"


def type_word(type_text: str) -> str:
    """The word a type is named by: the last segment of a qualified name, so
    `Timer_Status` is `Status` and `Time` is `Time`."""
    base = type_text.strip().lstrip("*[]&.").rsplit(".", 1)[-1]
    segments = [segment for segment in base.split("_") if segment[:1].isalpha()]
    return segments[-1] if segments else ""


def synthetic_name(type_text: str, taken: set[str]) -> str | None:
    """A parameter name from the first letter of its type; the first two
    letters when that is taken, then those two with a numeric suffix."""
    word = type_word(type_text)
    if not word:
        return None
    candidates = [word[0].lower()]
    if len(word) >= 2:
        candidates.append(word[:2].lower())
    for candidate in candidates:
        if candidate not in taken and candidate not in KEYWORDS:
            return candidate
    stem = candidates[-1]
    number = 1
    while f"{stem}{number}" in taken or f"{stem}{number}" in KEYWORDS:
        number += 1
    return f"{stem}{number}"


def add_import(head: list[str], name: str, uri: str) -> list[str]:
    declarations = khayyam_head(head)
    imports = [declaration for declaration in declarations if declaration.kind == "in"]
    line = f'tp {name} in "{uri}"'
    if imports:
        names = [declaration.name for declaration in imports]
        position = imports[-1].end + 1
        if names == sorted(names):
            later = next((declaration for declaration in imports if declaration.name > name), None)
            if later is not None:
                position = later.line
        return [*head[:position], line, *head[position:]]
    mask = comment_mask(head)
    position = 0
    while position < len(head) and mask[position]:
        position += 1
    if position < len(head) and not head[position].strip():
        position += 1
    return [*head[:position], line, "", *head[position:]]


def realize_generic_methods(
    head: list[str],
    blocks: Sequence[GoBlock],
    relative: str,
    memar_root: Path,
    report: TidyReport,
) -> list[str]:
    """The commented-generic-bindings rule: a Go interface method that names a
    type parameter becomes a Khayyam method on the interface's abstraction."""
    module = kh_module(relative)
    for block in blocks:
        for declared in block.types:
            if declared.kind != "interface" or not declared.bindings:
                continue
            bound = dict(declared.bindings)
            users = [
                member
                for member in declared.members
                if member.entry is not None
                and any(
                    re.search(rf"\b{re.escape(name)}\b", parameter.type_text)
                    for name in bound
                    for parameter in [*member.entry.parameters, *member.entry.results]
                )
            ]
            if not users:
                continue
            declarations = khayyam_head(head)
            owner, why = pick_counterpart(
                declared.name, [item.name for item in declarations if item.kind == "ab"], module
            )
            for member in users:
                entry = member.entry
                assert entry is not None
                used = sorted(
                    {
                        name
                        for name in bound
                        for parameter in [*entry.parameters, *entry.results]
                        if re.search(rf"\b{re.escape(name)}\b", parameter.type_text)
                    }
                )
                binding = ", ".join(f"{name} {bound[name]}".strip() for name in used)

                def unresolved(reason: str) -> None:
                    report.unresolved.append(
                        {"file": relative, "interface": declared.name, "method": entry.name, "binding": binding, "reason": reason}
                    )

                if all(bound[name] in OPEN_CONSTRAINTS for name in used):
                    report.open_parameters.append(f"{declared.name}.{entry.name} ({binding})")
                    continue
                if owner is None:
                    unresolved(f"the interface {declared.name}: {why}")
                    continue
                declarations = khayyam_head(head)
                if kh_method_for(declarations, owner, entry) is not None:
                    continue
                resolved: list[tuple[str, str, str]] = []
                failure = ""
                for parameter in [*entry.parameters, *entry.results]:
                    text = parameter.type_text
                    if parameter.variadic:
                        failure = f"`...{text}` is variadic"
                        break
                    if text in bound:
                        reference = bound[text]
                        if reference in OPEN_CONSTRAINTS:
                            failure = f"the type parameter `{text}` is open (`{reference or 'no constraint'}`) and fixes no type"
                            break
                        if not GO_TYPE_REFERENCE.match(reference):
                            failure = f"the binding `{text} {reference}` is not a single type"
                            break
                    elif any(re.search(rf"\b{re.escape(name)}\b", text) for name in bound):
                        failure = f"`{text}` uses a type parameter inside another type"
                        break
                    elif GO_TYPE_REFERENCE.match(text):
                        reference = text
                    else:
                        failure = f"`{text}` has no Khayyam form here"
                        break
                    found, reason = resolve_go_reference(reference, block.imports, relative, memar_root)
                    if found is None:
                        failure = f"`{reference}`: {reason}"
                        break
                    resolved.append((parameter.name or "", found[0], found[1]))
                if failure:
                    unresolved(failure)
                    continue
                local = {item.name: item for item in declarations if item.kind != "in"}
                imported = {item.name: item.uri for item in declarations if item.kind == "in"}
                conflict = ""
                for _, name, uri in resolved:
                    if uri == relative:
                        continue
                    if name in local:
                        conflict = f"`{name}` from {uri} is declared in this file too"
                    elif name in imported and imported[name] != uri:
                        conflict = f"`{name}` is already included from {imported[name]}"
                if conflict:
                    unresolved(conflict)
                    continue
                methods = [item for item in declarations if item.kind == "mt" and item.owner == owner]
                prefixed = (
                    split_field_name(owner) is None
                    and bool(methods)
                    and all(item.name.startswith(owner + "_") for item in methods)
                )
                method_name = f"{owner}_{entry.name}" if prefixed else entry.name
                if any(item.name == method_name for item in declarations):
                    unresolved(f"the name `{method_name}` is already declared in this file")
                    continue
                receiver = next((item.group(0)[0][0] for item in methods if item.group(0) and item.group(0)[0][0]), "self")
                taken = {receiver} | {name for name, _, _ in resolved if name}
                rendered: list[str] = []
                for name, type_text, _ in resolved:
                    if not name or SYNTHETIC_PARAMETER.match(name):
                        name = synthetic_name(type_text, taken) or "v"
                    taken.add(name)
                    rendered.append(f"{name} {type_text}")
                count = len(entry.parameters)
                line = f"tp {method_name} mt ({receiver} {owner}) ({', '.join(rendered[:count])}) ({', '.join(rendered[count:])})"
                doc = [
                    block.lines[index].replace("* /", "*/").strip()
                    for index in range(member.first, member_line(block, member))
                ]
                anchor = max(item.end for item in methods) if methods else next(item.end for item in declarations if item.name == owner and item.kind == "ab")
                head = [*head[: anchor + 1], *doc, line, *head[anchor + 1 :]]
                report.methods_realized.append(f"{owner}.{method_name} ({binding})")
                for _, name, uri in resolved:
                    if uri == relative or name in imported:
                        continue
                    head = add_import(head, name, uri)
                    imported[name] = uri
                    report.imports_added.append(f"{name} {uri}")
    return head


def member_line(block: GoBlock, member: GoMember) -> int:
    """The line of a member's own declaration, below its doc comment."""
    index = member.first
    while index < member.last and block.lines[index].strip().startswith("//"):
        index += 1
    return index


def rename_synthetic_parameters(head: list[str], report: TidyReport) -> list[str]:
    """The result-parameter-names rule over every method declaration."""
    result = list(head)
    for declaration in khayyam_head(head):
        if declaration.kind != "mt":
            continue
        synthetic = [
            name
            for group in declaration.groups[1:3]
            for name, _ in group
            if SYNTHETIC_PARAMETER.match(name)
        ]
        if not synthetic:
            continue
        if declaration.body:
            report.skipped.append(f"{declaration.name}: a method with a body keeps {', '.join(synthetic)}")
            continue
        taken = {name for group in declaration.groups for name, _ in group if name and not SYNTHETIC_PARAMETER.match(name)}
        renames: dict[str, str] = {}
        for group in declaration.groups[1:3]:
            for name, type_text in group:
                if not SYNTHETIC_PARAMETER.match(name):
                    continue
                chosen = synthetic_name(type_text, taken)
                if chosen is None:
                    report.skipped.append(f"{declaration.name}: {name} {type_text} has no letter to take")
                    continue
                taken.add(chosen)
                renames[name] = chosen
        line = result[declaration.line]
        code, comment = split_comment(line)
        match = TP_LINE.match(code.rstrip())
        if not match or not renames:
            continue
        start = match.start(3)
        _, tail = paren_groups(match.group(3))
        span_end = len(code.rstrip()) - len(tail)
        span = code[start:span_end]
        for old, new in renames.items():
            span = re.sub(rf"(?<![\w]){re.escape(old)}(?=\s)", new, span)
            report.renames.append(f"{declaration.name}: {old} -> {new}")
        rebuilt = code[:start] + span + code[span_end:]
        result[declaration.line] = rebuilt + (f"//{comment}" if comment is not None else "")
    return result


def has_textual_comments(head: Sequence[str]) -> bool:
    mask = comment_mask(head)
    leading = 0
    while leading < len(head) and mask[leading]:
        leading += 1
    for index, line in enumerate(head):
        if index < leading or GO_MIGRATE_LINE.match(line):
            continue
        if mask[index] or split_comment(line)[1] is not None:
            return True
    return False


def separate_methods(head: list[str], report: TidyReport) -> list[str]:
    """The method-separation rule: one blank line between two method
    declarations, each taken with the comment lines directly above it."""
    if not has_textual_comments(head):
        return head
    declarations = khayyam_head(head)
    insertions: list[int] = []
    for previous, current in zip(declarations, declarations[1:]):
        if previous.kind != "mt" or current.kind != "mt":
            continue
        start = current.line
        while start - 1 > previous.end and head[start - 1].strip().startswith("//"):
            start -= 1
        if start - 1 == previous.end:
            insertions.append(start)
    result = list(head)
    for position in reversed(insertions):
        result.insert(position, "")
    report.blank_lines += len(insertions)
    return result


def tidy_text(
    text: str,
    relative: str,
    memar_root: Path,
    rules: Sequence[str] = TIDY_RULES,
) -> tuple[str, TidyReport]:
    """Apply `rules` to one Khayyam file's text; newline style is the caller's."""
    report = TidyReport(relative)
    lines = text.split("\n")
    blocks = end_blocks(lines)
    head = lines[: blocks[0].marker] if blocks else list(lines)
    tail = lines[blocks[0].marker :] if blocks else []
    offset = blocks[0].marker if blocks else 0
    parsed: list[tuple[EndBlock, GoBlock | None]] = []
    for block in blocks:
        try:
            parsed.append((block, parse_go_block(lines[block.body : block.close])))
        except (SourceFailure, IndexError) as error:
            parsed.append((block, None))
            report.skipped.append(f"go block at line {block.marker + 1} does not parse: {error}")
    if "commented-generic-bindings" in rules:
        head = realize_generic_methods(
            head, [go for _, go in parsed if go is not None], relative, memar_root, report
        )
    if "go-clue-residue" in rules:
        for block, go in reversed(parsed):
            if go is None:
                continue
            first, last = block.marker - offset, block.last - offset
            body = tail[block.body - offset : block.close - offset]
            try:
                kept = shrink_go_lines(body, head, relative, report if not block.sealed else None)
            except (SourceFailure, IndexError) as error:
                report.skipped.append(f"go block at line {block.marker + 1}: {error}")
                continue
            if kept is None:
                if block.sealed:
                    shrink_go_lines(body, head, relative, report)
                del tail[first : last + 1]
                report.blocks_removed += 1
                continue
            if kept == body:
                continue
            if block.sealed:
                report.skipped.append(
                    f"go block at line {block.marker + 1} is sealed by its sha256; only removing it whole is applied"
                )
                continue
            tail[block.body - offset : block.close - offset] = kept
            report.blocks_shrunk += 1
        if blocks and not end_blocks(tail):
            while head and not head[-1].strip():
                head.pop()
            rest = [line for line in tail if line.strip()]
            tail = ["", *rest, ""] if rest else [""]
    if "result-parameter-names" in rules:
        head = rename_synthetic_parameters(head, report)
    if "method-separation" in rules:
        head = separate_methods(head, report)
    return "\n".join([*head, *tail]), report


def run_tidy(
    memar_root: Path,
    values: Sequence[str] = (),
    excludes: Sequence[str] = TIDY_EXCLUDES,
    rules: Sequence[str] = TIDY_RULES,
    write: bool = False,
) -> dict:
    memar_root = memar_root.resolve()
    reports: list[TidyReport] = []
    changed: list[str] = []
    for relative in tidy_paths(values, memar_root, excludes):
        path = memar_root / relative
        with path.open(encoding="utf-8", newline="") as handle:
            original = handle.read()
        newline = "\r\n" if "\r\n" in original else "\n"
        text, report = tidy_text(original.replace("\r\n", "\n"), relative, memar_root, rules)
        reports.append(report)
        text = text.replace("\n", newline)
        if text != original:
            changed.append(relative)
            if write:
                with path.open("w", encoding="utf-8", newline="") as handle:
                    handle.write(text)
    by_rule: dict[str, int] = {rule: 0 for rule in rules}
    for report in reports:
        if report.relative in changed:
            for rule in report.changed_by():
                by_rule[rule] = by_rule.get(rule, 0) + 1
    return {
        "files": len(reports),
        "changed": changed,
        "files_changed_by_rule": by_rule,
        "blank_lines": sum(report.blank_lines for report in reports),
        "licenses_removed": sum(report.licenses_removed for report in reports),
        "members_removed": sum(len(report.members_removed) for report in reports),
        "types_removed": sum(len(report.types_removed) for report in reports),
        "blocks_shrunk": sum(report.blocks_shrunk for report in reports),
        "blocks_removed": sum(report.blocks_removed for report in reports),
        "methods_realized": sum(len(report.methods_realized) for report in reports),
        "imports_added": sum(len(report.imports_added) for report in reports),
        "renames": sum(len(report.renames) for report in reports),
        "unresolved": [entry for report in reports for entry in report.unresolved],
        "open_parameters": sum(len(report.open_parameters) for report in reports),
        "reports": [
            {key: value for key, value in report.__dict__.items() if value}
            for report in reports
            if report.relative in changed or report.unresolved or report.skipped
        ],
    }


def build_tidy_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abstraction_bridge.py tidy",
        description="Apply the source-rewrite rules of modules/khayyam/rules/ to the ported corpus.",
    )
    parser.add_argument("paths", nargs="*", help="repository-relative .kh files or directories (default: modules)")
    parser.add_argument("--memar-root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        help=f"repository-relative prefix to leave alone (repeatable; default {', '.join(TIDY_EXCLUDES)})",
    )
    parser.add_argument("--rule", action="append", choices=TIDY_RULES, help="apply only this rule (repeatable)")
    parser.add_argument("--write", action="store_true", help="write; without it nothing is written")
    parser.add_argument("--report", help="write the machine readable report as JSON")
    return parser


def tidy_main(argv: Sequence[str]) -> int:
    arguments = build_tidy_parser().parse_args(list(argv))
    rules = tuple(rule for rule in TIDY_RULES if not arguments.rule or rule in arguments.rule)
    summary = run_tidy(
        Path(arguments.memar_root),
        arguments.paths,
        TIDY_EXCLUDES if arguments.exclude is None else arguments.exclude,
        rules,
        arguments.write,
    )
    if arguments.report:
        Path(arguments.report).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"files {summary['files']}  changed {len(summary['changed'])}  {'written' if arguments.write else 'dry'}")
    print("files changed by rule " + "  ".join(f"{rule} {count}" for rule, count in summary["files_changed_by_rule"].items()))
    print(f"blank lines {summary['blank_lines']}")
    print(
        "go blocks shrunk {blocks_shrunk}  removed {blocks_removed}  licenses {licenses_removed}  "
        "members {members_removed}  types {types_removed}".format(**summary)
    )
    print(f"generic methods realized {summary['methods_realized']}  imports added {summary['imports_added']}")
    print(f"result renames {summary['renames']}")
    print(f"generic methods over open type parameters (not a binding, left) {summary['open_parameters']}")
    print(f"unresolved generic methods {len(summary['unresolved'])}")
    for entry in summary["unresolved"]:
        print(f"  {entry['file']}: {entry['interface']}.{entry['method']} [{entry['binding']}] {entry['reason']}")
    return 0
