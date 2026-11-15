#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""router — the transitional registration bridge for the Python release.

Public calls are flat: `assemble` passes this legacy registration through `call_names.flat_parser`.
The describe/group contract below describes the internal compatibility bridge only. It is not the public CLI
or the intended Khayyam implementation. Explicit service Details take precedence over provisional legacy details;
the shared call-name operation owns the public lookup key. Loading this bridge in the Python server remains debt.

    memar <verb>              what it routes to; run `memar --help`
    memar --help              what Memar is, and the verbs its services declare

This file routes and nothing else, and it knows no verb: only which module holds
each domain. Every module of a domain, its own file and each file in its
`services/` folder, that has a command-line face declares it through one function,
`describe(verbs)`, the way every Memar type introduces itself
(modules/computer/type/protocol/detail.kh): the consumer calls only the method
it needs, and the declaration stays the one authority for what a verb accepts
and what its help says. A router that restated either would be a second
interface for one behavior, and the two would drift.

**The contract**, which every service with a command line keeps:

    describe(verbs) -> callable | None

`verbs` is where the module's verb goes: `memar`'s own verbs for a domain's
own file (`modules/process/task/task.py`), that domain verb's sub-verbs
for one of its capabilities (`modules/management/task/services/new.py`). It offers argparse's `add_parser`;
the service registers at most one verb on it, with its one-line summary as
`help` and, where it has one, its overview as `description`, adds the verb's
arguments, and returns
the callable that runs it — `run(args)`, given the parsed namespace, returning
an exit status or None for 0. A domain's run, where it returns one, runs before
its sub-verb's, so what every verb of a domain owes is said once. A module that
registers nothing and returns a callable asks to act before whichever verb is
routed — `before(argv)`, given the arguments as typed, even for `--help`, and
never failing the verb. `describe` does no work beyond declaring, and a module
that declares imports nothing heavy at module level, because every invocation
imports every service to assemble the command line.

**Two audiences, two texts.** `memar --help` is addressed to a person who has
Memar and wants to know what it is and what it does for them: it says what
Memar is, which is the command's own and so held here, and lists what the
services declare. The design above is addressed to whoever opens this file.

**Each help states its own work, and no sub-verb's** (owner, 2026-10-14). A
domain verb's overview says what the domain is, the words its sub-verbs share,
and what its own run does; argparse lists its sub-verbs under it, each with the
summary it declared, and each sub-verb's command lines, what it writes, and
when to use it are in that sub-verb's own `--help`. An overview that repeated
them grew with every sub-verb and drifted from each, and the reader who needs
one sub-verb paid for all of them. How a help is shaped beyond that waits for
the command module (`modules-plugable/computer/ui/command/`), which is not built on
until it is complete.

The name is the whole of the design. A framework whose entry point is a path
into a scripts folder asks every caller to know where it lives and what it is
called; `memar` asks for neither, so the same word works in a shell, in an
agent's command, in a CI step, and in a document that tells a reader what to
type.

**What it routes to is what Memar itself does**, and nothing else. A tool that
constrains a host tool the framework has no claim to does not belong on the
shelf — each `git_*` call's `--help` says why those verbs are a bundle's and not a path-invoked constraint script.

The active shell entry after install is `bin/memar` / `bin/memar.cmd`, which
starts the compiled release. This file is what the current release build still
copies as its entry, and a development entry when no release exists. The
command-line face lives in the `cli` part of the `memar_adaptor` bundle so the
server carries none of the shell surface.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""

from __future__ import annotations

import argparse
import functools
import importlib
import sys
from pathlib import Path
from typing import Callable, Iterable, NamedTuple

FACE = Path(__file__).resolve().parent
TOP = FACE.parent.parent.parent
SERVER = TOP / "bundles" / "memar"
if not (SERVER / "manifest.yaml").is_file():
    SERVER = FACE
SCRIPTS = SERVER
for folder in (TOP, FACE, SERVER, SERVER / "services"):
    if str(folder) not in sys.path:
        sys.path.insert(0, str(folder))

from machine.console import use_utf8_stdio

role_folders = importlib.import_module("bundles.memar.services.location.memar_location").role_folders
open = importlib.import_module("bundles.memar.services.memory.memory").open
_labels = importlib.import_module("modules.knowledge.label.primitive.declared_label").DeclaredLabel
# The modules a release declares are named by the program that started this process (the server does it before importing this file);
# a source run reads them from the manifest of the server bundle.
DECLARED = _labels.declared_modules() or importlib.import_module("modules.computer.software.edges.manifest.services.bundle_modules").modules_of(SERVER)
if not _labels.declared_modules():
    _labels.declare_modules(DECLARED)

