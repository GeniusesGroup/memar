"""`reemit`: re-emit the archived Go abstraction corpus into the Khayyam protocol files
it was first ported into.

This time with the Go doc comment of every declaration, method and referenced type
carried over verbatim, line by line, directly above what it documents; with
module-qualified, self-describing declaration names; with generic interfaces
emitted as plain non-generic abstractions, their type parameters resolved only
against concrete instantiations the corpus itself uses; and with `in` imports that
name a real file in the archive.

It only rewrites protocol files that already exist, and it never rewrites one whose
declarations or comments the Go corpus does not carry: such a file is reported as
guarded and left for its owner."""

import re
import argparse
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Sequence

from failures import SourceFailure
from comments import (
    CommentIndex,
    extract_comment_blocks,
    render_comment,
    strip_comments,
)
from names import (
    FIXED_KHAYYAM_DECLARATIONS,
    PRE_EXISTING_KHAYYAM,
    PRIMITIVE_KHAYYAM_TYPES,
    UNMAPPED_PRIMITIVE_CAPSULES,
    concept_forms,
    field_accessor_options,
    field_holds_its_concept,
    identity_carried,
    kebab_name,
    module_identity,
    normalize_module,
    pascal_segment,
    qualified_by_module,
    qualify_name,
    repeats,
    split_field_name,
    strip_protocol,
)
from go_source import (
    GoInterface,
    GoMethod,
    GoSource,
    GoType,
    InterfaceEntry,
    Parameter,
    has_unmappable_type,
    lex_source,
    parse_go_source,
    top_level_value_names,
    type_arguments,
    type_name,
)
from khayyam_source import (
    KEYWORDS,
    KhayyamParameter,
    khayyam_uri,
    render_khayyam_method,
)
from go_source_block import preserve_transfer_text


# ---------------------------------------------------------------------------
# Corpus port
#
# `reemit` re-emits the archived Go abstraction corpus into the Khayyam
# protocol files it was first ported into, this time with:
#
#   * the Go doc comment of every declaration, method and referenced type
#     carried over verbatim, line by line, directly above what it documents;
#   * module-qualified, self-describing declaration names;
#   * generic interfaces emitted as plain non-generic abstractions, with type
#     parameters resolved only against concrete instantiations the corpus
#     itself uses;
#   * `in` imports that name a real file in the archive.
# ---------------------------------------------------------------------------

CORPUS_LICENSE = "/* For license and copyright information please see the LEGAL file in the code repository */"
CORPUS_LICENSE_TEXT = "For license and copyright information"


def licence_blocks(source: GoSource) -> int:
    return sum(
        1
        for block in source.comments
        if block.lines and block.lines[0].strip().startswith(CORPUS_LICENSE_TEXT)
    )


@dataclass
class CorpusDecl:
    key: str
    name: str
    module: str
    kind: str
    generic: bool
    type_params: list[str]
    doc: list[str]
    path: str
    line: int
    source_stem: str
    interface: GoInterface | None = None
    declaration: GoType | None = None
    methods: list[GoMethod] = field(default_factory=list)
    output: str = ""
    output_file: str | None = None
    fixed: bool = False
    constraint: bool = False

    @property
    def is_interface(self) -> bool:
        return self.interface is not None


@dataclass
class CorpusTarget:
    path: Path
    relative: str
    module: str
    stem: str
    source: str
    baseline: list[str]
    roots: list[CorpusDecl] = field(default_factory=list)
    local_names: set[str] = field(default_factory=set)
    methods: set[str] = field(default_factory=set)
    selected: bool = True


@dataclass(frozen=True)
class CorpusScope:
    """Where a type is written: the package it resolves in and where from."""

    module: str
    site: str
    type_params: tuple[str, ...] = ()
    owner: str = ""


@dataclass
class CorpusRef:
    kind: str
    name: str = ""
    arguments: tuple["CorpusRef", ...] = ()
    reason: str = ""

    @property
    def ok(self) -> bool:
        return self.kind in {"primitive", "decl", "instantiation"}

    def describe(self) -> str:
        if self.kind == "primitive":
            return self.name
        if self.kind == "decl":
            return self.name
        if self.kind == "instantiation":
            inner = ", ".join(argument.describe() for argument in self.arguments)
            return f"{self.name}[{inner}]"
        return self.reason or "unresolved"


@dataclass
class CorpusInstantiation:
    decl: CorpusDecl
    arguments: list[CorpusRef]
    name: str = ""
    home: str | None = None
    signature: str = ""
    type_owned: bool = False


class CorpusNameTable:
    """Names every ported declaration the way the archive reads.

    A name is qualified only when it has to be. It is kept bare when the
    pre-existing archive files or a method of the corpus already own that
    spelling, when exactly one ported module declares it, or when it already
    carries the identity of its own module. Otherwise the module's own identity
    -- its last non-`protocol` segment, PascalCased -- is prefixed. When that
    identity cannot separate two declarations that both want the same name,
    nothing is invented: the archive's own spelling is kept and the case is
    reported for the owner.
    """

    def __init__(
        self,
        reserved: set[str],
        method_names: set[str],
        modules_of: dict[str, set[str]],
        current_names: dict[str, str],
    ) -> None:
        self.reserved = set(reserved)
        self.method_names = set(method_names)
        self.modules_of = modules_of
        self.current_names = current_names
        self.taken: dict[str, str] = {}
        self.holder_module: dict[str, str] = {}
        self.unrenderable: set[str] = set()
        self.output: dict[str, str] = {}
        self.renamed: list[tuple[str, str, str]] = []
        self.reserved_names: list[tuple[str, str]] = []
        self.unresolved: list[dict[str, object]] = []

    def target(self, decl: CorpusDecl) -> tuple[str, str]:
        """The name the rule asks for, and why."""
        bare = decl.name
        if bare in self.reserved or bare in self.method_names:
            return self.current_names.get(decl.key, bare), "reserved"
        if len(self.modules_of.get(bare, ())) <= 1 and not self.field_needs_qualifier(decl):
            return bare, "unique"
        identities = module_identity(decl.module)
        identity = pascal_segment(identities[0]) if identities else ""
        if not identity or identity_carried(identity, bare):
            return bare, "carries"
        return qualify_name(identity, bare), "qualified"

    def field_needs_qualifier(self, decl: CorpusDecl) -> bool:
        """True when `decl` is `Field_<X>` and the short name would not say
        which X it holds: more than one module declares X or its leading term,
        or an accessor returns what the module identity names rather than X
        (`Field_Access` in `process/time` returning a `Time`)."""
        parts = split_field_name(decl.name)
        if parts is None or parts[0]:
            return False
        concept = parts[1]
        terms = [concept, concept.split("_", 1)[0]] if "_" in concept else [concept]
        if any(len(self.modules_of.get(form, ())) > 1 for term in terms for form in concept_forms(term)):
            return True
        entries = decl.interface.entries if decl.interface is not None else []
        values = [type_name(result.type_text) for entry in entries for result in entry.results]
        values = [value for value in values if value.lower() != "error"]
        if field_holds_its_concept(concept, values):
            return False
        identities = module_identity(decl.module)
        identity = pascal_segment(identities[0]) if identities else ""
        return bool(identity) and any(repeats(identity, value) for value in values)

    def assign(self, decl: CorpusDecl) -> str:
        if decl.key in self.output:
            return self.output[decl.key]
        name, reason = self.target(decl)
        owner = self.taken.get(name)
        if owner is not None and owner != decl.key:
            self.unresolved.append(
                {
                    "name": decl.name,
                    "wants": name,
                    "module": decl.module,
                    "modules": sorted(self.modules_of.get(decl.name, ())),
                    "holder_module": self.holder_module.get(owner, owner),
                }
            )
            kept = self.current_names.get(decl.key)
            if kept is not None and self.taken.get(kept) in (None, decl.key):
                name = kept
                reason = "unresolved"
            else:
                # The archive's own spelling is held too. The declaration keeps
                # the name for the report, no name is taken from the holder, and
                # the file that would declare it twice is left unwritten.
                self.unrenderable.add(decl.key)
                self.output[decl.key] = name
                decl.output = name
                return name
        self.taken[name] = decl.key
        self.holder_module[decl.key] = decl.module
        self.output[decl.key] = name
        decl.output = name
        if reason == "reserved":
            self.reserved_names.append((decl.module, name))
        if name != decl.name:
            self.renamed.append((decl.module, decl.name, name))
        return name

    def name_of(self, decl: CorpusDecl) -> str:
        return self.output.get(decl.key, decl.name)


