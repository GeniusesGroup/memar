"""Convert Go interface declarations to Khayyam abstractions and back.
Usage:
  python abstraction_bridge.py go-to-khayyam [--mode 1|2|promote|refuse] [--only Interface[.Method]] PATH [PATH ...]
  python abstraction_bridge.py khayyam-to-go [--mode 1|2|promote|refuse] PATH [PATH ...]
  python abstraction_bridge.py reemit --go-root PATH --memar-root PATH [--only FILE] [--exclude FILE] [--dry-run] [--report FILE]
  python abstraction_bridge.py transfer SOURCE DEST [--memar-root PATH] [--go-root PATH] [--recursive] [--exclude PREFIX] [--write] [--verify] [--report FILE]
  python abstraction_bridge.py tidy [PATH ...] [--memar-root PATH] [--exclude PREFIX] [--rule NAME] [--write] [--report FILE]
  python abstraction_bridge.py observer-names [PATH ...] [--memar-root PATH] [--exclude PREFIX] [--write] [--no-frontend] [--report FILE]
  python abstraction_bridge.py bare-names [PATH ...] [--memar-root PATH] [--exclude PREFIX] [--write] [--no-frontend] [--report FILE]

PATH may be a source file or a directory. Go mode 1 promotes referenced
non-interface types and mode 2 refuses them. --only narrows the Go direction
to one interface or one method. The inverse direction emits Go interfaces and
refuses constructs without a Go interface form.

`reemit` is the corpus direction: it re-emits every protocol file of the
Khayyam archive from the whole Go corpus, carrying Go doc comments over
verbatim, qualifying every declaration by its module, emitting generic
interfaces as plain abstractions, and importing through real file URIs. It
only rewrites protocol files that already exist, and it never rewrites one
whose declarations or comments the Go corpus does not carry: such a file is
reported as guarded and left for its owner.

`transfer` moves one Go source into one Khayyam destination and is dry unless
--write is given. It creates a destination that does not exist and only ever
inserts into one that does. Declarations with a Khayyam form are written;
every other construct stays as a `TODO(go-migrate)` residue carrying its
original Go text, and the whole Go file is appended as comments.

`tidy` applies the source-rewrite rules of `modules/khayyam/rules/` --
commented-generic-bindings, go-clue-residue, result-parameter-names and
method-separation -- to Khayyam files in place, and is dry unless --write is
given. It leaves `modules/khayyam/` alone unless told otherwise.

`observer-names` applies the observer shape of the [ADT observer and mutator rule](../../computer/adt/rules/observer-mutator/observer-mutator.md), the [qualified names rule](../../rules/qualified-names/qualified-names.md), and the [receiver method names rule](../../rules/receiver-method-names/receiver-method-names.md) to Khayyam files: `URI_Observer_Scheme` becomes `Observer_Scheme`
(or `Observer_URI_Scheme` when the short name is taken or its concept is declared
by more than one module) and its method `URI_Observer_Scheme_Scheme` becomes
`GetScheme` (or `GetURIScheme` when that is ambiguous). Legacy
`URI_Field_Scheme` / `Field_*` spellings are accepted as input. It is dry
unless --write is given, and it writes nothing the Khayyam frontend would
newly refuse.

`bare-names` strips module and owner prefixes when the bare name is unique
across the corpus: `Datatype_Quiddity` becomes `Quiddity`, and
`Computer_Detail_Domain` becomes `Domain`. It updates `in` imports and every
reference in the Khayyam part, leaves end-of-file Go blocks unchanged, and is
dry unless --write is given.

The two directions are here. Each corpus-scale command -- `reemit`, `transfer`,
`tidy`, `observer-names`, `bare-names` -- is the file named for it beside this one."""

from __future__ import annotations
import re
import argparse
import sys
from typing import Sequence

