"""`observer-names` and `bare-names`: the two passes that rename what the corpus already
holds. Both are dry unless --write is given, and both plan before they apply -- a
plan says what each name becomes and, for every name it will not touch, why.

`observer-names` applies the observer shape of the ADT observer and mutator rule, the
qualified names rule, and the receiver method names rule: `URI_Observer_Scheme`
becomes `Observer_Scheme` (or `Observer_URI_Scheme` when the short name is taken or
its concept is declared by more than one module) and its method
`URI_Observer_Scheme_Scheme` becomes `Scheme` (or `URIScheme` when that is
ambiguous). Legacy `URI_Field_Scheme` / `Field_*` spellings are accepted as input. It
writes nothing the Khayyam frontend would newly refuse.

`bare-names` strips module and owner prefixes when the bare name is unique across the
corpus: `Datatype_Quiddity` becomes `Quiddity`, and `Computer_Detail_Domain` becomes
`Domain`. It updates `in` imports and every reference in the Khayyam part, and
leaves end-of-file Go blocks unchanged."""

import re
import argparse
import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Sequence

from failures import BridgeFailure
from names import (
    concept_forms,
    field_accessor_options,
    field_holds_its_concept,
    field_identity,
    field_name,
    module_identity,
    normalize_name,
    pascal_segment,
    qualified_by_module,
    repeats,
    split_field_name,
    strip_protocol,
)
from khayyam_source import (
    end_blocks,
    kh_module,
    khayyam_head,
    tidy_paths,
)
from khayyam_frontend import frontend_outcomes
from tidy import TIDY_EXCLUDES


@dataclass
class FieldDef:
    relative: str
    name: str
    kind: str
    owner: str
    signature: tuple[tuple[str, ...], tuple[str, ...]]
    module: str


def field_defs(texts: dict[str, str]) -> list[FieldDef]:
    """Every declaration (not inclusion) of the Khayyam part of `texts`."""
    found: list[FieldDef] = []
    for relative, text in sorted(texts.items()):
        lines = text.split("\n")
        blocks = end_blocks(lines)
        head = lines[: blocks[0].marker] if blocks else lines
        module = kh_module(relative)
        for declaration in khayyam_head(head):
            if declaration.kind == "in":
                continue
            signature: tuple[tuple[str, ...], tuple[str, ...]] = ((), ())
            if declaration.kind == "mt":
                signature = (
                    tuple(type_text for _, type_text in declaration.group(1)),
                    tuple(type_text for _, type_text in declaration.group(2)),
                )
            found.append(
                FieldDef(relative, declaration.name, declaration.kind, declaration.owner, signature, module)
            )
    return found


