"""`transfer`: move one Go source -- a file, a package directory, or with --recursive a
whole tree -- into one Khayyam destination.

Unlike `reemit` it creates a destination that does not exist, and it never rewrites
one that does: it only inserts, and a result that would lose a line, a declaration
or a comment of the destination is not written. Whatever has a Khayyam form is
written as a declaration; every other construct stays in the destination as a
`TODO(go-migrate)` residue with its original Go text, and the whole Go file is kept
verbatim as comments at the end of the destination, so nothing the Go file said is
lost. Decisions the owner has not taken -- the integer and float capsules, the
unresolved names, generic instantiation names -- are residue with the blocker named,
never a guess."""

import re
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from dataclasses import dataclass
from typing import Sequence

from failures import (
    BridgeFailure,
    SourceFailure,
)
from comments import (
    comment_lines,
    render_comment,
    strip_comments,
)
from names import (
    FIXED_KHAYYAM_DECLARATIONS,
    PRIMITIVE_KHAYYAM_TYPES,
    UNMAPPED_PRIMITIVE_CAPSULES,
    archive_module,
    carries_identity,
    field_accessor_options,
    identity_carried,
    module_identity,
    normalize_module,
    pascal_segment,
    qualified_by_module,
    qualify_name,
    split_field_name,
)
from go_source import (
    GoConstruct,
    GoSource,
    Parameter,
    balanced_end,
    doc_comment_starts,
    go_constructs,
    has_unmappable_type,
    lex_source,
    parse_go_source,
)
from khayyam_source import (
    KEYWORDS,
    KHAYYAM_INCLUSION,
    KhayyamParameter,
    khayyam_declarations,
    khayyam_uri,
    render_khayyam_method,
)
from go_source_block import (
    CORPUS_LICENSE,
    GO_MIGRATE,
    RESIDUE_MARKER,
    SOURCE_BLOCK_HEAD,
    comment_out,
    comment_text,
    go_source_lines,
    render_source_block,
    residue_marker,
    source_blocks,
    verify_source_block,
)
from khayyam_frontend import FRONTEND_CHECK
from corpus_port import (
    CorpusDecl,
    CorpusPort,
)


# ---------------------------------------------------------------------------
# Transfer: one Go source -- a file, a package directory, or with --recursive
# a whole tree -- into one Khayyam destination.
#
# Unlike `reemit` it creates a destination that does not exist, and it never
# rewrites one that does: it only inserts, and a result that would lose a line,
# a declaration or a comment of the destination is not written. Whatever has a
# Khayyam form is written as a declaration; every other construct stays in the
# destination as a `TODO(go-migrate)` residue with its original Go text, and the
# whole Go file is kept verbatim as comments at the end of the destination, so
# nothing the Go file said is lost. Decisions the owner has not taken -- the
# integer and float capsules, the unresolved names, generic instantiation names
# -- are residue with the blocker named, never a guess.
# ---------------------------------------------------------------------------


def insertion_hazards(before: str, after: str) -> list[str]:
    """What turning `before` into `after` would lose. A transfer only inserts,
    so every line of `before` must still be there, in order, and no count of a
    declaration kind or comment line may fall."""
    hazards: list[str] = []
    new = after.split("\n")
    cursor = 0
    for index, line in enumerate(before.split("\n")):
        while cursor < len(new) and new[cursor] != line:
            cursor += 1
        if cursor >= len(new):
            hazards.append(f"would drop or reorder line {index + 1}: {line[:80]!r}")
            break
        cursor += 1
    counts_before: dict[str, int] = {}
    counts_after: dict[str, int] = {}
    for counts, text in ((counts_before, before), (counts_after, after)):
        for _, kind, _ in khayyam_declarations(text):
            counts[kind] = counts.get(kind, 0) + 1
    for kind, count in sorted(counts_before.items()):
        if counts_after.get(kind, 0) < count:
            hazards.append(f"would drop {count - counts_after.get(kind, 0)} `{kind}` declaration(s)")
    kept = {" ".join(line.split()) for line in comment_lines(after)}
    lost = [
        line for line in (" ".join(text.split()) for text in comment_lines(before)) if line not in kept
    ]
    if lost:
        hazards.append(f"would drop {len(lost)} comment line(s), first {lost[0][:80]!r}")
    return hazards


@dataclass
class TransferItem:
    source: Path
    label: str
    relative: str
    module: str
    dest: Path
    dest_relative: str
    skip: str = ""


@dataclass
class TransferHome:
    name: str
    home: str
    state: str


@dataclass
class TransferEntry:
    source: str
    dest: str
    construct: str
    line: int
    state: str
    reason: str = ""