from failures import (
    BridgeFailure,
    SourceFailure,
)
from names import (
    KHAYYAM_TO_GO,
    KNOWN_GO_INTERFACES,
    PRIMITIVE_MAP,
    field_accessor_options,
    split_field_name,
)
from go_source import (
    GoInterface,
    GoModel,
    GoType,
    GoWorkspace,
    InterfaceEntry,
    Parameter,
    PromotedType,
    ResolvedType,
    Token,
    has_unmappable_type,
    is_empty_interface,
    lex_source,
    parse_go_source,
    source_model,
    source_paths,
    token_text,
)
from khayyam_source import (
    KEYWORDS,
    KhayyamDeclaration,
    KhayyamParameter,
    body_is_bodyless,
    parse_khayyam_source,
)
from corpus_port import reemit_main
from tidy import tidy_main
from transfer import transfer_main
# The names below moved into the module that owns each concern. They are
# re-exported here because another repository's migration tooling imports them
# from this module by name, and a split that silently breaks a caller outside
# this folder is a worse outcome than a longer import list. Remove each line
# when its caller names the module that owns it.
from corpus_port import CorpusPort  # noqa: F401
from khayyam_source import end_blocks, khayyam_head, tidy_paths  # noqa: F401
from khayyam_frontend import frontend_outcomes, FRONTEND_CHECK  # noqa: F401
from names import CORPUS_MODULE_ROOTS, split_field_name  # noqa: F401
from comments import strip_comments  # noqa: F401
from tidy import TIDY_EXCLUDES, shrink_go_lines  # noqa: F401
from renames import field_defs, rename_tokens  # noqa: F401
from failures import SourceFailure  # noqa: F401
from renames import (
    bare_names_main,
    observer_names_main,
)


def format_reference_error(path: str, construct: str, type_text: str, reason: str) -> str:
    return (
        f"{path}: {construct} cannot reference {type_text!r} from a Khayyam abstraction: {reason}"
    )