CORPUS_AB_PATTERN = re.compile(r"^tp\s+([A-Za-z_][A-Za-z0-9_]*)\s+ab\b", re.M)
CORPUS_MT_PATTERN = re.compile(r"^tp\s+([A-Za-z_][A-Za-z0-9_]*)\s+mt\b", re.M)
CORPUS_DECLARED_PATTERN = re.compile(r"^tp\s+([A-Za-z_][A-Za-z0-9_]*)\s+(ab|mt|cp|sc|in)\b", re.M)
CORPUS_KIND_PATTERN = re.compile(r"^[ \t]*tp[ \t]+(\S+)[ \t]+(ab|mt|cp|sc|vr)\b", re.M)


def comment_lines(source: str) -> list[str]:
    """The non-empty text lines of every comment in `source`."""
    return [
        line.strip()
        for block in extract_comment_blocks(source)
        for line in block.lines
        if line.strip()
    ]


def content_hazards(before_text: str, after_text: str) -> list[str]:
    """What replacing `before_text` with `after_text` would destroy: the
    guard `reemit` and `transfer` both write through."""
    hazards: list[str] = []
    before = [kind for _, kind in CORPUS_KIND_PATTERN.findall(strip_comments(before_text))]
    after = [kind for _, kind in CORPUS_KIND_PATTERN.findall(strip_comments(after_text))]
    if before and not after:
        hazards.append("no Go declaration maps to this file, so every declaration would be removed")
    foreign = sorted({kind for kind in before if kind not in {"ab", "mt"}})
    if foreign:
        hazards.append(
            "holds {} declarations the port never emits".format(
                ", ".join(f"`{kind}`" for kind in foreign)
            )
        )
    for kind in ("ab", "mt"):
        dropped = before.count(kind) - after.count(kind)
        if dropped > 0:
            hazards.append(f"would drop {dropped} `{kind}` declaration(s)")
    kept = {" ".join(line.split()) for line in comment_lines(after_text)}
    lost = [
        line
        for line in (" ".join(text.split()) for text in comment_lines(before_text))
        if line not in kept
    ]
    if lost:
        hazards.append(f"would drop {len(lost)} comment line(s), first {lost[0][:80]!r}")
    return hazards