def observer_names_plan(texts: dict[str, str]) -> dict:
    """The field shape of the qualified names and receiver method names rules
    over one corpus.

    `<Q>_Field_<X>` becomes `Field_<X>` when Q only repeats what X says, or
    when every accessor returns X and no second module declares an X or
    names an abstraction's method X; otherwise `Field_<Q>_<X>`. Q is kept
    when X starts with another module's identity. A field abstraction's method
    `<Owner>_<M>` becomes the first of `field_accessor_options` that names no
    declaration and no method of another signature. A pair the qualifier
    cannot separate and a name declared twice are skipped; a method with no
    free name is skipped too, and when its owner is renamed its owner part
    follows, so the method is where the unprefixed fields' methods already are.
    """
    defs = field_defs(texts)
    counts: dict[str, int] = {}
    for item in defs:
        counts[item.name] = counts.get(item.name, 0) + 1
    by_name = {item.name: item for item in defs}
    kinds = {item.name: item.kind for item in defs}
    fields = [item for item in defs if item.kind == "ab" and split_field_name(item.name) is not None]
    methods_of: dict[str, list[FieldDef]] = {}
    for item in defs:
        if item.kind == "mt":
            methods_of.setdefault(item.owner, []).append(item)
    identities = {field_identity(kh_module(relative)) for relative in texts} - {""}
    skipped: dict[str, str] = {}
    checks: dict[str, str] = {}

    def concept_modules(concept: str, own: str) -> set[str]:
        forms = concept_forms(concept)
        claims = set()
        for item in defs:
            if split_field_name(item.name) is not None:
                continue
            if item.kind == "mt":
                if item.owner != own and kinds.get(item.owner) == "ab" and item.name in forms:
                    claims.add(strip_protocol(item.module))
            elif any(item.name == form or item.name.endswith("_" + form) for form in forms):
                claims.add(strip_protocol(item.module))
        return claims

    unseparable: set[str] = set()
    twins: dict[tuple[str, str], list[str]] = {}
    for item in fields:
        qualifier, concept = split_field_name(item.name)  # type: ignore[misc]
        if qualifier:
            twins.setdefault((field_identity(item.module), concept), []).append(item.name)

    ab_options: dict[str, list[str]] = {}
    for item in fields:
        qualifier, concept = split_field_name(item.name)  # type: ignore[misc]
        if not qualifier:
            continue
        if counts[item.name] > 1:
            skipped[item.name] = "declared more than once in the corpus"
            continue
        rivals = [name for name in twins[(field_identity(item.module), concept)] if name != item.name]
        if rivals:
            unseparable.add(item.name)
            skipped[item.name] = (
                "its module path names it as it names "
                + ", ".join(rivals)
                + ", so qualification cannot separate them; which module keeps the concept is an owner question"
            )
            continue
        values = [
            text for method in methods_of.get(item.name, []) for text in method.signature[1] if text != "Error"
        ]
        leading = concept.split("_", 1)[0] if "_" in concept else ""
        short, qualified = field_name(concept), field_name(concept, qualifier)
        if repeats(qualifier, concept):
            checks[item.name] = f"`{concept}` already says `{qualifier}`"
            ab_options[item.name] = [short, qualified]
            continue
        if leading and normalize_name(leading) in identities - {field_identity(item.module)}:
            checks[item.name] = f"`{concept}` starts with the module identity `{leading}`; `{qualifier}` is kept"
            ab_options[item.name] = [qualified]
            continue
        if not field_holds_its_concept(concept, values) and any(repeats(qualifier, value) for value in values):
            checks[item.name] = f"an accessor returns {', '.join(sorted(set(values)))}: `{qualifier}` names the value; kept"
            ab_options[item.name] = [qualified]
            continue
        claimed = concept_modules(concept, item.name)
        if leading and len(concept_modules(leading, item.name)) > 1:
            claimed |= concept_modules(leading, item.name)
        if len(claimed) <= 1:
            checks[item.name] = f"`{concept}` is claimed by {len(claimed)} module(s)"
            ab_options[item.name] = [short, qualified]
        else:
            checks[item.name] = f"`{concept}` is claimed by {len(claimed)} modules: " + ", ".join(sorted(claimed))
            ab_options[item.name] = [qualified]

    non_methods = {item.name for item in defs if item.kind != "mt"}
    method_options: dict[str, list[str]] = {}
    field_methods: dict[str, FieldDef] = {}
    for item in fields:
        for method in methods_of.get(item.name, []):
            # a realization repeats the name on its own capsule and is renamed with it
            if not method.name.startswith(item.name + "_") or method.name in non_methods:
                continue
            original = method.name[len(item.name) + 1 :]
            method_options[method.name] = field_accessor_options(item.name, original, method.signature[1])
            field_methods[method.name] = method

    ab_index = {name: 0 for name in ab_options}
    method_index = {name: 0 for name in method_options}

    def skip_owner(name: str, reason: str) -> None:
        if name in ab_index:
            del ab_index[name]
            skipped[name] = reason

    changed = True
    while changed:
        changed = False
        ab_now = {name: ab_options[name][index] for name, index in ab_index.items()}
        method_now = {name: method_options[name][index] for name, index in method_index.items()}

        def renamed(name: str) -> str:
            return ab_now.get(name, name)

        fixed = {item.name for item in defs if item.name not in ab_now and item.name not in method_now}
        declared = {item.name for item in defs if item.kind != "mt" and item.name not in ab_now} | set(ab_now.values())
        method_names: dict[str, set[tuple]] = {}
        for item in defs:
            if item.kind != "mt":
                continue
            final = method_now.get(item.name, item.name)
            signature = tuple(tuple(renamed(text) for text in group) for group in item.signature)
            method_names.setdefault(final, set()).add((item.owner, signature))
        wanted: dict[str, list[str]] = {}
        for name, candidate in ab_now.items():
            wanted.setdefault(candidate, []).append(name)
        for name, candidate in sorted(ab_now.items()):
            rivals = [other for other in wanted[candidate] if other != name]
            identity = field_identity(by_name[name].module)
            if any(field_identity(by_name[other].module) == identity for other in rivals):
                unseparable.add(name)
                skip_owner(name, "the module path gives its rival the same name, so qualification cannot separate them: "
                           + ", ".join(sorted(rivals)))
                changed = True
                continue
            if candidate in fixed or candidate in method_names or rivals:
                if ab_index[name] + 1 < len(ab_options[name]):
                    ab_index[name] += 1
                else:
                    skip_owner(name, f"`{candidate}` is already declared")
                changed = True
        if changed:
            continue
        for name, candidate in sorted(method_now.items()):
            method = field_methods[name]
            signature = tuple(tuple(renamed(text) for text in group) for group in method.signature)
            others = {entry for entry in method_names.get(candidate, set()) if entry != (method.owner, signature)}
            sibling = any(owner == method.owner for owner, _ in others)
            foreign = any(owner != method.owner and other != signature for owner, other in others)
            if candidate in declared or sibling or foreign:
                if method_index[name] + 1 < len(method_options[name]):
                    method_index[name] += 1
                else:
                    del method_index[name]
                    skipped[name] = (
                        f"no free name: {', '.join(method_options[name])} "
                        "each name a declaration or another signature's method"
                    )
                changed = True
        if not changed:
            for name in list(method_index):
                owner = field_methods[name].owner
                if owner in unseparable:
                    del method_index[name]
                    skipped[name] = f"its owner `{owner}` is skipped: a pair qualification cannot separate"
                    changed = True

    abstractions = {name: ab_options[name][index] for name, index in ab_index.items()}
    abstractions = {name: new for name, new in abstractions.items() if new != name}
    methods = {name: method_options[name][index] for name, index in method_index.items()}
    methods = {name: new for name, new in methods.items() if new != name}
    taken = {item.name for item in defs} | set(abstractions.values()) | set(methods.values())
    for name in sorted(skipped):
        method = field_methods.get(name)
        if method is None or method.owner not in abstractions:
            continue
        follows = f"{abstractions[method.owner]}_{name[len(method.owner) + 1 :]}"
        if follows not in taken:
            methods[name] = follows
            taken.add(follows)
            skipped[name] += f"; its owner part follows the field: `{follows}`"
    return {
        "abstractions": dict(sorted(abstractions.items())),
        "methods": dict(sorted(methods.items())),
        "following": sorted(name for name in methods if name in skipped),
        "skipped": dict(sorted(skipped.items())),
        "checks": {name: checks[name] for name in sorted(abstractions) if name in checks},
    }