class GoToKhayyam:
    def __init__(self, model: GoModel, mode: int, only: str | None = None):
        self.model = model
        self.mode = mode
        self.only = only
        self.workspace = GoWorkspace(model)
        self.errors: list[str] = []
        self.imports: dict[str, str] = {}
        self.reserved_names: set[str] = set(model.types)
        self.reserved_names.update(interface.name for interface in model.interfaces)
        self.used_method_names: set[str] = set()
        self.promoted: dict[tuple[int, str], PromotedType] = {}
        self.generated_count = 0
        self.generated_abstractions: list[str] = []
        self.output_interfaces: list[tuple[GoInterface, list[str], list[tuple[str, list[KhayyamParameter], list[KhayyamParameter]]]]] = []
        self.output_promoted: list[PromotedType] = []

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def add_import(self, name: str, path: str) -> None:
        if name in self.model.types:
            self.fail(f"import {name!r} collides with local type {name!r}")
            return
        previous = self.imports.get(name)
        if previous and previous != path:
            self.fail(f"type name {name!r} is imported from both {previous!r} and {path!r}")
            return
        self.imports.setdefault(name, path)
        self.reserved_names.add(name)

    def generated_name(self, prefix: str) -> str:
        self.generated_count += 1
        name = f"{prefix}{self.generated_count}"
        self.generated_abstractions.append(name)
        self.reserved_names.add(name)
        return name

    def resolve_type(
        self,
        model: GoModel,
        type_tokens: Sequence[Token],
        path: str,
        line: int,
        construct: str,
    ) -> ResolvedType | None:
        if not type_tokens:
            self.fail(f"{path}:{line}: {construct} has no type")
            return None
        type_text = token_text(type_tokens)
        unmappable = has_unmappable_type(type_tokens)
        if unmappable:
            self.fail(f"{path}:{line}: {construct} has unmappable {unmappable} type {type_text!r}")
            return None
        if is_empty_interface(type_tokens):
            name = self.generated_name("EmptyInterface")
            return ResolvedType(name, True)
        primitive = PRIMITIVE_MAP.get(type_text)
        if primitive:
            self.add_import(primitive[0], primitive[1])
            return ResolvedType(primitive[0], True)
        if type_text in {"interface", "any"}:
            name = self.generated_name("EmptyInterface")
            return ResolvedType(name, True)
        if "." not in type_text:
            declaration = model.types.get(type_text)
            if declaration:
                if declaration.generic:
                    self.fail(f"{path}:{line}: {construct} uses generic type {type_text!r}")
                    return None
                if declaration.kind == "interface":
                    return ResolvedType(type_text, True, model, declaration)
                if declaration.alias and declaration.underlying:
                    target_tokens = lex_source(declaration.underlying, True)[:-1]
                    target = self.resolve_type(
                        model,
                        target_tokens,
                        declaration.path,
                        declaration.line,
                        f"alias target of {type_text}",
                    )
                    if target and target.is_interface:
                        return target
                if self.mode == 2:
                    self.fail(
                        format_reference_error(
                            path,
                            construct,
                            type_text,
                            "it is a non-interface type and mode 2 forbids promotion",
                        )
                    )
                    return None
                return self.promote(model, declaration, type_text)
            if type_text in KNOWN_GO_INTERFACES:
                return ResolvedType(type_text, True)
            if self.mode == 2:
                self.fail(
                    format_reference_error(
                        path,
                        construct,
                        type_text,
                        "its interface kind cannot be established and mode 2 forbids promotion",
                    )
                )
                return None
            return self.promote(model, GoType(type_text, "unknown", "", False, False, path, line), type_text)
        parts = type_text.split(".")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            self.fail(f"{path}:{line}: {construct} has invalid qualified type {type_text!r}")
            return None
        alias, name = parts
        import_path = model.imports.get(alias)
        if import_path is None:
            if f"{alias}.{name}" in KNOWN_GO_INTERFACES:
                return ResolvedType(type_text, True)
            if self.mode == 2:
                self.fail(
                    format_reference_error(
                        path,
                        construct,
                        type_text,
                        "its import is unknown and mode 2 forbids promotion",
                    )
                )
                return None
            return self.promote(model, GoType(name, "unknown", "", False, False, path, line), type_text)
        external = self.workspace.load_import(import_path, model)
        declaration = external.types.get(name) if external else None
        if declaration and declaration.generic:
            self.fail(f"{path}:{line}: {construct} uses generic type {type_text!r}")
            return None
        if declaration and declaration.kind == "interface":
            self.add_import(name, import_path)
            return ResolvedType(name, True, external, declaration)
        if declaration and declaration.alias and declaration.underlying:
            target_tokens = lex_source(declaration.underlying, True)[:-1]
            target = self.resolve_type(
                external,
                target_tokens,
                declaration.path,
                declaration.line,
                f"alias target of {type_text}",
            )
            if target and target.is_interface:
                return target
        if self.mode == 2:
            self.fail(
                format_reference_error(
                    path,
                    construct,
                    type_text,
                    "it is a non-interface or unresolved type and mode 2 forbids promotion",
                )
            )
            return None
        if declaration:
            return self.promote(external, declaration, type_text)
        return self.promote(model, GoType(name, "unknown", "", False, False, path, line), type_text)

    def promote(self, model: GoModel, declaration: GoType, source_name: str) -> ResolvedType:
        output_name = source_name.replace(".", "_")
        key = (id(model), declaration.name)
        promoted = self.promoted.get(key)
        if promoted is None:
            promoted = PromotedType(output_name, model, declaration.name)
            self.promoted[key] = promoted
            self.output_promoted.append(promoted)
            self.reserved_names.add(output_name)
            methods = model.methods.get(declaration.name, [])
            seen: set[tuple[str, str]] = set()
            for method in methods:
                fingerprint = (method.name, token_text([Token(p.type_text, "ident", 0) for p in method.parameters]))
                if fingerprint in seen:
                    continue
                seen.add(fingerprint)
                promoted.methods.append(method)
        return ResolvedType(output_name, True, model, declaration, output_name)

    def method_name(self, owner: str, original: str, value_types: Sequence[str] = ()) -> str:
        if split_field_name(owner) is not None:
            for option in field_accessor_options(owner, original, value_types):
                if option not in self.reserved_names and option not in self.used_method_names:
                    self.used_method_names.add(option)
                    return option
            suffix = 2
            while f"{original}_{suffix}" in self.reserved_names or f"{original}_{suffix}" in self.used_method_names:
                suffix += 1
            self.used_method_names.add(f"{original}_{suffix}")
            return f"{original}_{suffix}"
        candidate = original
        if candidate in self.reserved_names or candidate in self.used_method_names:
            candidate = f"{owner}_{original}"
            suffix = 2
            while candidate in self.reserved_names or candidate in self.used_method_names:
                candidate = f"{owner}_{original}_{suffix}"
                suffix += 1
        self.used_method_names.add(candidate)
        return candidate

    def convert_parameters(
        self,
        model: GoModel,
        parameters: Sequence[Parameter],
        path: str,
        line: int,
        owner: str,
        construct: str,
        result: bool,
    ) -> list[KhayyamParameter] | None:
        converted: list[KhayyamParameter] = []
        used: set[str] = set()
        for index, parameter in enumerate(parameters):
            if parameter.variadic:
                self.fail(f"{path}:{line}: {construct} has unmappable variadic type {parameter.type_text!r}")
                return None
            name = parameter.name
            if not name or name == "_":
                name = "result" if result else "arg"
                name = f"{name}{index}"
            if name in used:
                name = f"{name}_{index}"
            used.add(name)
            resolved = self.resolve_type(
                model,
                lex_source(parameter.type_text, True)[:-1],
                path,
                line,
                construct,
            )
            if resolved is None:
                return None
            converted.append(KhayyamParameter(name, resolved.text))
        return converted

    def convert_method(
        self,
        model: GoModel,
        owner: str,
        method: InterfaceEntry,
        path: str,
    ) -> tuple[str, list[KhayyamParameter], list[KhayyamParameter]] | None:
        construct = f"method {method.name} of interface {owner}"
        parameters = self.convert_parameters(
            model,
            method.parameters,
            path,
            method.line,
            owner,
            construct,
            False,
        )
        results = self.convert_parameters(
            model,
            method.results,
            path,
            method.line,
            owner,
            construct,
            True,
        )
        if parameters is None or results is None:
            return None
        return self.method_name(owner, method.name, [result.type_text for result in results]), parameters, results

    def convert_promoted_methods(self, promoted: PromotedType) -> list[tuple[str, list[KhayyamParameter], list[KhayyamParameter]]]:
        output: list[tuple[str, list[KhayyamParameter], list[KhayyamParameter]]] = []
        for method in promoted.methods:
            if method.generic:
                self.fail(
                    f"{method.path}:{method.line}: generic method {method.name!r} of promoted type {promoted.source_name} is unmappable"
                )
                continue
            construct = f"method {method.name} of promoted type {promoted.source_name}"
            parameters = self.convert_parameters(
                promoted.model,
                method.parameters,
                method.path,
                method.line,
                promoted.name,
                construct,
                False,
            )
            results = self.convert_parameters(
                promoted.model,
                method.results,
                method.path,
                method.line,
                promoted.name,
                construct,
                True,
            )
            if parameters is None or results is None:
                continue
            output.append((self.method_name(promoted.name, method.name), parameters, results))
        return output

    def selected_interface(self, interface: GoInterface) -> GoInterface | None:
        if not self.only:
            return interface
        parts = self.only.split(".", 1)
        if parts[0] != interface.name:
            return None
        if len(parts) == 1:
            return interface
        method_name = parts[1]
        entries = [entry for entry in interface.entries if entry.name == method_name]
        if not entries:
            self.fail(
                f"{interface.path}:{interface.line}: selected method {method_name!r} is not in interface {interface.name!r}"
            )
            return None
        return GoInterface(
            interface.name,
            entries,
            interface.compositions,
            interface.generic,
            interface.path,
            interface.line,
        )

    def convert(self) -> str:
        seen_interfaces: set[str] = set()
        selected_owner_found = False
        for source_interface in self.model.interfaces:
            if self.only and self.only.split(".", 1)[0] == source_interface.name:
                selected_owner_found = True
            interface = self.selected_interface(source_interface)
            if interface is None:
                continue
            if interface.name in seen_interfaces:
                self.fail(f"{interface.path}:{interface.line}: duplicate interface {interface.name!r}")
                continue
            seen_interfaces.add(interface.name)
            if interface.generic:
                self.fail(f"{interface.path}:{interface.line}: generic interface {interface.name!r} is unmappable")
                continue
            compositions: list[str] = []
            for composition in interface.compositions:
                if composition.anonymous:
                    self.fail(
                        f"{interface.path}:{interface.line}: embedded anonymous interface is unmappable"
                    )
                    continue
                if "[" in composition.text or "]" in composition.text:
                    self.fail(
                        f"{interface.path}:{interface.line}: embedded generic type {composition.text!r} is unmappable"
                    )
                    continue
                resolved = self.resolve_type(
                    self.model,
                    [Token(part, "ident", interface.line) for part in composition.text.split()],
                    interface.path,
                    interface.line,
                    f"embedded type of interface {interface.name}",
                )
                if resolved:
                    compositions.append(resolved.text)

            methods: list[tuple[str, list[KhayyamParameter], list[KhayyamParameter]]] = []
            for method in interface.entries:
                if method.generic:
                    self.fail(
                        f"{interface.path}:{method.line}: generic method {method.name!r} is unmappable"
                    )
                    continue
                converted = self.convert_method(self.model, interface.name, method, interface.path)
                if converted:
                    methods.append(converted)
            self.output_interfaces.append((interface, compositions, methods))
        if self.only and not selected_owner_found:
            self.fail(f"selected interface {self.only.split('.', 1)[0]!r} was not found")
        promoted_methods: dict[str, list[tuple[str, list[KhayyamParameter], list[KhayyamParameter]]]] = {}
        for promoted in self.output_promoted:
            promoted_methods[promoted.name] = self.convert_promoted_methods(promoted)
        if self.errors:
            raise BridgeFailure(self.errors)
        lines: list[str] = []
        for name, path in self.imports.items():
            lines.append(f'tp {name} in "{path}"')
        for name in self.generated_abstractions:
            lines.append(f"tp {name} ab")
        for interface, compositions, methods in self.output_interfaces:
            if compositions:
                lines.append(f"tp {interface.name} ab {{")
                lines.extend(f"    {name}" for name in compositions)
                lines.append("}")
            else:
                lines.append(f"tp {interface.name} ab")
            for name, influencing, influenced in methods:
                lines.append(render_khayyam_method(name, interface.name, influencing, influenced))
        for promoted in self.output_promoted:
            lines.append(f"tp {promoted.name} ab")
        for promoted in self.output_promoted:
            for name, influencing, influenced in promoted_methods[promoted.name]:
                lines.append(render_khayyam_method(name, promoted.name, influencing, influenced))
        return "\n".join(lines) + ("\n" if lines else "")