class CorpusPort:
    """Re-emits the archived Go abstraction corpus as Khayyam abstractions."""

    def __init__(
        self,
        go_root: Path,
        memar_root: Path,
        excludes: Sequence[str] = (),
        only: Sequence[str] = (),
    ) -> None:
        self.go_root = go_root
        self.memar_root = memar_root
        self.excludes = set(excludes)
        self.only = set(only)
        self.module_name = self.read_module_name()
        self.sources: dict[str, GoSource] = {}
        self.declarations: dict[str, CorpusDecl] = {}
        self.by_name: dict[str, list[CorpusDecl]] = {}
        self.parse_failures: list[str] = []
        self.method_owners: list[str] = []
        self.targets: list[CorpusTarget] = []
        self.reserved: set[str] = set(KEYWORDS)
        self.pre_existing_names: dict[str, set[str]] = {}
        self.wanted: dict[str, CorpusDecl] = {}
        self.claimed: dict[str, list[tuple[CorpusTarget, str]]] = {}
        self.instantiations: dict[str, list[CorpusInstantiation]] = {}
        self.instantiation_index: dict[str, CorpusInstantiation] = {}
        self.scanned_instantiations: dict[str, list[tuple[str, list[str]]]] = {}
        self.names: CorpusNameTable | None = None
        self.named: dict[str, CorpusDecl] = {}
        self.declared_names: set[str] = set()
        self.member_names: set[str] = set()
        self.member_signatures: dict[str, set[tuple]] = {}
        self.references: list[tuple[str, str, str]] = []
        self.omissions: list[dict[str, str]] = []
        self.unmatched_baseline: list[tuple[str, str]] = []
        self.comment_blocks = 0
        self.comment_blocks_emitted = 0
        self.comment_lines_emitted = 0
        self.comment_floating: list[tuple[str, int, str]] = []
        self.method_count = 0
        self.method_emitted = 0
        self.method_omitted: list[dict[str, str]] = []
        self.written: list[str] = []
        self.unchanged: list[str] = []
        self.guarded: list[str] = []
        self.constants: list[tuple[str, str, list[str]]] = []

    # -- loading ------------------------------------------------------------

    def read_module_name(self) -> str:
        go_mod = self.go_root / "go.mod"
        if not go_mod.exists():
            return ""
        for line in go_mod.read_text(encoding="utf-8").splitlines():
            match = re.match(r"\s*module\s+(\S+)", line)
            if match:
                return match.group(1)
        return ""

    def load_sources(self) -> None:
        for path in sorted(self.go_root.rglob("*.go")):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as error:
                self.parse_failures.append(f"{path}: {error}")
                continue
            try:
                self.sources[str(path)] = parse_go_source(str(path), text)
            except SourceFailure as error:
                self.parse_failures.append(str(error))
                continue
            tokens = lex_source(text, True)
            relative = path.relative_to(self.go_root).as_posix()
            for keyword in ("const", "var"):
                names = top_level_value_names(tokens, keyword)
                if names:
                    self.constants.append((relative, keyword, names))

    def build_declarations(self) -> None:
        for path in sorted(self.sources):
            source = self.sources[path]
            relative = Path(path).relative_to(self.go_root)
            module = normalize_module(
                relative.parent.as_posix() if relative.parent != Path(".") else ""
            )
            stem = relative.stem
            interfaces = {interface.name: interface for interface in source.interfaces}
            for declaration in source.types:
                interface = interfaces.get(declaration.name) if declaration.kind == "interface" else None
                constraint = False
                if interface is not None:
                    constraint = not interface.entries and any(
                        composition.constraint for composition in interface.compositions
                    )
                key = f"{module}\x00{declaration.name}"
                if key in self.declarations:
                    continue
                corpus = CorpusDecl(
                    key=key,
                    name=declaration.name,
                    module=module,
                    kind="constraint" if constraint else ("interface" if interface else declaration.kind),
                    generic=declaration.generic,
                    type_params=list(declaration.type_params),
                    doc=list(declaration.doc),
                    path=path,
                    line=declaration.line,
                    source_stem=stem,
                    interface=interface,
                    declaration=declaration,
                )
                self.declarations[key] = corpus
                self.by_name.setdefault(declaration.name, []).append(corpus)
            for method in source.methods:
                owner = self.declarations.get(f"{module}\x00{method.owner}")
                if owner is None or owner.is_interface:
                    self.method_owners.append(f"{path}:{method.line}: {method.owner}.{method.name}")
                    continue
                if any(
                    existing.name == method.name
                    and [parameter.type_text for parameter in existing.parameters]
                    == [parameter.type_text for parameter in method.parameters]
                    for existing in owner.methods
                ):
                    continue
                owner.methods.append(method)

    def reserve_pre_existing(self) -> None:
        for relative in PRE_EXISTING_KHAYYAM:
            path = self.memar_root / relative
            if not path.exists():
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            code = strip_comments(text)
            self.reserved.update(
                token.text for token in lex_source(code, False) if token.kind == "ident"
            )
            self.pre_existing_names[relative] = {
                match.group(1) for match in CORPUS_DECLARED_PATTERN.finditer(code)
            }

    def load_targets(self) -> None:
        modules = self.memar_root / "modules"
        for path in sorted(modules.rglob("*.kh")):
            relative = path.relative_to(self.memar_root).as_posix()
            if "/protocol/" not in f"/{relative}":
                continue
            if relative in PRE_EXISTING_KHAYYAM:
                continue
            # --exclude and --only narrow what is written, never where a
            # declaration is placed: a file left out of placement would push
            # its declarations into the files that remain.
            selected = relative not in self.excludes and not any(
                relative.startswith(excluded) or f"/{relative}".endswith(f"/{excluded}")
                for excluded in self.excludes
                if not excluded.endswith(".kh")
            )
            if self.only and not any(relative.endswith(item) for item in self.only):
                selected = False
            text = path.read_text(encoding="utf-8", errors="replace")
            target = CorpusTarget(
                path=path,
                relative=relative,
                module=path.parent.relative_to(modules).as_posix(),
                stem=path.stem,
                source=text,
                baseline=list(dict.fromkeys(CORPUS_AB_PATTERN.findall(text))),
                methods=set(CORPUS_MT_PATTERN.findall(text)),
                selected=selected,
            )
            self.targets.append(target)

    def scan_instantiations(self) -> None:
        """Every `Name[arguments]` in the corpus, with the file it appears in."""
        pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\[([^\[\]]*)\]")
        for path in sorted(self.go_root.rglob("*.go")):
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            code = strip_comments(text)
            for match in pattern.finditer(code):
                name = match.group(1)
                arguments = [part.strip() for part in match.group(2).split(",") if part.strip()]
                if not arguments:
                    continue
                if not all(re.fullmatch(r"[A-Za-z0-9_.*\[\]]+", part) for part in arguments):
                    continue
                for decl in self.by_name.get(name, ()):
                    if decl.generic:
                        self.scanned_instantiations.setdefault(decl.key, []).append(
                            (str(path), arguments)
                        )

    # -- placement ----------------------------------------------------------

    def claim_key(self, decl: CorpusDecl, target: CorpusTarget, declares: bool) -> tuple:
        declared = 0 if (declares and decl.name in target.baseline) else 1
        stem_rank = 0 if target.stem == decl.source_stem else 1
        return (declared, self.module_rank(decl, target), stem_rank, target.relative)

    def module_rank(self, decl: CorpusDecl, target: CorpusTarget) -> int:
        if target.module == decl.module:
            return 0
        if strip_protocol(target.module) == strip_protocol(decl.module):
            return 1
        if target.module.split("/")[0] == decl.module.split("/")[0]:
            return 2
        return 3

    def home_for(self, decl: CorpusDecl) -> CorpusTarget | None:
        """The protocol file that declares `decl`.

        The archive's own layout wins when it filed the declaration in its own
        module; otherwise the file of that module whose name is closest to the
        declaration — its kebab name, then its Go file, then a name that extends
        its Go file. Never a file of another module, and never dependent on
        anything but the Go corpus and the set of protocol files, so re-running
        cannot move a declaration.
        """
        claimants = [
            (self.claim_key(decl, target, True), index, target)
            for index, (target, _) in enumerate(self.claimed.get(decl.key, []))
            if self.module_rank(decl, target) <= 1
        ]
        if claimants:
            return min(claimants, key=lambda entry: (entry[0], entry[1]))[2]
        kebab = kebab_name(decl.name)
        candidates = [
            target for target in self.targets if self.module_rank(decl, target) <= 1
        ]
        if not candidates:
            return None
        return min(
            candidates,
            key=lambda target: (
                self.module_rank(decl, target),
                0 if target.stem == kebab else 1,
                0 if target.stem == decl.source_stem else 1,
                0 if target.stem.startswith(decl.source_stem) else 1,
                target.relative,
            ),
        )

    def want(self, decl: CorpusDecl) -> CorpusDecl:
        return self.wanted.setdefault(decl.key, decl)

    def claim_baselines(self) -> None:
        """Seed the roots from the abstraction names the archive already holds.

        A name is matched to the Go declaration that produced it in three
        steps, so the archive is read whatever qualifier its names carry: the Go
        name itself, the name this port gives the declaration, and finally a
        name the archive put a module qualifier in front of the Go name. A Go
        name is claimed once, longest match first, so a name like
        `Boolean_Math_Boolean` cannot be mistaken for the declaration `Boolean`.
        """
        homed = [
            decl
            for decl in self.declarations.values()
            if decl.output_file is not None and decl.kind != "constraint"
        ]

        def qualified(decl: CorpusDecl, name: str) -> bool:
            """True when `name` is the Go name behind a module identity prefix."""
            return name != decl.name and qualified_by_module(decl.name, name, decl.module)

        for target in self.targets:
            taken: set[str] = set()
            # three passes, so a loose match never takes a name an exact one owns
            for tier in ("go", "canonical", "qualified"):
                for name in target.baseline:
                    candidates: list[CorpusDecl] = []
                    if tier == "go":
                        candidates = [
                            candidate
                            for candidate in self.by_name.get(name, [])
                            if candidate.kind != "constraint"
                        ]
                    elif tier == "canonical":
                        candidates = [
                            decl
                            for decl in self.declarations.values()
                            if decl.output == name
                            and decl.kind != "constraint"
                            and decl.name not in taken
                        ]
                    else:
                        candidates = [
                            decl
                            for decl in homed
                            if decl.name not in taken and qualified(decl, name)
                        ]
                    if not candidates:
                        continue
                    decl = min(
                        candidates,
                        key=lambda candidate: (
                            self.claim_key(candidate, target, True),
                            -len(candidate.name),
                            candidate.path,
                            candidate.line,
                        ),
                    )
                    taken.add(decl.name)
                    self.claimed.setdefault(decl.key, []).append((target, name))
                    self.want(decl)
            for name in target.baseline:
                if not any(name == claimed for _, claimed in self.claimed_names(target)):
                    self.unmatched_baseline.append((target.relative, name))

    def claimed_names(self, target: CorpusTarget) -> list[tuple[CorpusTarget, str]]:
        return [
            (held, name)
            for held, name in (
                (claims[0][0], claims[0][1]) for claims in self.claimed.values()
            )
            if held is target
        ]

    def attach_roots(self) -> None:
        by_relative = {target.relative: target for target in self.targets}
        for target in self.targets:
            target.roots = []
        for decl in sorted(
            self.wanted.values(), key=lambda item: (item.path, item.line, item.name)
        ):
            target = by_relative.get(decl.output_file or "")
            if target is not None and decl not in target.roots:
                target.roots.append(decl)

    def assign_names(self) -> None:
        """Name every declaration the port emits.

        A bare name is unique when one ported module declares it, so the test
        runs over the declarations the port actually emits -- the roots of a
        target file plus everything they reference. The first call, before the
        roots are known, is a provisional pass whose only job is to give the
        archive's own spellings something to match against.
        """
        self.named = {
            key: decl
            for key, decl in self.declarations.items()
            if decl.output_file is not None and decl.kind != "constraint"
        }
        emitted = self.wanted or self.named
        modules_of: dict[str, set[str]] = {}
        for decl in emitted.values():
            modules_of.setdefault(decl.name, set()).add(decl.module)
        current_names = {
            decl.key: name
            for decl in self.named.values()
            for _, name in self.claimed.get(decl.key, [])
        }
        method_names: set[str] = set()
        for target in self.targets:
            method_names |= target.methods
        self.names = CorpusNameTable(
            set(self.reserved), method_names, modules_of, current_names
        )
        ordered = sorted(
            emitted.values(),
            key=lambda decl: (decl.module, decl.path, decl.line, decl.name),
        )
        for decl in ordered:
            self.names.assign(decl)

    # -- reference resolution ----------------------------------------------

    def import_module(self, import_path: str) -> str:
        prefix = self.module_name
        if prefix and import_path.startswith(prefix + "/"):
            return import_path[len(prefix) + 1 :]
        if prefix and import_path == prefix:
            return ""
        return import_path

    def reference_to(self, decl: CorpusDecl, text: str) -> CorpusRef:
        if decl.kind == "constraint":
            return CorpusRef("unresolved", reason=f"Go {decl.module}.{decl.name} is a type constraint")
        self.want(decl)
        self.references.append((decl.path, decl.line, text))
        return CorpusRef("decl", name=decl.key)

    def register_instantiation(
        self, decl: CorpusDecl, arguments: Sequence[CorpusRef]
    ) -> CorpusRef:
        signature = "{}({})".format(
            decl.key, ",".join(argument.describe() for argument in arguments)
        )
        if signature not in self.instantiation_index:
            instantiation = CorpusInstantiation(
                decl=decl, arguments=list(arguments), signature=signature
            )
            self.instantiation_index[signature] = instantiation
            self.instantiations.setdefault(decl.key, []).append(instantiation)
        return CorpusRef("instantiation", name=signature, arguments=tuple(arguments))

    def scope_of(self, path: str) -> str:
        relative = Path(path).relative_to(self.go_root)
        return normalize_module(
            relative.parent.as_posix() if relative.parent != Path(".") else ""
        )

    def resolve(
        self,
        text: str,
        scope: CorpusScope,
        binding: dict[str, CorpusRef],
        depth: int = 0,
    ) -> CorpusRef:
        value = " ".join(text.split())
        if not value:
            return CorpusRef("unresolved", reason="empty type")
        if value in binding:
            return binding[value]
        if depth > 6:
            return CorpusRef("unresolved", reason=f"type nesting too deep at {value!r}")
        if value in scope.type_params and value not in binding:
            return CorpusRef(
                "unresolved",
                reason=(
                    f"type parameter {value!r} of {scope.owner or scope.module} "
                    "is not bound at this level"
                ),
            )
        if value in PRIMITIVE_KHAYYAM_TYPES:
            return CorpusRef("primitive", name=PRIMITIVE_KHAYYAM_TYPES[value])
        if value in UNMAPPED_PRIMITIVE_CAPSULES:
            return CorpusRef(
                "unresolved",
                reason=(
                    f"Go {value!r} needs {UNMAPPED_PRIMITIVE_CAPSULES[value]}, "
                    "which the archive does not have"
                ),
            )
        if value in {"any", "interface", "interface{}", "comparable"}:
            return CorpusRef("unresolved", reason=f"Go {value!r} has no Khayyam form")
        if "[" in value and value.endswith("]") and not value.startswith("["):
            base, _, rest = value.partition("[")
            arguments = type_arguments(lex_source(rest[:-1], True)[:-1])
            target = self.resolve(base, scope, binding, depth + 1)
            if target.kind != "decl":
                return CorpusRef("unresolved", reason=f"{value!r} does not instantiate a declaration")
            instantiated = self.declarations[target.name]
            if not instantiated.generic:
                return CorpusRef(
                    "unresolved", reason=f"Go {instantiated.module}.{instantiated.name} is not generic"
                )
            resolved = [
                self.resolve(argument, scope, binding, depth + 1) for argument in arguments
            ]
            for argument in resolved:
                if not argument.ok:
                    return CorpusRef("unresolved", reason=argument.reason)
            return self.register_instantiation(instantiated, resolved)
        unmappable = has_unmappable_type(lex_source(value, True)[:-1])
        if unmappable:
            return CorpusRef("unresolved", reason=f"Go {unmappable} type {value!r}")
        if "." in value:
            alias, _, name = value.partition(".")
            if "." in name:
                return CorpusRef("unresolved", reason=f"invalid qualified type {value!r}")
            source = self.sources.get(scope.site)
            import_path = (source.imports.get(alias) if source else None) or alias
            module = normalize_module(self.import_module(import_path))
            referenced = self.declarations.get(f"{module}\x00{name}")
            if referenced is None:
                return CorpusRef("unresolved", reason=f"{import_path} declares no {name}")
            return self.reference_to(referenced, value)
        referenced = self.declarations.get(f"{scope.module}\x00{value}")
        if referenced is None:
            return CorpusRef(
                "unresolved", reason=f"Go package {scope.module} declares no {value}"
            )
        return self.reference_to(referenced, value)

    def collect_instantiations(self) -> None:
        for key, sites in sorted(self.scanned_instantiations.items()):
            decl = self.wanted.get(key)
            if decl is None or not decl.generic:
                continue
            for site, arguments in sites:
                if site == decl.path:
                    continue
                scope = CorpusScope(self.scope_of(site), site)
                resolved: list[CorpusRef] = []
                failure = ""
                for argument in arguments:
                    reference = self.resolve(argument, scope, {})
                    if not reference.ok:
                        failure = reference.reason
                        break
                    resolved.append(reference)
                if failure:
                    self.omissions.append(
                        {
                            "kind": "instantiation-without-concrete-type",
                            "site": f"{decl.module}.{decl.name}[{', '.join(arguments)}]",
                            "detail": f"{Path(site).relative_to(self.go_root).as_posix()}: {failure}",
                        }
                    )
                    continue
                self.register_instantiation(decl, resolved)

    def reference_output_file(self, reference: CorpusRef) -> str | None:
        if reference.kind == "primitive":
            decl = self.primitive_declaration(reference.name)
            return decl.output_file if decl else None
        if reference.kind == "decl":
            decl = self.declarations.get(reference.name)
            return decl.output_file if decl and decl.output_file else None
        return None

    def instantiation_is_type_owned(self, instantiation: CorpusInstantiation) -> bool:
        decl = instantiation.decl
        return (
            len(decl.type_params) == 1
            and len(instantiation.arguments) == 1
            and self.reference_output_file(instantiation.arguments[0]) is not None
        )

    def instantiation_owner_file(self, instantiation: CorpusInstantiation) -> str | None:
        if not self.instantiation_is_type_owned(instantiation):
            return None
        return self.reference_output_file(instantiation.arguments[0])

    def instantiation_owner_name(self, instantiation: CorpusInstantiation) -> str | None:
        reference = instantiation.arguments[0]
        if reference.kind == "primitive":
            return PRIMITIVE_KHAYYAM_TYPES.get(reference.name)
        if reference.kind == "decl":
            decl = self.declarations.get(reference.name)
            if decl is None:
                return None
            return self.names.name_of(decl) if self.names else decl.name
        return None

    def argument_name(self, reference: CorpusRef) -> str:
        if reference.kind == "primitive":
            return reference.name
        if reference.kind == "decl":
            decl = self.declarations[reference.name]
            if decl.key not in self.wanted:
                self.want(decl)
            return self.names.name_of(decl) if self.names else decl.name
        instantiation = self.instantiation_index[reference.name]
        if not instantiation.name:
            parts = [self.argument_name(argument) for argument in instantiation.arguments]
            instantiation.name = "_".join([instantiation.decl.output, *parts])
        return instantiation.name

    def name_instantiations(self) -> None:
        for signature in sorted(self.instantiation_index):
            instantiation = self.instantiation_index[signature]
            parts = [self.argument_name(argument) for argument in instantiation.arguments]
            instantiation.name = "_".join([instantiation.decl.output, *parts])
            instantiation.type_owned = self.instantiation_is_type_owned(instantiation)
            instantiation.home = (
                self.instantiation_owner_file(instantiation) or instantiation.decl.output_file
            )
        self.declared_names = {decl.output for decl in self.named.values()}
        self.declared_names.update(
            instantiation.name
            for instantiation in self.instantiation_index.values()
            if not instantiation.type_owned
        )
        self.member_names = set()
        self.member_signatures = {}

    def primitive_declaration(self, name: str) -> CorpusDecl | None:
        for (module, declared), fixed in FIXED_KHAYYAM_DECLARATIONS.items():
            if fixed != name:
                continue
            decl = self.declarations.get(f"{module}\x00{declared}")
            if decl is not None:
                self.want(decl)
                return decl
        return None

    def materialize(
        self,
        reference: CorpusRef,
        target: CorpusTarget,
        imports: dict[str, str],
        local: set[str],
    ) -> str | None:
        """The emitted name of `reference`, or None when it cannot be carried."""
        if reference.kind == "primitive":
            decl = self.primitive_declaration(reference.name)
            if decl is None or decl.output_file is None:
                self.omissions.append(
                    {
                        "kind": "primitive-without-capsule",
                        "site": f"{target.relative} {reference.name}",
                        "detail": f"no Khayyam file declares {reference.name}",
                    }
                )
                return None
            name = self.names.name_of(decl) if self.names else reference.name
            home = decl.output_file
        elif reference.kind == "decl":
            decl = self.declarations[reference.name]
            if decl.output_file is None:
                self.omissions.append(
                    {
                        "kind": "reference-without-home",
                        "site": f"{target.relative} {decl.module}.{decl.name}",
                        "detail": "no protocol file in the first port declared it",
                    }
                )
                return None
            name = self.names.name_of(decl) if self.names else decl.name
            home = decl.output_file
        else:
            instantiation = self.instantiation_index[reference.name]
            decl = instantiation.decl
            if instantiation.type_owned:
                if decl.output_file is None:
                    self.omissions.append(
                        {
                            "kind": "instantiation-without-home",
                            "site": f"{target.relative} {instantiation.signature}",
                            "detail": "the generic declaration it comes from has no protocol file",
                        }
                    )
                    return None
                name = decl.output
                home = decl.output_file
            elif instantiation.home is None:
                self.omissions.append(
                    {
                        "kind": "instantiation-without-home",
                        "site": f"{target.relative} {instantiation.signature}",
                        "detail": "the generic declaration it comes from has no protocol file",
                    }
                )
                return None
            else:
                name = instantiation.name
                home = instantiation.home
        if home in self.pre_existing_names and name not in self.pre_existing_names[home]:
            self.omissions.append(
                {
                    "kind": "reference-into-pre-existing-file",
                    "site": f"{target.relative} {name}",
                    "detail": f"{home} declares {sorted(self.pre_existing_names[home])}, not {name}",
                }
            )
            return None
        if home == target.relative:
            local.add(name)
        else:
            imports[name] = khayyam_uri(home)
        return name

    # -- members ------------------------------------------------------------

    def convert_parameters(
        self,
        decl: CorpusDecl,
        parameters: Sequence[Parameter],
        binding: dict[str, CorpusRef],
        site: str,
        result: bool,
    ) -> list[KhayyamParameter] | None:
        converted: list[KhayyamParameter] = []
        used: set[str] = set()
        scope = CorpusScope(
            self.scope_of(site), site, tuple(decl.type_params), f"{decl.module}.{decl.name}"
        )
        for index, parameter in enumerate(parameters):
            if parameter.variadic:
                return None
            name = parameter.name
            if not name or name == "_":
                name = f"{'result' if result else 'arg'}{index}"
            if name in KEYWORDS:
                # `mt`, `in`, `ab`, ... are Khayyam keywords: a Go parameter
                # keeps its name with a trailing underscore.
                name = f"{name}_"
            if name in used:
                name = f"{name}_{index}"
            used.add(name)
            reference = self.resolve(parameter.type_text, scope, binding)
            if not reference.ok:
                self.member_failure(decl, "type", parameter.type_text, reference.reason)
                return None
            converted.append(KhayyamParameter(name, reference))
        return converted

    def member_failure(self, decl: CorpusDecl, kind: str, text: str, reason: str) -> None:
        self.omissions.append(
            {
                "kind": f"{kind}-not-portable",
                "site": f"{decl.module}.{decl.name} {text}",
                "detail": reason,
            }
        )

    def member_name(
        self,
        decl: CorpusDecl,
        owner: str,
        original: str,
        signature: tuple[tuple[str | None, ...], tuple[str | None, ...]] = ((), ()),
    ) -> str:
        """The name of a method or field accessor of `owner`.

        A method no file imports keeps the bare name: the receiver supplies the
        context, so `tp Start mt (self Timer)` is `Start`, not `Timer_Start` --
        the receiver method names rule, `modules/khayyam/rules/receiver-method-names/`.
        A field abstraction's method never takes its owner's name: when its own
        is a declaration's, or another method's with another signature, it
        takes the next of `field_accessor_options` (`Scheme` -> `URIScheme`).
        Any other method falls back to the owner prefix, then the module
        identity. The last fallback of either is a counter.
        """
        identities = [pascal_segment(identity) for identity in module_identity(decl.module)]
        field_owner = split_field_name(owner) is not None
        if field_owner:
            options = field_accessor_options(owner, original, [text for text in signature[1] if text])
        else:
            options = [
                original,
                f"{owner}_{original}",
                *[f"{owner}_{original}_{identity}" for identity in identities],
            ]
        for candidate in options:
            if candidate in self.declared_names:
                continue
            if field_owner:
                free = self.member_signatures.get(candidate, set()) <= {signature}
            else:
                free = candidate not in self.member_names
            if free:
                self.member_names.add(candidate)
                self.member_signatures.setdefault(candidate, set()).add(signature)
                if candidate != original:
                    self.omissions.append(
                        {
                            "kind": "member-qualified-for-collision",
                            "site": f"{owner}.{original}",
                            "detail": f"`{original}` is already declared; emitted as `{candidate}`",
                        }
                    )
                return candidate
        suffix = 2
        while f"{original}_{suffix}" in self.declared_names or f"{original}_{suffix}" in self.member_names:
            suffix += 1
        candidate = f"{original}_{suffix}"
        self.member_names.add(candidate)
        self.member_signatures.setdefault(candidate, set()).add(signature)
        self.omissions.append(
            {
                "kind": "member-qualified-for-collision",
                "site": f"{owner}.{original}",
                "detail": f"`{original}` is already declared; emitted as `{candidate}`",
            }
        )
        return candidate

    def resolve_members(
        self,
        decl: CorpusDecl,
        owner: str,
        binding: dict[str, CorpusRef],
    ) -> tuple[list[tuple[CorpusRef, list[str]]], list[tuple[InterfaceEntry | GoMethod, list[KhayyamParameter], list[KhayyamParameter]]]]:
        compositions: list[tuple[CorpusRef, list[str]]] = []
        methods: list[tuple[InterfaceEntry | GoMethod, list[KhayyamParameter], list[KhayyamParameter]]] = []
        scope = CorpusScope(
            decl.module, decl.path, tuple(decl.type_params), f"{decl.module}.{decl.name}"
        )
        if decl.interface is not None:
            for composition in decl.interface.compositions:
                if composition.anonymous:
                    self.member_failure(decl, "composition", composition.text, "anonymous interface body")
                    continue
                if composition.constraint:
                    self.member_failure(
                        decl, "composition", composition.text, "type constraint has no abstraction form"
                    )
                    continue
                reference = self.resolve(composition.text, scope, binding)
                if not reference.ok:
                    self.member_failure(decl, "composition", composition.text, reference.reason)
                    continue
                compositions.append((reference, list(composition.doc)))
            for entry in decl.interface.entries:
                if entry.generic:
                    self.member_failure(
                        decl,
                        "method",
                        f"{entry.name}{entry.type_params}",
                        "generic method: its own type parameters are bound per call, not per abstraction",
                    )
                    continue
                influencing = self.convert_parameters(
                    decl, entry.parameters, binding, decl.path, False
                )
                if influencing is None:
                    continue
                influenced = self.convert_parameters(decl, entry.results, binding, decl.path, True)
                if influenced is None:
                    continue
                methods.append((entry, influencing, influenced))
            return compositions, methods
        for method in decl.methods:
            local_binding = dict(binding)
            if method.receiver_arguments and decl.type_params:
                if not (
                    len(method.receiver_arguments) == len(decl.type_params)
                    and all(item in decl.type_params for item in method.receiver_arguments)
                ):
                    method_scope = CorpusScope(
                        self.scope_of(method.path),
                        method.path,
                        tuple(decl.type_params),
                        f"{decl.module}.{decl.name}",
                    )
                    resolved = [
                        self.resolve(item, method_scope, binding)
                        for item in method.receiver_arguments
                    ]
                    if all(item.ok for item in resolved) and len(resolved) == len(decl.type_params):
                        local_binding = {
                            parameter: reference
                            for parameter, reference in zip(decl.type_params, resolved)
                        }
                    else:
                        local_binding = {}
            influencing = self.convert_parameters(
                decl, method.parameters, local_binding, method.path, False
            )
            if influencing is None:
                continue
            influenced = self.convert_parameters(decl, method.results, local_binding, method.path, True)
            if influenced is None:
                continue
            methods.append((method, influencing, influenced))
        return compositions, methods

    # -- rendering ----------------------------------------------------------

    def render_declaration(
        self,
        decl: CorpusDecl,
        target: CorpusTarget,
        binding: dict[str, CorpusRef],
        suffix: str,
        with_doc: bool,
        body: list[str],
        imports: dict[str, str],
        local: set[str],
    ) -> None:
        name = f"{decl.output}{suffix}"
        if body:
            body.append("")
        if with_doc and decl.doc:
            body.extend(render_comment(decl.doc))
            self.comment_blocks_emitted += 1
            self.comment_lines_emitted += len(decl.doc)
        compositions, methods = self.resolve_members(decl, name, binding)
        rendered_compositions: list[tuple[str, list[str]]] = []
        for reference, documentation in compositions:
            materialized = self.materialize(reference, target, imports, local)
            if materialized is None:
                continue
            rendered_compositions.append((materialized, documentation if with_doc else []))
        rendered_methods: list[tuple[str, list[str], list[KhayyamParameter], list[KhayyamParameter]]] = []
        for method, influencing, influenced in methods:
            influencing_types = [
                self.materialize(parameter.type_text, target, imports, local)
                for parameter in influencing
            ]
            influenced_types = [
                self.materialize(parameter.type_text, target, imports, local)
                for parameter in influenced
            ]
            if any(item is None for item in influencing_types) or any(
                item is None for item in influenced_types
            ):
                continue
            member = self.member_name(
                decl, name, method.name, (tuple(influencing_types), tuple(influenced_types))
            )
            rendered_methods.append(
                (
                    member,
                    method.doc if with_doc else [],
                    [
                        KhayyamParameter(parameter.name, resolved)
                        for parameter, resolved in zip(influencing, influencing_types)
                    ],
                    [
                        KhayyamParameter(parameter.name, resolved)
                        for parameter, resolved in zip(influenced, influenced_types)
                    ],
                )
            )
        if rendered_compositions:
            body.append(f"tp {name} ab {{")
            for member, documentation in rendered_compositions:
                if documentation:
                    body.extend(render_comment(documentation))
                    self.comment_blocks_emitted += 1
                    self.comment_lines_emitted += len(documentation)
                body.append(f"    {member}")
            body.append("}")
        else:
            body.append(f"tp {name} ab")
        for member, documentation, influencing, influenced in rendered_methods:
            if documentation:
                body.extend(render_comment(documentation))
                self.comment_blocks_emitted += 1
                self.comment_lines_emitted += len(documentation)
            self.method_emitted += 1
            body.append(render_khayyam_method(member, name, influencing, influenced))

    def render_type_owned_instantiation(
        self,
        decl: CorpusDecl,
        owner: str,
        binding: dict[str, CorpusRef],
        target: CorpusTarget,
        body: list[str],
        imports: dict[str, str],
        local: set[str],
    ) -> None:
        """Emit a generic concept's methods on the owning type, not as a matrix abstraction."""
        _, methods = self.resolve_members(decl, owner, binding)
        for method, influencing, influenced in methods:
            influencing_types = [
                self.materialize(parameter.type_text, target, imports, local)
                for parameter in influencing
            ]
            influenced_types = [
                self.materialize(parameter.type_text, target, imports, local)
                for parameter in influenced
            ]
            if any(item is None for item in influencing_types) or any(
                item is None for item in influenced_types
            ):
                continue
            member = method.name
            if member in self.member_names:
                continue
            self.member_names.add(member)
            if body and body[-1].strip():
                body.append("")
            self.method_emitted += 1
            body.append(
                render_khayyam_method(
                    member,
                    owner,
                    [
                        KhayyamParameter(parameter.name, resolved)
                        for parameter, resolved in zip(influencing, influencing_types)
                    ],
                    [
                        KhayyamParameter(parameter.name, resolved)
                        for parameter, resolved in zip(influenced, influenced_types)
                    ],
                )
            )

    def render_target(self, target: CorpusTarget) -> str | None:
        blocked = sorted(
            decl.name
            for decl in target.roots
            if self.names is not None and decl.key in self.names.unrenderable
        )
        if blocked:
            self.omissions.append(
                {
                    "kind": "naming-unresolved-omitted",
                    "site": target.relative,
                    "detail": ", ".join(blocked) + ": left unwritten until the owner decides",
                }
            )
            return None
        body: list[str] = []
        imports: dict[str, str] = {}
        local: set[str] = set()
        for decl in target.roots:
            if decl.constraint:
                continue
            self.render_declaration(decl, target, {}, "", True, body, imports, local)
            for instantiation in self.instantiations.get(decl.key, []):
                if instantiation.home != target.relative:
                    continue
                binding = {
                    parameter: reference
                    for parameter, reference in zip(
                        decl.type_params, instantiation.arguments
                    )
                }
                if instantiation.type_owned:
                    owner = self.instantiation_owner_name(instantiation)
                    if owner is None:
                        continue
                    self.render_type_owned_instantiation(
                        decl, owner, binding, target, body, imports, local
                    )
                    continue
                self.render_declaration(
                    decl, target, binding, instantiation.name[len(decl.output) :], False, body, imports, local
                )
        lines = [CORPUS_LICENSE, ""]
        for name in sorted(imports):
            if name in local:
                continue
            lines.append(f'tp {name} in "{imports[name]}"')
        if any(line.startswith("tp ") for line in lines):
            lines.append("")
        lines.extend(body)
        text = "\n".join(lines).rstrip() + "\n"
        text = preserve_transfer_text(target.source, text)
        # Khayyam has one flat namespace: a file that would declare the same
        # name twice is never written, so the owner sees the case instead.
        declared = re.findall(r"^tp\s+(\S+)\s+(?:ab|mt|cp|sc)\b", text, re.M)
        repeated = sorted({name for name in declared if declared.count(name) > 1})
        if repeated:
            self.omissions.append(
                {
                    "kind": "naming-collision-inside-file",
                    "site": target.relative,
                    "detail": ", ".join(repeated),
                }
            )
            return None
        return text

    def audit_comments(self) -> None:
        files = {decl.path for decl in self.wanted.values() if decl.output_file}
        for path in sorted(files):
            source = self.sources.get(path)
            if source is None:
                continue
            index = CommentIndex(source.comments)
            for declaration in source.types:
                index.documenting(declaration.line)
            for interface in source.interfaces:
                for entry in interface.entries:
                    index.documenting(entry.line)
                for composition in interface.compositions:
                    index.documenting(composition.line)
            for method in source.methods:
                index.documenting(method.declaration_line)
            for block in index.floating():
                first = block.lines[0].strip() if block.lines else ""
                if first.startswith(CORPUS_LICENSE_TEXT):
                    # The file's licence header, not a doc comment: the Khayyam
                    # file already opens with it.
                    continue
                self.comment_floating.append(
                    (
                        Path(path).relative_to(self.go_root).as_posix(),
                        block.start,
                        first[:80],
                    )
                )
            self.comment_blocks += len(source.comments) - licence_blocks(source)

    def assign_homes(self) -> None:
        for decl in self.declarations.values():
            if decl.kind == "constraint":
                continue
            home = self.home_for(decl)
            if home is not None:
                decl.output_file = home.relative

    def discover(self) -> None:
        """Walk every ported declaration, at the abstraction level and once per
        concrete instantiation, until nothing new is referenced."""
        for _ in range(16):
            before = (set(self.wanted), set(self.instantiation_index))
            pending: list[tuple[CorpusDecl, dict[str, CorpusRef]]] = [
                (decl, {}) for decl in self.wanted.values()
            ]
            seen: set[tuple[str, str]] = set()
            while pending:
                decl, binding = pending.pop()
                fingerprint = (
                    decl.key,
                    ",".join(f"{name}={value.describe()}" for name, value in sorted(binding.items())),
                )
                if fingerprint in seen or decl.constraint:
                    continue
                seen.add(fingerprint)
                self.resolve_members(decl, decl.name, binding)
                for key, candidate in list(self.wanted.items()):
                    if (key, "") not in seen:
                        pending.append((candidate, {}))
                for instantiation in self.instantiations.get(decl.key, []):
                    pending.append(
                        (
                            decl,
                            dict(
                                zip(
                                    decl.type_params,
                                    instantiation.arguments,
                                )
                            ),
                        )
                    )
            if before == (set(self.wanted), set(self.instantiation_index)):
                return

    # -- driver -------------------------------------------------------------

    def write_hazards(self, target: CorpusTarget, rendered: str) -> list[str]:
        """What re-emitting `target` as `rendered` would destroy.

        The port only knows what the Go corpus says, so a file that holds
        anything else -- a capsule, a comment recovered by hand, a declaration
        whose Go source is gone -- is left for its owner rather than
        overwritten. Renames keep the counts, so counting kinds is enough to
        tell a rename from a loss.
        """
        return content_hazards(target.source, rendered)

    def prepare(self) -> None:
        self.load_sources()
        self.build_declarations()
        self.reserve_pre_existing()
        self.load_targets()
        # Two rounds: the first lays every declaration out from the Go corpus
        # alone so that the archive's own names can be read back, the second
        # honours the layout the archive already used where it filed a
        # declaration in its own module.
        self.assign_homes()
        self.assign_names()
        self.claim_baselines()
        self.assign_homes()
        self.scan_instantiations()
        self.collect_instantiations()
        self.discover()
        self.attach_roots()
        self.assign_names()
        self.name_instantiations()

    def run(self, write: bool) -> dict:
        self.prepare()
        for target in self.targets:
            if not target.selected:
                continue
            rendered = self.render_target(target)
            if rendered is None:
                continue
            if rendered == target.source:
                self.unchanged.append(target.relative)
                continue
            hazards = self.write_hazards(target, rendered)
            if hazards:
                self.omissions.append(
                    {
                        "kind": "target-would-lose-content",
                        "site": target.relative,
                        "detail": "left untouched: " + "; ".join(hazards),
                    }
                )
                self.guarded.append(target.relative)
                continue
            self.written.append(target.relative)
            if write:
                if target.path.read_text(encoding="utf-8", errors="replace") != target.source:
                    self.omissions.append(
                        {
                            "kind": "target-changed-during-run",
                            "site": target.relative,
                            "detail": "left untouched; another writer touched the file",
                        }
                    )
                    continue
                target.path.write_text(rendered, encoding="utf-8", newline="\n")
        self.audit_comments()
        return self.summary()

    def summary(self) -> dict:
        names = self.names
        return {
            "targets": sum(1 for target in self.targets if target.selected),
            "written": len(self.written),
            "unchanged": len(self.unchanged),
            "guarded": len(self.guarded),
            "guarded_files": list(self.guarded),
            "go_module": self.module_name,
            "go_files": len(self.sources),
            "go_parse_failures": self.parse_failures,
            "declarations_named": len(self.wanted),
            "declarations_renamed": list(names.renamed) if names else [],
            "declarations_reserved": list(names.reserved_names) if names else [],
            "naming_unresolved": list(names.unresolved) if names else [],
            "fixed_names": [
                f"{module}.{name} -> {fixed}"
                for (module, name), fixed in FIXED_KHAYYAM_DECLARATIONS.items()
            ],
            "instantiations": [
                {
                    "signature": instantiation.signature,
                    "name": instantiation.name,
                    "home": instantiation.home,
                }
                for instantiation in sorted(
                    self.instantiation_index.values(),
                    key=lambda item: (item.name, item.signature),
                )
            ],
            "generic_declarations": sorted(
                f"{decl.module}.{decl.name}"
                for decl in self.wanted.values()
                if decl.generic
            ),
            "comments_in_scope": self.comment_blocks,
            "comment_blocks_emitted": self.comment_blocks_emitted,
            "comment_lines_emitted": self.comment_lines_emitted,
            "comment_blocks_dropped": max(
                0,
                self.comment_blocks
                - self.comment_blocks_emitted
                - len(self.comment_floating),
            ),
            "comments_floating": self.comment_floating,
            "methods_emitted": self.method_emitted,
            "omissions": self.deduplicated_omissions(),
            "method_owners_unmatched": self.method_owners,
            "constants_and_variables_not_ported": [
                f"{path}: {kind} {', '.join(names)}" for path, kind, names in self.constants
            ],
        }

    def deduplicated_omissions(self) -> list[dict[str, object]]:
        emitted = {decl.output for decl in self.named.values()}
        emitted.update(
            instantiation.name for instantiation in self.instantiation_index.values()
        )
        items = list(self.omissions)
        for relative, name in self.unmatched_baseline:
            if name in emitted:
                continue
            items.append(
                {
                    "kind": "baseline-root-without-source",
                    "site": f"{relative} {name}",
                    "detail": "the first port declared it; the Go corpus has no such declaration",
                }
            )
        grouped: dict[tuple[str, str], dict[str, object]] = {}
        for item in items:
            key = (item["kind"], item["site"])
            entry = grouped.get(key)
            if entry is None:
                grouped[key] = {
                    "kind": item["kind"],
                    "site": item["site"],
                    "detail": item["detail"],
                    "occurrences": 1,
                }
            else:
                entry["occurrences"] = int(entry["occurrences"]) + 1
        return sorted(
            grouped.values(), key=lambda entry: (-int(entry["occurrences"]), str(entry["site"]))
        )