BARE_NAMES_EXEMPT = frozenset(
    {
        "Record_Observer_RecordUUID",
        "Record_Observer_RecordsUUID",
        "Storage_Observer_RecordUUID",
        "Record_UUID",
        "Storage_UUID",
    }
)
BARE_NAMES_COUNTER = re.compile(r"_2$")


def bare_from_module_qualified(name: str, module: str) -> str | None:
    """The plain name behind a module-qualified declaration, or None."""
    identities = [pascal_segment(part) for part in module_identity(module)]
    for identity in identities:
        prefix = identity + "_"
        if name.startswith(prefix) and len(name) > len(prefix):
            bare = name[len(prefix) :]
            if qualified_by_module(bare, name, module):
                return bare
    return None


def bare_from_owner_qualified(name: str, owner: str) -> str | None:
    """The plain name behind an owner-prefixed method, or None."""
    prefix = owner + "_"
    if name.startswith(prefix) and len(name) > len(prefix):
        return name[len(prefix) :]
    return None


def name_steps_up_module(bare: str, module: str) -> bool:
    """True when `bare` is the module path's own concept and must stay stepped up."""
    segments = [pascal_segment(part) for part in strip_protocol(module).split("/") if part]
    return bare in segments


def bare_names_skip_reason(name: str) -> str | None:
    if name in BARE_NAMES_EXEMPT:
        return "Record/Storage UUID pair; which module owns the concept is an owner question"
    if BARE_NAMES_COUNTER.search(name):
        return "`_2` name is a tool report, not kept"
    parts = split_field_name(name)
    if parts is not None and parts[0]:
        return "observer abstraction; use observer-names"
    return None