def render_khayyam_method(
    name: str,
    owner: str,
    influencing: Sequence[KhayyamParameter],
    influenced: Sequence[KhayyamParameter],
) -> str:
    first = ", ".join(f"{parameter.name} {parameter.type_text}" for parameter in influencing)
    second = ", ".join(f"{parameter.name} {parameter.type_text}" for parameter in influenced)
    return f"tp {name} mt (self {owner}) ({first}) ({second})"


def convert_go_to_khayyam(values: Sequence[str], mode: int, only: str | None = None) -> str:
    loaded = source_paths(values, ".go")
    sources = [parse_go_source(path, source) for path, source in loaded]
    model = source_model(sources)
    return GoToKhayyam(model, mode, only).convert()


class KhayyamToGo:
    def __init__(self, declarations: list[KhayyamDeclaration]):
        self.declarations = declarations
        self.abstractions: dict[str, KhayyamDeclaration] = {}
        self.capsules: set[str] = set()
        self.imports: dict[str, tuple[str, str]] = {}
        self.errors: list[str] = []
        self.used_import_aliases: set[str] = set()
        self.import_aliases: dict[str, str] = {}

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def package_alias(self, path: str) -> str:
        candidate = path.rstrip("/").split("/")[-1]
        candidate = re.sub(r"[^A-Za-z0-9_]", "_", candidate)
        if not candidate or candidate[0].isdigit():
            candidate = f"pkg_{candidate}"
        base = candidate
        suffix = 2
        while candidate in self.used_import_aliases:
            candidate = f"{base}_{suffix}"
            suffix += 1
        self.used_import_aliases.add(candidate)
        return candidate

    def setup(self) -> None:
        for declaration in self.declarations:
            if declaration.kind == "ab":
                if declaration.name in self.abstractions:
                    self.fail(f"{declaration.path}:{declaration.line}: duplicate abstraction {declaration.name!r}")
                self.abstractions[declaration.name] = declaration
            elif declaration.kind in {"cp", "sc"}:
                self.capsules.add(declaration.name)
            elif declaration.kind == "in":
                if declaration.name in self.abstractions or declaration.name in self.capsules:
                    self.fail(f"{declaration.path}:{declaration.line}: import duplicates {declaration.name!r}")
                import_path = declaration.composition[0]
                previous = self.imports.get(declaration.name)
                if previous and previous[0] != import_path:
                    self.fail(
                        f"{declaration.path}:{declaration.line}: import name {declaration.name!r} is declared from two paths"
                    )
                self.imports[declaration.name] = (import_path, declaration.path)
        for name, (import_path, _) in self.imports.items():
            if name not in KHAYYAM_TO_GO and name not in self.abstractions:
                self.import_aliases[name] = self.package_alias(import_path)

    def go_type(
        self,
        type_name: str,
        declaration_path: str,
        line: int,
        construct: str,
        composition: bool = False,
    ) -> str | None:
        if type_name in self.abstractions:
            return type_name
        if type_name in self.imports:
            if type_name in KHAYYAM_TO_GO:
                if composition:
                    self.fail(
                        f"{declaration_path}:{line}: {construct} composes primitive {type_name!r}, which has no Go interface form"
                    )
                    return None
                return KHAYYAM_TO_GO[type_name]
            return f"{self.import_aliases[type_name]}.{type_name}"
        if type_name in KHAYYAM_TO_GO:
            if composition:
                self.fail(
                    f"{declaration_path}:{line}: {construct} composes primitive {type_name!r}, which has no Go interface form"
                )
                return None
            return KHAYYAM_TO_GO[type_name]
        if type_name in self.capsules:
            self.fail(
                f"{declaration_path}:{line}: {construct} references capsule {type_name!r}, which has no Go interface form"
            )
            return None
        if "." in type_name:
            self.fail(
                f"{declaration_path}:{line}: {construct} references qualified type {type_name!r} without a resolvable Khayyam import, which has no Go interface form"
            )
            return None
        self.fail(
            f"{declaration_path}:{line}: {construct} references unknown type {type_name!r}, which has no Go interface form"
        )
        return None

    def validate_parameters(
        self,
        parameters: Sequence[KhayyamParameter],
        declaration: KhayyamDeclaration,
        construct: str,
    ) -> bool:
        names: set[str] = set()
        valid = True
        for parameter in parameters:
            if parameter.name in names:
                self.fail(f"{declaration.path}:{declaration.line}: {construct} repeats parameter {parameter.name!r}")
                valid = False
            names.add(parameter.name)
            if parameter.name in KEYWORDS:
                self.fail(f"{declaration.path}:{declaration.line}: {construct} uses Khayyam keyword as a Go name")
                valid = False
            if self.go_type(
                parameter.type_text,
                declaration.path,
                declaration.line,
                construct,
            ) is None:
                valid = False
        return valid

    def convert(self) -> str:
        self.setup()
        methods_by_owner: dict[str, list[KhayyamDeclaration]] = {}
        for declaration in self.declarations:
            if declaration.kind != "mt":
                if declaration.kind in {"cp", "sc", "vr", "vr-in"}:
                    self.fail(
                        f"{declaration.path}:{declaration.line}: {declaration.kind} declaration {declaration.name!r} has no Go interface form"
                    )
                continue
            if declaration.body_present and not body_is_bodyless(declaration.body_tokens):
                self.fail(
                    f"{declaration.path}:{declaration.line}: method {declaration.name!r} has a body and no body-less Go interface form"
                )
                continue
            owner = [parameter for parameter in declaration.owner if parameter.name == "self"]
            if len(declaration.owner) != 1 or len(owner) != 1:
                self.fail(
                    f"{declaration.path}:{declaration.line}: method {declaration.name!r} must have exactly one owner named self"
                )
                continue
            owner_name = owner[0].type_text
            if owner_name not in self.abstractions:
                self.fail(
                    f"{declaration.path}:{declaration.line}: method {declaration.name!r} owner {owner_name!r} is not a local abstraction"
                )
                continue
            if not self.validate_parameters(declaration.influencing, declaration, f"method {declaration.name}"):
                continue
            if not self.validate_parameters(declaration.influenced, declaration, f"method {declaration.name}"):
                continue
            methods_by_owner.setdefault(owner_name, []).append(declaration)
        if not self.abstractions:
            self.fail("input contains no Khayyam abstraction")
        for owner, abstraction in self.abstractions.items():
            for composition in abstraction.composition:
                self.go_type(
                    composition,
                    abstraction.path,
                    abstraction.line,
                    f"composition of interface {owner}",
                    True,
                )
        for owner, methods in methods_by_owner.items():
            names: set[str] = set()
            for method in methods:
                if method.name in names:
                    self.fail(
                        f"{method.path}:{method.line}: interface {owner!r} repeats method {method.name!r}"
                    )
                names.add(method.name)
        if self.errors:
            raise BridgeFailure(self.errors)
        lines = ["package generated", ""]
        for name, (import_path, _) in self.imports.items():
            if name in self.import_aliases:
                lines.append(f'import {self.import_aliases[name]} "{import_path}"')
        if any(name in self.import_aliases for name in self.imports):
            lines.append("")
        for owner in self.abstractions:
            methods = methods_by_owner.get(owner, [])
            lines.append(f"type {owner} interface {{")
            declaration = self.abstractions[owner]
            for composition in declaration.composition:
                mapped = self.go_type(
                    composition,
                    declaration.path,
                    declaration.line,
                    f"composition of interface {owner}",
                    True,
                )
                if mapped:
                    lines.append(f"\t{mapped}")
            for method in methods:
                influencing = ", ".join(
                    f"{parameter.name} {self.go_type(parameter.type_text, method.path, method.line, f'method {method.name}') or ''}"
                    for parameter in method.influencing
                )
                results = [
                    f"{parameter.name} {self.go_type(parameter.type_text, method.path, method.line, f'method {method.name}') or ''}"
                    for parameter in method.influenced
                ]
                signature = f"\t{method.name}({influencing})"
                if results:
                    signature += f" ({', '.join(results)})"
                lines.append(signature)
            lines.append("}")
            lines.append("")
        return "\n".join(lines).rstrip() + "\n"