def build_reemit_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abstraction_bridge.py reemit",
        description="Re-emit the archived Go abstraction corpus as Khayyam abstractions.",
    )
    parser.add_argument("--go-root", required=True, help="path of the Go corpus root (holds go.mod)")
    parser.add_argument("--memar-root", required=True, help="path of the Khayyam archive root")
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="repository-relative .kh path to leave alone (repeatable)",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        help="suffix of a protocol file to re-emit (repeatable)",
    )
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument(
        "--print", action="store_true", help="print every re-emitted file instead of writing it"
    )
    parser.add_argument("--report", help="write the machine readable report as JSON")
    return parser


def reemit_main(argv: Sequence[str]) -> int:
    arguments = build_reemit_parser().parse_args(list(argv))
    port = CorpusPort(
        Path(arguments.go_root),
        Path(arguments.memar_root),
        excludes=arguments.exclude,
        only=arguments.only,
    )
    if arguments.print:
        port.prepare()
        for target in port.targets:
            if not target.selected:
                continue
            sys.stdout.write(f"===== {target.relative}\n")
            rendered = port.render_target(target)
            if rendered is None:
                sys.stdout.write("(not rendered; the omissions of a --report run say why)\n")
                continue
            hazards = port.write_hazards(target, rendered) if rendered != target.source else []
            for hazard in hazards:
                sys.stdout.write(f"(a write would leave this file untouched: {hazard})\n")
            sys.stdout.write(rendered)
        return 0
    summary = port.run(write=not arguments.dry_run)
    if arguments.report:
        Path(arguments.report).write_text(
            json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    print(
        "targets {targets}  written {written}  unchanged {unchanged}  guarded {guarded}".format(
            **summary
        )
    )
    print(
        "declarations {named}  renamed {renamed}  unresolved {unresolved}".format(
            named=summary["declarations_named"],
            renamed=len(summary["declarations_renamed"]),
            unresolved=len(summary["naming_unresolved"]),
        )
    )
    print(
        "comment blocks in scope {scope}  emitted {emitted}  dropped {dropped}  floating {floating}".format(
            scope=summary["comments_in_scope"],
            emitted=summary["comment_blocks_emitted"],
            dropped=summary["comment_blocks_dropped"],
            floating=len(summary["comments_floating"]),
        )
    )
    print(f"methods emitted {summary['methods_emitted']}")
    print(
        "instantiations {count}  parse failures {failures}".format(
            count=len(summary["instantiations"]),
            failures=len(summary["go_parse_failures"]),
        )
    )
    print(
        "files with constants or variables not ported {count}".format(
            count=len({item.split(":", 1)[0] for item in summary["constants_and_variables_not_ported"]})
        )
    )
    print(f"omissions {len(summary['omissions'])} distinct")
    return 0