def bare_names_plan(texts: dict[str, str]) -> dict:
    """Strip module and owner prefixes when the bare name is unique.

    Abstractions lose one module-identity prefix when `qualified_by_module`
    says they carry it and the bare name is not another declaration. Methods
    lose their owner's prefix when the bare name is not another declaration or
    a method of another signature. Collisions, `_2` names, field abstractions,
    and the Record/Storage UUID pair are skipped.
    """
    defs = field_defs(texts)
    by_name = {item.name: item for item in defs}
    kinds = {item.name: item.kind for item in defs}
    skipped: dict[str, str] = {}
    for item in defs:
        reason = bare_names_skip_reason(item.name)
        if reason is not None:
            skipped[item.name] = reason

    ab_wants: dict[str, str] = {}
    for item in defs:
        if item.kind not in {"ab", "cp", "sc", "vr"} or item.name in skipped:
            continue
        bare = bare_from_module_qualified(item.name, item.module)
        if bare is None or bare == item.name:
            continue
        if name_steps_up_module(bare, item.module):
            skipped[item.name] = f"`{bare}` carries its module at `{item.module}`"
            continue
        ab_wants[item.name] = bare

    mt_wants: dict[str, str] = {}
    for item in defs:
        if item.kind != "mt" or item.name in skipped:
            continue
        bare = bare_from_owner_qualified(item.name, item.owner)
        if bare is None or bare == item.name:
            continue
        mt_wants[item.name] = bare

    def renamed(name: str) -> str:
        return ab_wants.get(name, mt_wants.get(name, name))

    fixed = {item.name for item in defs if item.name not in ab_wants and item.name not in mt_wants}
    declared = {item.name for item in defs if item.kind != "mt" and item.name not in ab_wants} | set(ab_wants.values())
    method_names: dict[str, set[tuple]] = {}
    for item in defs:
        if item.kind != "mt":
            continue
        final = mt_wants.get(item.name, item.name)
        owner = renamed(item.owner)
        signature = tuple(tuple(renamed(text) for text in group) for group in item.signature)
        method_names.setdefault(final, set()).add((owner, signature))

    changed = True
    while changed:
        changed = False
        wanted: dict[str, list[str]] = {}
        for name, candidate in ab_wants.items():
            wanted.setdefault(candidate, []).append(name)
        for name, candidate in sorted(ab_wants.items()):
            if candidate in fixed:
                skipped[name] = f"`{candidate}` is already declared"
                del ab_wants[name]
                changed = True
                continue
            if candidate in method_names:
                skipped[name] = f"`{candidate}` is already a method name"
                del ab_wants[name]
                changed = True
                continue
            rivals = [other for other in wanted[candidate] if other != name]
            if rivals:
                skipped[name] = f"`{candidate}` is wanted by " + ", ".join(sorted(rivals))
                del ab_wants[name]
                changed = True
        if changed:
            continue
        for name, candidate in sorted(mt_wants.items()):
            if candidate in declared:
                skipped[name] = f"`{candidate}` is already declared"
                del mt_wants[name]
                changed = True
                continue
            method = by_name[name]
            owner = renamed(method.owner)
            signature = tuple(tuple(renamed(text) for text in group) for group in method.signature)
            others = {entry for entry in method_names.get(candidate, set()) if entry != (owner, signature)}
            sibling = any(entry_owner == owner for entry_owner, _ in others)
            foreign = any(entry_owner != owner and entry_sig != signature for entry_owner, entry_sig in others)
            if sibling or foreign:
                skipped[name] = f"`{candidate}` is already a method of another signature"
                del mt_wants[name]
                changed = True

    abstractions = {name: new for name, new in ab_wants.items() if new != name}
    methods = {name: new for name, new in mt_wants.items() if new != name}
    collisions = sorted(
        {
            entry
            for entry in skipped.values()
            if entry.startswith("`") and " is already" in entry
        }
    )
    return {
        "abstractions": dict(sorted(abstractions.items())),
        "methods": dict(sorted(methods.items())),
        "skipped": dict(sorted(skipped.items())),
        "collisions": collisions,
    }