SERVICES = "services"
# A module that is no domain still has its services: they go under a group of their own, named by the module (see `group_of`).
NO_DOMAIN = ""
DESCRIBE = "describe"
DECLARATIONS = "DECLARATIONS"
ROOTS = ("modules", "modules-plugable", "bundles")
SHELF = ("bundles", "memar", SERVICES)
# The face's own services (`memar memar_commands`) are verbs of the root, not of a domain.
FACE_HOME = "bundles/memar_adaptor/cli"
NOT_MODULES = frozenset({SERVICES, *role_folders(), "node_modules", "__pycache__"})
RUN_REF_PREFIX = "_memar_run_ref_"
JSON_FIELD = (type(None), bool, int, float, str, list, dict)
from face_policy import NOT_HANDED_OVER, run_ref
# A module that has a command-line face keeps it in a file named by its folder (`task/task.py`);
# each capability is a file in its `services/` folder. What the router works with is a path: the module's for its
# own file, and that path with `services` and the file's stem for a capability. A capability goes under the domain of
# the folder it is in, or under the domain whose last word, then this separator, begins its stem (`module_ensure_folders`
# goes under `module`); a folder's last word may be shared by a mirror and its original, so no word is a key.
DOMAIN_SEPARATOR = "_"
VERB_METAVAR = "<verb>"
HELP_WORDS = ("help",)
RUN_PREFIX = "_memar_run_"

ABOUT = """memar — Memar, a development framework whose model is written down

Memar keeps its design model, its rules, and its language sources as documents
in a checkout, and this is the one command that reaches them.

List every call with `memar memar_commands` (one flat name each, the same for CLI and MCP).
Each call's own `--help` defines the words that are its own."""

EPILOG = """List every call with `memar memar_commands`. Ask one call with `--help` for what it accepts.

Before deleting, moving, restoring, or committing files, read the applicable git or
filesystem service's help from the calls `memar memar_commands` lists.
For putting text into a file, use `memar content_write` and `memar content_edit`."""


class Verbs:
    """Where one level's verbs go: argparse's sub-parser registration, made on first use.

    A level whose services register nothing gets no verb group, so a domain verb
    that runs itself never asks for a sub-verb it has none of.
    """

    def __init__(self, parser: argparse.ArgumentParser, depth: int) -> None:
        self.parser = parser
        self.depth = depth
        self.group: argparse._SubParsersAction | None = None

    def add_parser(self, name: str, **kwargs) -> argparse.ArgumentParser:
        if self.group is None:
            self.group = self.parser.add_subparsers(
                title="verbs",
                dest=f"_memar_verb_{self.depth}",
                metavar=VERB_METAVAR,
                required=True,
            )
        kwargs.setdefault("formatter_class", argparse.RawDescriptionHelpFormatter)
        return self.group.add_parser(name, **kwargs)

    def registered(self) -> dict[str, argparse.ArgumentParser]:
        return dict(self.group.choices) if self.group is not None else {}


class Entry(NamedTuple):
    """One file that may declare verbs: where it is imported from, which domain it goes under, and how it is shown to a reader."""

    address: str
    domain: str | None
    shown: str


@functools.lru_cache(maxsize=None)
def placed(name: str) -> tuple[tuple[str, ...], str | None] | None:
    parts = name.split(".")
    if parts[0] not in ROOTS:
        return None
    # Service package: …/services/<name>/<name>.py — before twin detection, because
    # `services` is a role folder and would refuse a twin whose path holds it.
    # Not under the memar shelf: bundles/memar/services/<module>/<module>.py is a
    # shelf module twin, not a service of `bundles/memar`.
    if (
        len(parts) > 4
        and parts[-3] == SERVICES
        and parts[-1] == parts[-2]
        and not parts[-1].startswith("_")
        and tuple(parts[: len(SHELF)]) != SHELF
    ):
        folder, stem = parts[:-3], parts[-1]
    elif len(parts) > 2 and parts[-1] == parts[-2]:
        folder, stem = parts[:-1], None
    elif len(parts) > 3 and parts[-2] == SERVICES and not parts[-1].startswith("_"):
        folder, stem = parts[:-2], parts[-1]
    else:
        return None
    inside = folder[len(SHELF):] if tuple(folder[:len(SHELF)]) == SHELF else folder
    if len(folder) < 2 or NOT_MODULES.intersection(inside):
        return None
    return tuple(folder), stem