class GoTransfer:
    """Transfers Go files into Khayyam destinations, inserting only."""

    def __init__(
        self,
        items: Sequence[TransferItem],
        memar_root: Path,
        go_root: Path | None = None,
        frontend: bool = True,
        source_only: bool = False,
    ) -> None:
        self.items = list(items)
        self.memar_root = memar_root.resolve()
        self.go_root = go_root.resolve() if go_root else None
        self.frontend = frontend
        self.source_only = source_only
        self.raw: dict[str, bytes] = {}
        self.sources: dict[str, GoSource] = {}
        self.code_lines: dict[str, list[str]] = {}
        self.constructs: dict[str, list[GoConstruct]] = {}
        self.texts: dict[str, str | None] = {}
        self.newlines: dict[str, str] = {}
        self.holders: dict[str, set[str]] = {}
        self.declarations_of: dict[str, list[tuple[str, str, str]]] = {}
        self.by_directory: dict[str, list[str]] = {}
        self.go_types: dict[str, CorpusDecl] = {}
        self.homes: dict[str, TransferHome] = {}
        self.unresolved_names: dict[str, str] = {}
        self.demoted: dict[str, str] = {}
        self.refused_before: dict[str, str] = {}
        self.dependents: dict[str, dict[str, dict]] = {}
        self.outcomes: dict[str, dict] = {}
        self.run_names: set[str] = set()
        self.port: CorpusPort | None = None
        self.module_name = ""
        self.entries: list[TransferEntry] = []
        self.outputs: dict[str, str] = {}
        self.files: dict[str, str] = {}
        self.rounds = 0

    # -- loading ------------------------------------------------------------

    def load(self) -> None:
        for item in self.items:
            if item.skip:
                continue
            raw = item.source.read_bytes()
            self.raw[item.label] = raw
            text = raw.decode("utf-8", errors="replace")
            if not re.search(r"(?m)^package\s+\w+", text):
                item.skip = "not a Go source: no package clause"
                continue
            try:
                tokens = lex_source(text, True)
                source = parse_go_source(str(item.source), text)
                self.constructs[item.label] = go_constructs(text, tokens, source)
            except (SourceFailure, IndexError) as error:
                self.constructs[item.label] = []
                self.sources[item.label] = GoSource(str(item.source), "", {}, [], [], [])
                self.entries.append(
                    TransferEntry(item.label, item.dest_relative, "file", 0, "unreadable", str(error))
                )
                continue
            self.sources[item.label] = source
            self.code_lines[item.label] = strip_comments(text).split("\n")
        modules = self.memar_root / "modules"
        for path in sorted(modules.rglob("*.kh")) if modules.exists() else []:
            if "node_modules" in path.parts:
                continue
            relative = path.relative_to(self.memar_root).as_posix()
            text = path.read_text(encoding="utf-8", errors="replace")
            self.index(relative, text)
        for item in self.items:
            if item.skip or item.dest_relative in self.texts:
                continue
            if item.dest.exists():
                with item.dest.open(encoding="utf-8", newline="") as handle:
                    text = handle.read()
                self.newlines[item.dest_relative] = "\r\n" if "\r\n" in text else "\n"
                self.texts[item.dest_relative] = text.replace("\r\n", "\n")
            else:
                self.texts[item.dest_relative] = None
        if self.go_root is not None and (self.go_root / "go.mod").exists():
            self.port = CorpusPort(self.go_root, self.memar_root)
            self.port.prepare()
            self.module_name = self.port.module_name
            self.go_types = dict(self.port.declarations)
        for item in self.items:
            if item.skip:
                continue
            source = self.sources[item.label]
            interfaces = {interface.name: interface for interface in source.interfaces}
            for declaration in source.types:
                key = f"{item.module}\x00{declaration.name}"
                if key in self.go_types:
                    continue
                interface = interfaces.get(declaration.name) if declaration.kind == "interface" else None
                constraint = bool(
                    interface is not None
                    and not interface.entries
                    and any(composition.constraint for composition in interface.compositions)
                )
                self.go_types[key] = CorpusDecl(
                    key=key,
                    name=declaration.name,
                    module=item.module,
                    kind="constraint" if constraint else ("interface" if interface else declaration.kind),
                    generic=declaration.generic,
                    type_params=list(declaration.type_params),
                    doc=list(declaration.doc),
                    path=str(item.source),
                    line=declaration.line,
                    source_stem=item.source.stem,
                    interface=interface,
                    declaration=declaration,
                )

    def index(self, relative: str, text: str) -> None:
        declarations = khayyam_declarations(text)
        self.declarations_of[relative] = declarations
        self.by_directory.setdefault(relative.rsplit("/", 1)[0], []).append(relative)
        for name, kind, _ in declarations:
            if kind in {"ab", "mt", "cp", "sc", "vr"}:
                self.holders.setdefault(name, set()).add(relative)

    # -- placement and names -----------------------------------------------

    @staticmethod
    def portable(decl: CorpusDecl) -> bool:
        declaration = decl.declaration
        if declaration is None or declaration.alias or decl.generic:
            return False
        if decl.kind == "interface":
            return True
        return decl.kind == "named" and declaration.underlying.strip() in UNMAPPED_PRIMITIVE_CAPSULES

    def present(self, name: str, module: str, dest: str) -> tuple[str, str] | None:
        for declared, kind, _ in self.declarations_of.get(dest, []):
            if kind in {"ab", "cp"} and qualified_by_module(name, declared, module):
                return declared, dest
        for relative in self.by_directory.get(dest.rsplit("/", 1)[0], []):
            if relative == dest:
                continue
            for declared, kind, _ in self.declarations_of.get(relative, []):
                if kind in {"ab", "cp"} and declared == name:
                    return declared, relative
        return None

    def plan_homes(self) -> None:
        self.homes = {}
        self.unresolved_names = {}
        if self.port is not None:
            for key, claims in self.port.claimed.items():
                decl = self.port.declarations.get(key)
                preferred = [claim for claim in claims if decl and claim[0].relative == decl.output_file]
                target, name = (preferred or claims)[0]
                if any(
                    declared == name and kind in {"ab", "cp"}
                    for declared, kind, _ in self.declarations_of.get(target.relative, [])
                ):
                    self.homes[key] = TransferHome(name, target.relative, "archive")
        candidates: list[tuple[TransferItem, GoConstruct, str]] = []
        for item in self.items:
            if item.skip:
                continue
            for construct in self.constructs.get(item.label, []):
                if construct.kind != "type":
                    continue
                key = f"{item.module}\x00{construct.name}"
                decl = self.go_types.get(key)
                if decl is None or decl.path != str(item.source) or key in self.homes:
                    continue
                portable = self.portable(decl)
                if not portable and decl.kind != "interface":
                    continue
                found = self.present(construct.name, item.module, item.dest_relative)
                if found:
                    self.homes[key] = TransferHome(found[0], found[1], "present")
                    continue
                if not portable:
                    continue
                if item.dest_relative in self.demoted:
                    self.unresolved_names[key] = self.demoted[item.dest_relative]
                    continue
                candidates.append((item, construct, key))
        modules_of: dict[str, set[str]] = {}
        for item, construct, _ in candidates:
            modules_of.setdefault(construct.name, set()).add(item.module)
        taken = set(self.holders) | set(KEYWORDS) | {home.name for home in self.homes.values()}
        for item, construct, key in sorted(
            candidates, key=lambda entry: (entry[0].module, entry[0].label, entry[1].head)
        ):
            options: list[str] = []
            names = self.port.names if self.port is not None else None
            if names is not None and key in names.output and key not in names.unrenderable:
                options.append(names.output[key])
            if len(modules_of[construct.name]) == 1:
                options.append(construct.name)
            identities = module_identity(item.module)
            identity = pascal_segment(identities[0]) if identities else ""
            if identity and not identity_carried(identity, construct.name):
                options.append(qualify_name(identity, construct.name))
            elif construct.name not in options:
                options.append(construct.name)
            chosen = next((option for option in options if option not in taken), None)
            if chosen is None:
                holders = sorted(
                    {holder for option in options for holder in self.holders.get(option, ())}
                )[:3]
                self.unresolved_names[key] = (
                    "naming unresolved: {} already declared{}; the name is an owner decision".format(
                        " and ".join(f"`{option}`" for option in dict.fromkeys(options)),
                        f" ({', '.join(holders)})" if holders else "",
                    )
                )
                continue
            taken.add(chosen)
            self.homes[key] = TransferHome(chosen, item.dest_relative, "new")

    def import_module(self, import_path: str) -> str | None:
        prefix = self.module_name
        if prefix and import_path.startswith(prefix + "/"):
            return import_path[len(prefix) + 1 :]
        if prefix and import_path == prefix:
            return ""
        return None

    def primitive_home(self, name: str) -> str | None:
        for (module, _), fixed in FIXED_KHAYYAM_DECLARATIONS.items():
            if fixed != name:
                continue
            homes = sorted(
                relative
                for relative in self.holders.get(name, ())
                if relative.startswith(f"modules/{module}/")
                and any(
                    declared == name and kind in {"ab", "cp"}
                    for declared, kind, _ in self.declarations_of.get(relative, [])
                )
            )
            if homes:
                return homes[0]
        return None

    def resolve_reference(self, text: str, item: TransferItem) -> tuple[str, str] | str:
        """The Khayyam name and home of Go type `text`, or why there is none."""
        value = " ".join(text.split())
        if value in PRIMITIVE_KHAYYAM_TYPES:
            name = PRIMITIVE_KHAYYAM_TYPES[value]
            home = self.primitive_home(name)
            return (name, home) if home else f"no archive file declares {name} for Go {value!r}"
        if value in UNMAPPED_PRIMITIVE_CAPSULES:
            return (
                f"Go {value!r}: the integer/float capsule mapping is an owner decision "
                "(migration-plan.md, decision 1)"
            )
        if value in {"any", "interface{}", "interface {}", "comparable"}:
            return f"Go {value!r} has no Khayyam form"
        if "[" in value and value.endswith("]") and not value.startswith("["):
            return f"Go generic instantiation {value!r}: instantiation names are reemit's, not transfer's"
        try:
            tokens = lex_source(value, True)[:-1]
        except SourceFailure as error:
            return f"Go type {value!r} does not scan: {error}"
        unmappable = has_unmappable_type(tokens)
        if unmappable:
            return f"Go {unmappable} type {value!r} has no systematic Khayyam form"
        if "." in value:
            alias, _, name = value.partition(".")
            import_path = self.sources[item.label].imports.get(alias)
            if import_path is None:
                return f"Go {value!r}: no import named {alias!r}"
            module = self.import_module(import_path)
            if module is None:
                return f"Go {value!r} is outside the Go module (standard library or external)"
            key = f"{normalize_module(module)}\x00{name}"
        else:
            key = f"{item.module}\x00{value}"
        home = self.homes.get(key)
        if home is not None:
            return home.name, home.home
        if key in self.unresolved_names:
            return self.unresolved_names[key]
        decl = self.go_types.get(key)
        if decl is None:
            return f"Go {value!r} is not declared in the corpus"
        return f"Go {value!r} ({decl.kind}) has no Khayyam declaration yet"

    # -- rendering ----------------------------------------------------------

    def render(self, item: TransferItem, current: str | None) -> tuple[str | None, list[TransferEntry]]:
        entries: list[TransferEntry] = []
        text = current if current is not None else ""
        lines_now = text.split("\n")
        declared = khayyam_declarations(text)
        visible = {name for name, _, _ in declared}
        source_lines = go_source_lines(self.raw[item.label])
        code_lines = self.code_lines.get(item.label, [])
        starts = doc_comment_starts("\n".join(source_lines))
        imports: dict[str, str] = {}
        blocks: list[list[str]] = []
        needs_marker = False
        dest = item.dest_relative
        demoted = self.demoted.get(dest)
        outside = list(lines_now)
        for _, _, first, last in source_blocks(text):
            outside[first : last + 1] = [""] * (last + 1 - first)
        hand_quoted = {comment_text(line) for line in outside if line.startswith("//")}
        hand_residue = any(
            line.strip().startswith(f"// {GO_MIGRATE}:")
            and not RESIDUE_MARKER.match(line)
            and not line.startswith(f"// {GO_MIGRATE}: manual port from ")
            for line in outside
        )

        def entry(construct: str, line: int, state: str, reason: str = "") -> None:
            entries.append(TransferEntry(item.label, dest, construct, line, state, reason))

        def quote(first: int, last: int) -> list[str]:
            return [comment_out(line) for line in source_lines[first - 1 : last]]

        def residue_block(reason: str, first: int, last: int, quoted_last: int | None = None) -> list[str]:
            shown = last if quoted_last is None else quoted_last
            return [
                f"// {GO_MIGRATE}: {reason}. Original Go ({item.label}:{first}-{shown}):",
                *quote(first, shown),
            ]

        def add_residue(construct: str, line: int, block: list[str], reason: str, target: list[str] | None = None) -> None:
            nonlocal needs_marker
            needs_marker = True
            if "\n".join(block) in text:
                entry(construct, line, "present", "residue already in the destination")
                return
            quoted = [comment_text(part) for part in block[1:] if comment_text(part)]
            if hand_residue and quoted and all(part in hand_quoted for part in quoted):
                entry(construct, line, "present", "the destination already quotes this Go text under its own TODO(go-migrate)")
                return
            entry(construct, line, "residue", reason)
            if target is None:
                blocks.append(block)
            else:
                target.extend(block)

        def take_name(options: Sequence[str]) -> str | None:
            for option in options:
                if option not in self.holders and option not in self.run_names and option not in KEYWORDS:
                    self.run_names.add(option)
                    return option
            return None

        def materialize(name: str, home: str) -> None:
            if home != dest and name not in visible:
                imports[name] = khayyam_uri(home)

        type_parameters: set[str] = set()

        def parameters(values: Sequence[Parameter], result: bool) -> list[tuple[str, str, str]] | str:
            rendered: list[tuple[str, str, str]] = []
            used: set[str] = set()
            for index, parameter in enumerate(values):
                if parameter.variadic:
                    return f"variadic parameter `...{parameter.type_text}` has no Khayyam form"
                if parameter.type_text.strip() in type_parameters:
                    return (
                        f"type parameter `{parameter.type_text.strip()}` is bound per instantiation, "
                        "and instantiation names are reemit's"
                    )
                name = parameter.name
                if not name or name == "_":
                    name = f"{'result' if result else 'arg'}{index}"
                if name in KEYWORDS:
                    name = f"{name}_"
                if name in used:
                    name = f"{name}_{index}"
                used.add(name)
                reference = self.resolve_reference(parameter.type_text, item)
                if isinstance(reference, str):
                    return reference
                rendered.append((name, reference[0], reference[1]))
            return rendered

        def has_method(owner: str, method: str, where: str) -> bool:
            declarations = declared if where == dest else self.declarations_of.get(where, [])
            return any(
                kind == "mt" and detail == owner and (name == method or name.endswith("_" + method))
                for name, kind, detail in declarations
            )

        unreadable = next(
            (
                entry.reason
                for entry in self.entries
                if entry.source == item.label and entry.state == "unreadable"
            ),
            None,
        )
        source_only = self.source_only and current is not None
        if source_only:
            # A hand port carries its own declarations and naming decisions;
            # generated ones beside them would decide what its TODOs leave open.
            entry("file", 1, "consumed", "--source-only: the destination's declarations are its own")
            needs_marker = hand_residue
        elif unreadable is not None:
            reason = f"the transfer could not parse this Go file ({unreadable}); nothing was ported"
            add_residue(
                "file",
                1,
                [f"// {GO_MIGRATE}: {reason}. Original Go: the go-source block at the end of this file"],
                reason,
            )

        for construct in [] if source_only else self.constructs.get(item.label, []):
            label = f"{construct.kind} {construct.name}"
            if construct.kind in {"package", "import"}:
                entry(label, construct.head, "consumed", "carried by the file and its `in` lines")
                continue
            if construct.kind in {"func", "method"}:
                what = "method" if construct.kind == "method" else "function"
                if construct.body:
                    reason = (
                        f"{what} implementation not ported; its body (lines {construct.body}-"
                        f"{construct.end}) is in the go-source block at the end of this file"
                    )
                    block = residue_block(reason, construct.start, construct.end, construct.body)
                else:
                    reason = f"{what} declaration without a body has no Khayyam form"
                    block = residue_block(reason, construct.start, construct.end)
                add_residue(label, construct.head, block, reason)
                continue
            if construct.kind == "const":
                reason = "const: docs/khayyam documents no constant form"
                if construct.value is not None and construct.value.iota:
                    reason += "; the iota sequence is kept as written"
                add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                continue
            if construct.kind == "var":
                value = construct.value
                if value is None or value.value_text:
                    reason = "var with an initial value: docs/khayyam documents no initializer form"
                    add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                    continue
                reference = self.resolve_reference(value.type_text, item) if value.type_text else "var without a type"
                if demoted and not isinstance(reference, str):
                    reference = demoted
                if isinstance(reference, str):
                    reason = f"var type not portable: {reference}"
                    add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                    continue
                identities = module_identity(item.module)
                identity = pascal_segment(identities[0]) if identities else ""
                for name in value.names:
                    if any(declared_name == name and kind == "vr" for declared_name, kind, _ in declared):
                        entry(f"var {name}", construct.head, "present")
                        continue
                    options = [name] + ([f"{identity}_{name}"] if identity and not carries_identity(identity, name) else [])
                    chosen = take_name(options)
                    if chosen is None:
                        reason = f"var naming unresolved: {' and '.join(options)} already declared; the name is an owner decision"
                        add_residue(f"var {name}", construct.head, residue_block(reason, construct.start, construct.end), reason)
                        continue
                    materialize(reference[0], reference[1])
                    # The doc comment is Go comment text already, and both
                    # comment forms are Khayyam's too.
                    block: list[str] = list(source_lines[construct.start - 1 : construct.head - 1])
                    reason = (
                        "Khayyam has no assignment operator, so how this vr is bound to the value "
                        "Go assigned elsewhere is undecided"
                    )
                    binding = residue_block(reason, construct.head, construct.end)
                    add_residue(f"var {name} binding", construct.head, binding, reason, block)
                    block.append(f"vr {chosen} {reference[0]}")
                    visible.add(chosen)
                    entry(f"var {name}", construct.head, "emitted", f"vr {chosen}")
                    blocks.append(block)
                continue
            # type
            key = f"{item.module}\x00{construct.name}"
            decl = self.go_types.get(key)
            declaration = construct.declaration
            if decl is None or declaration is None or decl.path != str(item.source):
                if decl is not None and declaration is not None:
                    other = Path(decl.path)
                    other_label = (
                        other.relative_to(self.go_root).as_posix()
                        if self.go_root and other.is_relative_to(self.go_root)
                        else other.name
                    )
                    reason = (
                        f"{other_label} declares `{construct.name}` in the same Go package too "
                        "(a build variant or an ignored copy); only one declaration can carry the name"
                    )
                else:
                    reason = "type declaration the transfer could not read"
                add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                continue
            home = self.homes.get(key)
            type_parameters.clear()
            type_parameters.update(decl.type_params)
            if not self.portable(decl) and (home is None or decl.kind != "interface"):
                if decl.kind == "struct":
                    reason = "struct: capsule fields are not generated by transfer; the fields and their types need a manual port"
                elif decl.kind == "constraint":
                    reason = "type constraint: no abstraction form"
                elif decl.kind == "interface":
                    reason = "generic interface: its abstraction and instantiation names are reemit's or the owner's decision"
                elif declaration.alias:
                    reason = "type alias: no Khayyam form"
                else:
                    reason = f"named type over `{declaration.underlying}`: no systematic Khayyam form"
                add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                continue
            if home is None:
                reason = self.unresolved_names.get(key, "no home for this declaration")
                add_residue(label, construct.head, residue_block(reason, construct.start, construct.end), reason)
                continue
            owner = home.name
            interface = decl.interface
            if home.home != dest:
                entry(label, construct.head, "present", f"declared as {owner} in {home.home}")
                for member in interface.entries if interface else []:
                    if has_method(owner, member.name, home.home):
                        entry(f"method {construct.name}.{member.name}", member.line, "present", home.home)
                        continue
                    first = starts.get(member.line, member.line)
                    reason = (
                        f"{owner} is declared in {home.home}, which lacks this member; "
                        f"transfer only writes {dest}"
                    )
                    add_residue(
                        f"method {construct.name}.{member.name}",
                        member.line,
                        residue_block(reason, first, balanced_end(code_lines, member.line)),
                        reason,
                    )
                continue
            block = []
            fresh = not any(name == owner and kind in {"ab", "cp"} for name, kind, _ in declared)
            if not fresh:
                entry(label, construct.head, "present", owner)
            compositions: list[tuple[str, list[str]]] = []
            for composition in interface.compositions if interface else []:
                first = starts.get(composition.line, composition.line)
                reference = self.resolve_reference(composition.text, item)
                if isinstance(reference, str) or composition.anonymous or composition.constraint:
                    reason = f"embedded `{composition.text}` not portable: " + (
                        reference if isinstance(reference, str) else "anonymous or constraint element"
                    )
                    add_residue(
                        f"embed {construct.name}.{composition.text}",
                        composition.line,
                        residue_block(reason, first, balanced_end(code_lines, composition.line)),
                        reason,
                    )
                    continue
                if not fresh:
                    if re.search(rf"(?m)^\s+{re.escape(reference[0])}\s*$", strip_comments(text)):
                        entry(f"embed {construct.name}.{composition.text}", composition.line, "present")
                        continue
                    reason = (
                        f"embedded `{composition.text}` ({reference[0]}) is missing from the existing "
                        f"`{owner}` block; transfer does not edit an existing block"
                    )
                    add_residue(
                        f"embed {construct.name}.{composition.text}",
                        composition.line,
                        residue_block(reason, first, balanced_end(code_lines, composition.line)),
                        reason,
                    )
                    continue
                materialize(reference[0], reference[1])
                compositions.append((reference[0], list(composition.doc)))
                entry(f"embed {construct.name}.{composition.text}", composition.line, "emitted", reference[0])
            if fresh:
                block.extend(render_comment(decl.doc))
                if compositions:
                    block.append(f"tp {owner} ab {{")
                    for name, documentation in compositions:
                        block.extend(render_comment(documentation))
                        block.append(f"    {name}")
                    block.append("}")
                else:
                    block.append(f"tp {owner} ab")
                visible.add(owner)
                entry(label, construct.head, "emitted", f"tp {owner} ab")
                if interface is None:
                    reason = (
                        f"underlying Go type `{declaration.underlying}`: the integer/float capsule "
                        f"mapping is an owner decision; `{owner}` stands for the named type"
                    )
                    add_residue(
                        f"{label} underlying", construct.head,
                        residue_block(reason, construct.head, construct.end), reason, block,
                    )
            for member in interface.entries if interface else []:
                member_label = f"method {construct.name}.{member.name}"
                first = starts.get(member.line, member.line)
                last = balanced_end(code_lines, member.line)
                if not fresh and has_method(owner, member.name, dest):
                    entry(member_label, member.line, "present")
                    continue
                if demoted:
                    add_residue(member_label, member.line, residue_block(demoted, first, last), demoted, block)
                    continue
                if member.generic:
                    reason = "generic method: its type parameters are bound per call, not per abstraction"
                    add_residue(member_label, member.line, residue_block(reason, first, last), reason, block)
                    continue
                influencing = parameters(member.parameters, False)
                influenced = parameters(member.results, True) if not isinstance(influencing, str) else influencing
                if isinstance(influencing, str) or isinstance(influenced, str):
                    reason = f"method not portable: {influencing if isinstance(influencing, str) else influenced}"
                    add_residue(member_label, member.line, residue_block(reason, first, last), reason, block)
                    continue
                if split_field_name(owner) is not None:
                    options = field_accessor_options(owner, member.name, [type_name_ for _, type_name_, _ in influenced])
                else:
                    options = [
                        member.name,
                        f"{owner}_{member.name}",
                        *[f"{owner}_{member.name}_{pascal_segment(identity)}" for identity in module_identity(item.module)],
                    ]
                chosen = take_name(options)
                if chosen is None:
                    reason = f"method naming unresolved: {', '.join(options)} are all declared; the name is an owner decision"
                    add_residue(member_label, member.line, residue_block(reason, first, last), reason, block)
                    continue
                for _, type_name_, home_ in [*influencing, *influenced]:
                    materialize(type_name_, home_)
                block.extend(render_comment(member.doc))
                block.append(
                    render_khayyam_method(
                        chosen,
                        owner,
                        [KhayyamParameter(name, type_name_) for name, type_name_, _ in influencing],
                        [KhayyamParameter(name, type_name_) for name, type_name_, _ in influenced],
                    )
                )
                visible.add(chosen)
                entry(member_label, member.line, "emitted", chosen)
            if block:
                blocks.append(block)

        source_block = render_source_block(item.label, self.raw[item.label])
        block_present = source_block[1] in lines_now
        marker = residue_marker(item.label)
        add_marker = needs_marker and marker not in lines_now
        import_lines = [f'tp {name} in "{imports[name]}"' for name in sorted(imports)]
        if not blocks and not import_lines and block_present and not add_marker:
            return current, entries
        if current is None:
            output: list[str] = [marker] if needs_marker else []
            output += [CORPUS_LICENSE, ""]
            if import_lines:
                output += import_lines + [""]
            for block in blocks:
                output += block + [""]
            output += source_block
            return "\n".join(output) + "\n", entries
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines.pop()
        existing_blocks = source_blocks(text)
        tail = existing_blocks[0][2] if existing_blocks else len(lines)
        last_import = max(
            (index for index, line in enumerate(lines[:tail]) if re.match(r'^tp\s+\S+\s+in\s+"', line)),
            default=None,
        )
        additions: list[str] = []
        if import_lines and last_import is None:
            additions += [""] + import_lines
        for block in blocks:
            additions += [""] + block
        if additions and tail < len(lines):
            additions.append("")
        result = list(lines[:tail]) + additions + list(lines[tail:])
        if import_lines and last_import is not None:
            result[last_import + 1 : last_import + 1] = import_lines
        if not block_present:
            result += [""] + source_block
        if add_marker:
            result.insert(0, marker)
        return "\n".join(result) + "\n", entries

    def render_all(self) -> dict[str, str | None]:
        # A new abstraction keeps the bare name and a method that wants it is
        # qualified -- the policy `CorpusPort.member_name` already follows.
        self.run_names = {home.name for home in self.homes.values() if home.state == "new"}
        self.entries = [entry for entry in self.entries if entry.state == "unreadable"]
        texts: dict[str, str | None] = dict(self.texts)
        for item in self.items:
            if item.skip:
                self.entries.append(
                    TransferEntry(item.label, item.dest_relative, "file", 0, "skipped", item.skip)
                )
                continue
            rendered, entries = self.render(item, texts[item.dest_relative])
            texts[item.dest_relative] = rendered
            self.entries.extend(entries)
        return texts

    # -- frontend -----------------------------------------------------------

    def check(self, overrides: dict[str, str], paths: Sequence[str]) -> dict[str, dict]:
        if not paths:
            return {}
        node = shutil.which("node")
        if node is None:
            raise BridgeFailure(["node is not on PATH; run with --no-frontend to skip the Khayyam frontend"])
        with tempfile.TemporaryDirectory() as directory:
            request = Path(directory) / "request.json"
            request.write_text(
                json.dumps({"root": str(self.memar_root), "paths": list(paths), "overrides": overrides}),
                encoding="utf-8",
            )
            completed = subprocess.run(
                [node, str(FRONTEND_CHECK), str(request)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
        if completed.returncode != 0:
            raise BridgeFailure([f"frontend check failed: {completed.stderr.strip()[:400]}"])
        return json.loads(completed.stdout)

    def check_dependents(self, changed: dict[str, str]) -> None:
        """Record untouched archive files whose frontend outcome a created file changes.

        A file created here can satisfy a URI an existing file already carries,
        so that file's outcome moves even though transfer never edits it.
        """
        created = {dest for dest in changed if self.texts.get(dest) is None}
        if not created:
            return
        importers = []
        for path in sorted((self.memar_root / "modules").rglob("*.kh")):
            relative = path.relative_to(self.memar_root).as_posix()
            if relative in changed:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if any(uri in created for uri in KHAYYAM_INCLUSION.findall(text)):
                importers.append(relative)
        if not importers:
            return
        before = self.check({}, importers)
        after = self.check(changed, importers)
        for relative in importers:
            if before.get(relative) != after.get(relative):
                self.dependents[relative] = {"before": before.get(relative, {}), "after": after.get(relative, {})}

    # -- driver -------------------------------------------------------------

    def run(self, write: bool) -> dict:
        self.load()
        if self.frontend:
            existing = sorted(dest for dest, text in self.texts.items() if text is not None)
            for dest, outcome in self.check({}, existing).items():
                if outcome.get("outcome") == "refuse":
                    reason = f"{outcome.get('reason')} at line {outcome.get('line')}"
                    self.refused_before[dest] = reason
                    self.demoted[dest] = (
                        f"the destination was already refused by the Khayyam frontend ({reason}), "
                        "so no declaration is added to it"
                    )
        while True:
            self.rounds += 1
            self.plan_homes()
            outputs = self.render_all()
            changed = {
                dest: text
                for dest, text in outputs.items()
                if text is not None and text != self.texts.get(dest)
            }
            if not self.frontend:
                break
            self.outcomes = self.check(changed, sorted(changed))
            refused = {
                dest: outcome
                for dest, outcome in self.outcomes.items()
                if outcome.get("outcome") == "refuse" and dest not in self.demoted
            }
            if not refused or self.rounds >= 12:
                break
            for dest, outcome in refused.items():
                self.demoted[dest] = (
                    f"the Khayyam frontend refused the declarations transfer generated here "
                    f"({outcome.get('reason')} at line {outcome.get('line')}), so they are kept as residue"
                )
        self.outputs = {dest: text for dest, text in outputs.items() if text is not None}
        if self.frontend:
            self.check_dependents(changed)
        for dest in sorted(self.outputs):
            text = self.outputs[dest]
            original = self.texts.get(dest)
            if text == original:
                self.files[dest] = "unchanged"
                continue
            if original is not None:
                hazards = insertion_hazards(original, text)
                if hazards:
                    self.files[dest] = "guarded: target-would-lose-content: " + "; ".join(hazards)
                    continue
            outcome = self.outcomes.get(dest, {})
            if self.frontend and outcome.get("outcome") == "refuse" and dest not in self.refused_before:
                self.files[dest] = f"guarded: frontend refuses the result ({outcome.get('reason')} at line {outcome.get('line')})"
                continue
            state = "created" if original is None else "appended"
            if write:
                path = self.memar_root / dest
                if path.exists():
                    with path.open(encoding="utf-8", newline="") as handle:
                        on_disk: str | None = handle.read().replace("\r\n", "\n")
                else:
                    on_disk = None
                if on_disk != original:
                    self.files[dest] = "guarded: target-changed-during-run"
                    continue
                path.parent.mkdir(parents=True, exist_ok=True)
                with path.open("w", encoding="utf-8", newline="") as handle:
                    handle.write(text.replace("\n", self.newlines.get(dest, "\n")))
            self.files[dest] = state
        for item in self.items:
            if item.skip and item.dest_relative not in self.files:
                self.files.setdefault(item.dest_relative, f"skipped: {item.skip}")
        return self.summary(write)

    def summary(self, write: bool) -> dict:
        states: dict[str, int] = {}
        for entry in self.entries:
            states[entry.state] = states.get(entry.state, 0) + 1
        files: dict[str, int] = {}
        for state in self.files.values():
            key = state.split(":", 1)[0] if state.startswith(("guarded", "skipped")) else state
            files[key] = files.get(key, 0) + 1
        todo_blocks = 0
        for dest, text in self.outputs.items():
            original = self.texts.get(dest) or ""
            if self.files.get(dest) not in {"created", "appended"}:
                continue
            todo_blocks += sum(
                1
                for line in text.split("\n")
                if line.startswith(f"// {GO_MIGRATE}:")
                and not RESIDUE_MARKER.match(line)
                and line != SOURCE_BLOCK_HEAD
            ) - sum(
                1
                for line in original.split("\n")
                if line.startswith(f"// {GO_MIGRATE}:")
                and not RESIDUE_MARKER.match(line)
                and line != SOURCE_BLOCK_HEAD
            )
        per_source: dict[str, dict[str, int]] = {}
        for entry in self.entries:
            counts = per_source.setdefault(entry.source, {})
            counts[entry.state] = counts.get(entry.state, 0) + 1
        return {
            "mode": "write" if write else "dry-run",
            "sources": len(self.items),
            "files": files,
            "constructs": states,
            "todo_blocks_added": todo_blocks,
            "frontend_rounds": self.rounds,
            "demoted": dict(sorted(self.demoted.items())),
            "refused_before_transfer": dict(sorted(self.refused_before.items())),
            "dependents_changed": dict(sorted(self.dependents.items())),
            "file_states": dict(sorted(self.files.items())),
            "per_source": per_source,
            "entries": [entry.__dict__ for entry in self.entries],
        }


def transfer_items(
    source: Path,
    dest: Path,
    memar_root: Path,
    go_root: Path | None,
    recursive: bool,
    excludes: Sequence[str] = (),
) -> list[TransferItem]:
    source = source.resolve()
    dest = dest.resolve() if dest.is_absolute() else (Path.cwd() / dest).resolve()
    memar_root = memar_root.resolve()
    go_root = go_root.resolve() if go_root else None
    if source.is_file():
        files = [source]
    elif recursive:
        files = sorted(path for path in source.rglob("*.go") if ".git" not in path.parts)
    else:
        files = sorted(source.glob("*.go"))
    items: list[TransferItem] = []
    for path in files:
        base = next(
            (root for root in (go_root, memar_root) if root is not None and path.is_relative_to(root)),
            None,
        )
        relative = path.relative_to(base).as_posix() if base else path.name
        label = f"{base.name}/{relative}" if base else path.name
        parent = Path(relative).parent.as_posix()
        in_archive = base is not None and base == memar_root and base != go_root
        relocate = archive_module if in_archive else normalize_module
        module = relocate("" if parent == "." else parent)
        if source.is_file():
            target = dest if dest.suffix == ".kh" else dest / f"{path.stem}.kh"
        elif recursive:
            inner = path.parent.relative_to(source).as_posix()
            inner = "" if inner == "." else inner
            if in_archive:
                placed = archive_module(inner) if source == memar_root else inner
            else:
                placed = normalize_module(inner)
            target = (dest / placed if placed else dest) / f"{path.stem}.kh"
        else:
            target = dest / f"{path.stem}.kh"
        skip = ""
        if not target.is_relative_to(memar_root):
            skip = "destination outside --memar-root"
        elif go_root is not None and go_root != memar_root and target.is_relative_to(go_root):
            skip = "destination inside the Go root; transfer never writes into it"
        dest_relative = target.relative_to(memar_root).as_posix() if target.is_relative_to(memar_root) else str(target)
        for excluded in excludes:
            clean = excluded.strip("/")
            if dest_relative == clean or dest_relative.startswith(clean + "/") or relative == clean or relative.startswith(clean + "/"):
                skip = skip or f"excluded by --exclude {excluded}"
        items.append(TransferItem(path, label, relative, module, target, dest_relative, skip))
    return items


def build_transfer_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abstraction_bridge.py transfer",
        description=(
            "Transfer Go source into Khayyam: declarations where a Khayyam form exists, "
            "TODO(go-migrate) residue with the original text elsewhere, and the full Go "
            "file as comments at the end. Dry by default."
        ),
    )
    parser.add_argument("source", help="a .go file, a package directory, or with --recursive a tree")
    parser.add_argument("dest", help="a .kh file or a directory")
    parser.add_argument("--memar-root", help="repository that receives the .kh files (default: current directory)")
    parser.add_argument("--go-root", help="Go module root (holds go.mod); resolves imports and archive names")
    parser.add_argument("--recursive", action="store_true", help="walk SOURCE and place files by CORPUS_MODULE_ROOTS")
    parser.add_argument("--exclude", action="append", default=[], help="destination or source prefix to leave alone (repeatable)")
    parser.add_argument("--write", action="store_true", help="write; without it nothing is written")
    parser.add_argument("--no-frontend", action="store_true", help="skip the Khayyam frontend check")
    parser.add_argument(
        "--source-only",
        action="store_true",
        help="add only the go-source block (and the residue marker) to an existing destination, e.g. a hand port",
    )
    parser.add_argument("--print", action="store_true", help="print every destination that would change")
    parser.add_argument("--verify", action="store_true", help="only check each destination carries its Go source block")
    parser.add_argument("--report", help="write the machine readable report as JSON")
    return parser


def transfer_main(argv: Sequence[str]) -> int:
    arguments = build_transfer_parser().parse_args(list(argv))
    if hasattr(sys.stdout, "reconfigure"):
        # Go comments carry §, Persian and math symbols; a console code page must not lose them.
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    memar_root = Path(arguments.memar_root or ".").resolve()
    go_root = Path(arguments.go_root).resolve() if arguments.go_root else None
    items = transfer_items(
        Path(arguments.source), Path(arguments.dest), memar_root, go_root, arguments.recursive, arguments.exclude
    )
    if arguments.verify:
        problems = 0
        results = []
        for item in items:
            if item.skip:
                results.append({"source": item.label, "dest": item.dest_relative, "state": f"skipped: {item.skip}"})
                continue
            raw = item.source.read_bytes()
            if not re.search(r"(?m)^package\s+\w+", raw.decode("utf-8", errors="replace")):
                results.append(
                    {"source": item.label, "dest": item.dest_relative, "state": "skipped: not a Go source: no package clause"}
                )
                continue
            text = item.dest.read_text(encoding="utf-8") if item.dest.exists() else ""
            problem = verify_source_block(text.replace("\r\n", "\n"), item.label, raw)
            problems += problem is not None
            results.append({"source": item.label, "dest": item.dest_relative, "state": problem or "ok"})
        if arguments.report:
            Path(arguments.report).write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        for result in results:
            if result["state"] != "ok":
                print(f"{result['source']} -> {result['dest']}: {result['state']}")
        verified = sum(result["state"] == "ok" for result in results)
        skipped = len(results) - verified - problems
        print(f"verified {verified} of {len(results)}  skipped {skipped}  problems {problems}")
        return 1 if problems else 0
    transfer = GoTransfer(
        items, memar_root, go_root, frontend=not arguments.no_frontend, source_only=arguments.source_only
    )
    try:
        summary = transfer.run(write=arguments.write)
    except (BridgeFailure, SourceFailure) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if arguments.print:
        for dest, text in sorted(transfer.outputs.items()):
            if text != transfer.texts.get(dest):
                sys.stdout.write(f"===== {dest} ({transfer.files.get(dest)})\n{text}")
    if arguments.report:
        Path(arguments.report).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"mode {summary['mode']}  sources {summary['sources']}  frontend rounds {summary['frontend_rounds']}")
    print("files " + "  ".join(f"{key} {value}" for key, value in sorted(summary["files"].items())))
    print("constructs " + "  ".join(f"{key} {value}" for key, value in sorted(summary["constructs"].items())))
    print(f"todo blocks added {summary['todo_blocks_added']}  demoted {len(summary['demoted'])}")
    for relative, change in summary["dependents_changed"].items():
        print(f"untouched {relative}: frontend {change['before']} -> {change['after']}")
    return 0