def rename_tokens(text: str, renames: dict[str, str]) -> str:
    """`text` with every whole identifier of `renames` renamed, in the Khayyam
    part only; the end-of-file Go blocks are left as their source."""
    if not renames:
        return text
    lines = text.split("\n")
    blocks = end_blocks(lines)
    cut = blocks[0].marker if blocks else len(lines)
    pattern = re.compile(
        r"(?<![A-Za-z0-9_])("
        + "|".join(re.escape(name) for name in sorted(renames, key=len, reverse=True))
        + r")(?![A-Za-z0-9_])"
    )
    head = [pattern.sub(lambda match: renames[match.group(1)], line) for line in lines[:cut]]
    return "\n".join([*head, *lines[cut:]])


def run_observer_names(
    memar_root: Path,
    values: Sequence[str] = (),
    excludes: Sequence[str] = TIDY_EXCLUDES,
    write: bool = False,
    frontend: bool = True,
) -> dict:
    memar_root = memar_root.resolve()
    originals: dict[str, str] = {}
    for relative in tidy_paths(values, memar_root, excludes):
        with (memar_root / relative).open(encoding="utf-8", newline="") as handle:
            originals[relative] = handle.read()
    texts = {relative: text.replace("\r\n", "\n") for relative, text in originals.items()}
    plan = observer_names_plan(texts)
    renames = {**plan["abstractions"], **plan["methods"]}
    changed: dict[str, str] = {}
    for relative, text in texts.items():
        renamed = rename_tokens(text, renames)
        if renamed != text:
            newline = "\r\n" if "\r\n" in originals[relative] else "\n"
            changed[relative] = renamed.replace("\n", newline)
    summary: dict = {
        "files": len(texts),
        "abstractions_renamed": len(plan["abstractions"]),
        "methods_renamed": len(plan["methods"]),
        "files_changed": sorted(changed),
        **plan,
    }
    if frontend:
        every = sorted(texts)
        before = frontend_outcomes(memar_root, every, {})
        after = frontend_outcomes(memar_root, every, changed)
        refused_before = {path for path, outcome in before.items() if outcome.get("outcome") == "refuse"}
        refused_after = {path for path, outcome in after.items() if outcome.get("outcome") == "refuse"}
        summary["frontend"] = {
            "before": {"accept": len(every) - len(refused_before), "refuse": len(refused_before)},
            "after": {"accept": len(every) - len(refused_after), "refuse": len(refused_after)},
            "newly_refused": {path: after[path] for path in sorted(refused_after - refused_before)},
        }
        if refused_after - refused_before:
            summary["written"] = False
            return summary
    if write:
        for relative, text in changed.items():
            with (memar_root / relative).open("w", encoding="utf-8", newline="") as handle:
                handle.write(text)
    summary["written"] = write
    return summary