def parts_role(name: str) -> str:
    """The folder of a module's kind (`services`, `widgets`) it sits in."""
    parts = name.split(".")
    if len(parts) > 4 and parts[-3] == SERVICES and parts[-1] == parts[-2]:
        return SERVICES
    return parts[-2]


def group_of(key: str) -> str:
    """The word of the module an entry sits in: `a/b/status/widgets/x` is in `status`. A group is named by its module and by nothing a person wrote."""
    return key.rsplit("/", 2)[0].rsplit("/", 1)[-1]


@functools.lru_cache(maxsize=None)
def entries(names: tuple[str, ...] = DECLARED) -> dict[str, Entry]:
    domains: dict[str, tuple[str, str]] = {}
    shelved: list[tuple[str, str, str, str, str]] = []
    for name in names:
        spot = placed(name)
        if spot is None:
            continue
        folder, stem = spot
        key = "/".join(folder)
        if stem is None:
            domains[key] = (folder[-1], name)
        else:
            shelved.append((key, stem, name, folder[-1], parts_role(name)))
    found = {key: Entry(address, None, leaf) for key, (leaf, address) in domains.items()}
    for home, stem, address, leaf, role in sorted(shelved):
        if home == FACE_HOME:
            found[f"{home}/{role}/{stem}"] = Entry(address, None, stem)
            continue
        owners = [
            key for key, (word, _) in domains.items() if word != leaf and key != home and stem.startswith(word + DOMAIN_SEPARATOR)
        ]
        if len(owners) > 1:
            print(f"memar: {stem} begins the name of more than one domain, so it is left out: {', '.join(sorted(owners))}", file=sys.stderr)
            continue
        if owners:
            found[f"{home}/{role}/{stem}"] = Entry(address, owners[0], stem)
        else:
            # A twin domain file is optional: the folder leaf still names the
            # provisional Details.Domain for the flat call (CLI and MCP alike).
            found[f"{home}/{role}/{stem}"] = Entry(address, home, f"{leaf}{DOMAIN_SEPARATOR}{stem}")
    return found


def catalog(names: Iterable[str] = DECLARED) -> dict[str, str]:
    return {key: each.address for key, each in entries(tuple(names)).items()}


def domain_of(key: str, names: Iterable[str] = DECLARED) -> str | None:
    return entries(tuple(names))[key].domain


def services_of(word: str, names: Iterable[str] = DECLARED) -> list[str]:
    """Services whose provisional Domain leaf is WORD — with or without a twin file."""
    names = tuple(names)
    found = entries(names)
    homes = {key for key, each in found.items() if each.domain is None and each.shown == word}
    homes |= {
        each.domain
        for each in found.values()
        if each.domain and each.domain.rsplit("/", 1)[-1] == word
    }
    return [key for key in services(names) if key in homes or found[key].domain in homes]


def services(names: Iterable[str] = DECLARED) -> list[str]:
    found = entries(tuple(names))
    return sorted(found, key=lambda key: (found[key].domain is not None, found[key].shown, key))


def import_path(name: str, names: dict[str, str] | None = None) -> str:
    return (catalog() if names is None else names)[name]


def _silent_group(root: Verbs, levels: dict[str, Verbs], home: str, word: str) -> Verbs:
    """Legacy nesting for flat_parser only: not advertised; public calls stay flat."""
    held = levels.get(home)
    if held is not None:
        return held
    levels[home] = Verbs(root.add_parser(word, help=argparse.SUPPRESS), 1)
    return levels[home]