def convert_khayyam_to_go(values: Sequence[str]) -> str:
    loaded = source_paths(values, ".kh")
    declarations: list[KhayyamDeclaration] = []
    for path, source in loaded:
        declarations.extend(parse_khayyam_source(path, source))
    return KhayyamToGo(declarations).convert()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert Go interface declarations and Khayyam abstractions."
    )
    parser.add_argument("direction", choices=("go-to-khayyam", "khayyam-to-go"))
    parser.add_argument("paths", nargs="+")
    parser.add_argument(
        "--mode",
        choices=("1", "2", "promote", "refuse"),
        default="1",
        help="Go direction: 1/promote non-interface references, 2/refuse them",
    )
    parser.add_argument(
        "--only",
        help="Go direction: convert only Interface or Interface.Method",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    given = list(sys.argv[1:] if argv is None else argv)
    if given and given[0] == "reemit":
        return reemit_main(given[1:])
    if given and given[0] == "transfer":
        return transfer_main(given[1:])
    if given and given[0] == "tidy":
        return tidy_main(given[1:])
    if given and given[0] == "observer-names":
        return observer_names_main(given[1:])
    if given and given[0] == "bare-names":
        return bare_names_main(given[1:])
    parser = build_parser()
    arguments = parser.parse_args(given)
    mode = 2 if arguments.mode in {"2", "refuse"} else 1
    try:
        if arguments.direction == "go-to-khayyam":
            output = convert_go_to_khayyam(arguments.paths, mode, arguments.only)
        else:
            output = convert_khayyam_to_go(arguments.paths)
    except (BridgeFailure, SourceFailure) as error:
        if isinstance(error, BridgeFailure):
            messages = error.messages
        else:
            messages = [str(error)]
        for message in messages:
            print(f"error: {message}", file=sys.stderr)
        return 2
    sys.stdout.write(output)
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