def build_observer_names_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abstraction_bridge.py observer-names",
        description="Rename observer abstractions to Observer_<X> and their methods to the value they return.",
    )
    parser.add_argument("paths", nargs="*", help="repository-relative .kh files or directories (default: modules)")
    parser.add_argument("--memar-root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        help=f"repository-relative prefix to leave alone (repeatable; default {', '.join(TIDY_EXCLUDES)})",
    )
    parser.add_argument("--write", action="store_true", help="write; without it nothing is written")
    parser.add_argument("--no-frontend", action="store_true", help="skip the Khayyam frontend check")
    parser.add_argument("--samples", type=int, default=10, help="renames to print (default 10)")
    parser.add_argument("--report", help="write the machine readable report as JSON")
    return parser


def observer_names_main(argv: Sequence[str]) -> int:
    arguments = build_observer_names_parser().parse_args(list(argv))
    try:
        summary = run_observer_names(
            Path(arguments.memar_root),
            arguments.paths,
            TIDY_EXCLUDES if arguments.exclude is None else arguments.exclude,
            arguments.write,
            not arguments.no_frontend,
        )
    except BridgeFailure as error:
        for message in error.messages:
            print(f"error: {message}", file=sys.stderr)
        return 2
    if arguments.report:
        Path(arguments.report).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    state = "written" if summary["written"] else "dry" if not arguments.write else "refused"
    print(
        f"files {summary['files']}  changed {len(summary['files_changed'])}  "
        f"abstractions {summary['abstractions_renamed']}  methods {summary['methods_renamed']}  "
        f"skipped {len(summary['skipped'])}  {state}"
    )
    samples = [*summary["abstractions"].items(), *summary["methods"].items()][: arguments.samples]
    for old, new in samples:
        print(f"  {old} -> {new}")
    for name, reason in summary["skipped"].items():
        print(f"skipped {name}: {reason}")
    if "frontend" in summary:
        frontend = summary["frontend"]
        print(
            "frontend accept/refuse before {}/{}  after {}/{}".format(
                frontend["before"]["accept"], frontend["before"]["refuse"],
                frontend["after"]["accept"], frontend["after"]["refuse"],
            )
        )
        for path, outcome in frontend["newly_refused"].items():
            print(f"  newly refused {path}: {outcome.get('reason')} at line {outcome.get('line')}")
    return 1 if arguments.write and not summary["written"] else 0


def run_bare_names(
    memar_root: Path,
    values: Sequence[str] = (),
    excludes: Sequence[str] = TIDY_EXCLUDES,
    write: bool = False,
    frontend: bool = True,
) -> dict:
    memar_root = memar_root.resolve()
    originals: dict[str, str] = {}
    for relative in tidy_paths(values, memar_root, excludes):
        with (memar_root / relative).open(encoding="utf-8", newline="") as handle:
            originals[relative] = handle.read()
    texts = {relative: text.replace("\r\n", "\n") for relative, text in originals.items()}
    totals = {"abstractions": {}, "methods": {}, "skipped": {}, "collisions": []}
    changed: dict[str, str] = {}
    plan = bare_names_plan(texts)
    while True:
        renames = {**plan["abstractions"], **plan["methods"]}
        totals["abstractions"].update(plan["abstractions"])
        totals["methods"].update(plan["methods"])
        totals["skipped"] = dict(plan["skipped"])
        totals["collisions"] = sorted(set(totals["collisions"]) | set(plan["collisions"]))
        if not renames:
            break
        for relative, text in texts.items():
            renamed = rename_tokens(text, renames)
            if renamed != text:
                texts[relative] = renamed
                newline = "\r\n" if "\r\n" in originals[relative] else "\n"
                changed[relative] = renamed.replace("\n", newline)
        plan = bare_names_plan(texts)
    summary: dict = {
        "files": len(texts),
        "abstractions_renamed": len(totals["abstractions"]),
        "methods_renamed": len(totals["methods"]),
        "files_changed": sorted(changed),
        "abstractions": dict(sorted(totals["abstractions"].items())),
        "methods": dict(sorted(totals["methods"].items())),
        "skipped": dict(sorted(totals["skipped"].items())),
        "collisions": totals["collisions"],
    }
    if frontend:
        every = sorted(texts)
        before = frontend_outcomes(memar_root, every, {})
        after = frontend_outcomes(memar_root, every, changed)
        refused_before = {path for path, outcome in before.items() if outcome.get("outcome") == "refuse"}
        refused_after = {path for path, outcome in after.items() if outcome.get("outcome") == "refuse"}
        summary["frontend"] = {
            "before": {"accept": len(every) - len(refused_before), "refuse": len(refused_before)},
            "after": {"accept": len(every) - len(refused_after), "refuse": len(refused_after)},
            "newly_refused": {path: after[path] for path in sorted(refused_after - refused_before)},
        }
        if refused_after - refused_before:
            summary["written"] = False
            return summary
    if write:
        for relative, text in changed.items():
            with (memar_root / relative).open("w", encoding="utf-8", newline="") as handle:
                handle.write(text)
    summary["written"] = write
    return summary