def _assemble_legacy(
    names: Iterable[str],
    load: Callable[[str], object] = lambda name: importlib.import_module(import_path(name)),
    domain: Callable[[str], str | None] = domain_of,
) -> tuple[argparse.ArgumentParser, list[Callable[[list[str]], None]]]:
    """The command line the shelf entries declare, and what asks to run before every verb.

    Pure apart from importing: no entry does any work while describing itself.
    An entry that fails to import is named on stderr and left out, so one broken
    entry costs its own verbs, never `memar --help` or the verb that repairs it.
    Domain twin files need not declare a public group: a silent group is made so
    flat call names keep Details.Domain from the folder leaf.
    """
    top = argparse.ArgumentParser(
        prog="memar",
        description=ABOUT,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    root = Verbs(top, 0)
    levels: dict[str, Verbs] = {}
    before: list[Callable[[list[str]], None]] = []
    for name in names:
        try:
            loaded = load(name)
        except Exception as failed:
            print(
                f"memar: {name} did not load, so its verbs are missing: "
                f"{type(failed).__name__}: {failed}",
                file=sys.stderr,
            )
            continue
        describe = getattr(loaded, DESCRIBE, None)
        declared = getattr(loaded, DECLARATIONS, ())
        derive = importlib.import_module("bundles.memar_adaptor.cli.derive") if declared and describe is None else None
        describers = [describe] if describe is not None else [derive.describer(each) for each in declared]
        for describe in describers:
            home = domain(name)
            if home is None:
                verbs = root
            elif home == NO_DOMAIN:
                word = group_of(name)
                verbs = _silent_group(root, levels, f"{NO_DOMAIN}:{word}", word)
            else:
                word = home.rsplit("/", 1)[-1]
                verbs = _silent_group(root, levels, home, word)
            known = verbs.registered()
            try:
                run = describe(verbs)
            except (argparse.ArgumentError, ValueError) as clash:
                print(f"memar: {name} could not declare its verb, so it is missing: {clash}", file=sys.stderr)
                continue
            added = {key: parser for key, parser in verbs.registered().items() if key not in known}
            if not added:
                if run is not None:
                    before.append(run)
                continue
            for parser in {id(parser): parser for parser in added.values()}.values():
                if run is not None:
                    parser.set_defaults(
                        **{
                            f"{RUN_PREFIX}{verbs.depth}": run,
                            f"{RUN_REF_PREFIX}{verbs.depth}": run_ref(run),
                        }
                    )
                if home is None:
                    levels[name] = Verbs(parser, verbs.depth + 1)
    return top, before


def assemble(
    names: Iterable[str],
    load: Callable[[str], object] = lambda name: importlib.import_module(import_path(name)),
    domain: Callable[[str], str | None] = domain_of,
) -> tuple[argparse.ArgumentParser, list[Callable[[list[str]], None]]]:
    from bundles.memar_adaptor.cli.call_names import flat_parser
    parser, before = _assemble_legacy(names, load, domain)
    return flat_parser(parser), before


def runs(parsed: argparse.Namespace) -> list[Callable[[argparse.Namespace], int | None]]:
    """The runs the parsed verbs declared, outermost first."""
    found = {
        int(key[len(RUN_PREFIX):]): value
        for key, value in vars(parsed).items()
        if key.startswith(RUN_PREFIX) and not key.startswith(RUN_REF_PREFIX)
    }
    return [found[depth] for depth in sorted(found)]


def run_refs(parsed: argparse.Namespace) -> list[str]:
    found = {
        int(key[len(RUN_REF_PREFIX):]): value
        for key, value in vars(parsed).items()
        if key.startswith(RUN_REF_PREFIX)
    }
    return [found[depth] for depth in sorted(found)]


def fields_of(parsed: argparse.Namespace) -> dict:
    out = {}
    for key, value in vars(parsed).items():
        if key.startswith(RUN_PREFIX) or key.startswith(RUN_REF_PREFIX):
            continue
        if isinstance(value, JSON_FIELD):
            out[key] = value
    return out


def server_call(parsed: argparse.Namespace, *, cwd: str | None = None, env: dict | None = None, stdin: str = "") -> dict:
    import os

    return {
        "fields": fields_of(parsed),
        "runs": run_refs(parsed),
        "cwd": os.getcwd() if cwd is None else cwd,
        "env": dict(os.environ) if env is None else env,
        "stdin": stdin,
    }


def apply(parsed: argparse.Namespace) -> int:
    for run in runs(parsed):
        code = run(parsed)
        if code:
            return code
    return 0


def main(argv: list[str] | None = None) -> int:
    use_utf8_stdio()
    args = list(sys.argv[1:] if argv is None else argv)
    top, before = assemble(services())
    for step in before:
        step(args)
    if args[:1] and args[0] in HELP_WORDS:
        args = ["--help", *args[1:]]
    return apply(top.parse_args(args))


@functools.lru_cache(maxsize=1)
def assembled() -> tuple[argparse.ArgumentParser, list[Callable[[list[str]], None]]]:
    """The command line, composed once: a process that stays answers many calls from one composition."""
    return assemble(services())


def parsed_of(args: list[str]) -> argparse.Namespace:
    """The namespace the command line PARSES ARGS into; `--help` and a wrong call end in SystemExit, as argparse does."""
    top, before = assembled()
    args = list(args)
    for step in before:
        step(args)
    if args[:1] and args[0] in HELP_WORDS:
        args = ["--help", *args[1:]]
    return top.parse_args(args)


def in_place(args: list[str]) -> int:
    """The call as typed, run in this process."""
    use_utf8_stdio()
    return apply(parsed_of(args))