def build_bare_names_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abstraction_bridge.py bare-names",
        description="Strip module and owner prefixes when the bare name is unique.",
    )
    parser.add_argument("paths", nargs="*", help="repository-relative .kh files or directories (default: modules)")
    parser.add_argument("--memar-root", default=".", help="repository root (default: current directory)")
    parser.add_argument(
        "--exclude",
        action="append",
        default=None,
        help=f"repository-relative prefix to leave alone (repeatable; default {', '.join(TIDY_EXCLUDES)})",
    )
    parser.add_argument("--write", action="store_true", help="write; without it nothing is written")
    parser.add_argument("--no-frontend", action="store_true", help="skip the Khayyam frontend check")
    parser.add_argument("--samples", type=int, default=10, help="renames to print (default 10)")
    parser.add_argument("--report", help="write the machine readable report as JSON")
    return parser


def bare_names_main(argv: Sequence[str]) -> int:
    arguments = build_bare_names_parser().parse_args(list(argv))
    try:
        summary = run_bare_names(
            Path(arguments.memar_root),
            arguments.paths,
            TIDY_EXCLUDES if arguments.exclude is None else arguments.exclude,
            arguments.write,
            not arguments.no_frontend,
        )
    except BridgeFailure as error:
        for message in error.messages:
            print(f"error: {message}", file=sys.stderr)
        return 2
    if arguments.report:
        Path(arguments.report).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    state = "written" if summary["written"] else "dry" if not arguments.write else "refused"
    print(
        f"files {summary['files']}  changed {len(summary['files_changed'])}  "
        f"abstractions {summary['abstractions_renamed']}  methods {summary['methods_renamed']}  "
        f"skipped {len(summary['skipped'])}  {state}"
    )
    samples = [*summary["abstractions"].items(), *summary["methods"].items()][: arguments.samples]
    for old, new in samples:
        print(f"  {old} -> {new}")
    for name, reason in summary["skipped"].items():
        print(f"skipped {name}: {reason}")
    if summary.get("collisions"):
        print("collisions:")
        for entry in summary["collisions"][: arguments.samples]:
            print(f"  {entry}")
    if "frontend" in summary:
        frontend = summary["frontend"]
        print(
            "frontend accept/refuse before {}/{}  after {}/{}".format(
                frontend["before"]["accept"], frontend["before"]["refuse"],
                frontend["after"]["accept"], frontend["after"]["refuse"],
            )
        )
        for path, outcome in frontend["newly_refused"].items():
            print(f"  newly refused {path}: {outcome.get('reason')} at line {outcome.get('line')}")
    return 1 if arguments.write and not summary["written"] else 0
