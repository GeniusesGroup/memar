#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar/install/install.py — `memar install`: record where Memar lives, then settle the machine and everything around it.

**Two audiences, two texts, and this file is where each lives.** `description`
below is what `memar install --help` prints: it is addressed to whoever is
putting Memar on a machine, and it says what the run does and what the person
must do afterwards, and stops. Everything from here down is addressed to whoever
opens this file, and it is here rather than in the help output because the
person running the install has no use for the mechanism that performs it. The
help is the interface; this is the reasoning behind it, and a module that
printed its own reasoning to its caller would be a caller reading the same text
twice.

This verb is the bootstrap's only step once it holds the architecture:
`install.sh` and `install.ps1` obtain Memar — the repository is a git checkout,
so obtaining it is a clone — and then hand the run to `memar install` in that
checkout, where the rest of the architecture sits on disk.

**A bare run installs everything, in the only order that works.** Three layers,
one service each: onto the machine (`install_machine`: the variable, the command
on `PATH`, the editor extensions); into the project this is run from, when the
directory is one (`install_project`); and into the agent apps this machine has,
when the machine layer has left a location to copy from (`install_apps`). The
order is not a preference — the third layer needs the root the first one
writes, so a project that is not under version control is simply reported and
skipped while the rest still runs, and a run with nothing to do in one layer is
not a failure of the run. What it never does is go beyond installing: obtaining
the checkout belongs to the bootstrap, and a bare run does not create a
repository, edit a version-control configuration, or touch anything else it was
not asked about.

This file holds the verb and that order, and nothing a layer does. It imports
the layers only when the verb runs, because every `memar` invocation imports
this file to learn what `install` accepts.

The layers are asked in this process. They were once run files, asked as child
processes because a hyphenated name cannot be imported; as services they are
imported, and `ask_layer` keeps what the child process gave the run. A layer
that stops — a directory that is not a project, a machine with no agent apps —
stops only itself, says why on stderr as it did as a child, and the remaining
layers still belong to the run: that is a fact about this machine, not a broken
install. Its output reaches the reader as it happens, uncaptured. The location
the machine layer records is set in this process's environment, so the layers
after it see it as the children saw it in theirs.

With neither a folder nor a question named: with MEMAR_ROOT already naming a
Memar repository, this says where Memar is and stops, so re-running costs
nothing; with nothing recorded, this records the checkout this file is in, which
is the one the bootstrap obtained and the only one a file in this folder can
name. With nothing recorded and nothing holding a repository, this refuses and
says so. `--register` records a Memar folder that already exists where you want
it, without moving or copying anything, and then puts Memar into this project
and into the agent apps as well; `--check` asks the machine layer whether a
folder would be refused, and writes nothing, clones nothing, and touches neither
the variable nor the editor.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import sys
import traceback
from typing import Callable

VERB = "install"
SUMMARY = "put Memar on this machine, and into the project you name"

def description() -> str:
    """What `memar install --help` prints; built when the verb runs, so the two project flags come from their types without a top-level import."""
    from modules.process.project.primitive.project_name import ProjectName
    from modules.process.project.primitive.project_path import ProjectPath

    return f"""memar install — put Memar on this machine, and into the project you name

One run installs three layers, in the only order that works:

  - onto this machine: where Memar lives, the `memar` command on your PATH, and
    the editor extensions this checkout ships;
  - into the project you name with {ProjectName.either_words()}, if it is one,
    and the project is registered with Memar under its folder's name (a project
    already registered is left as it is; a name another project holds is
    reported, and nothing is renamed);
    the folder you run it from is never read, so with none named this layer says so;
  - into the AI agent apps this machine has.

Each layer prints what it did. Running it again is safe and costs nothing: a
layer with nothing to do says so.

If Memar is already installed, a bare run says where it is and stops.

What you must do afterwards: **restart your shell and your editor.** Where Memar
lives is written as an environment variable, and a program that was already
running when it was written does not read it.

This needs Python 3 and a Memar checkout. If you do not have one, run
`install.sh` (POSIX) or `install.ps1` (Windows) first — those fetch the
checkout, and this runs from inside it.

Getting Memar somewhere else, or asking whether a folder would be accepted:

    memar install --register ~/src/memar   point Memar at a checkout you already have
    memar install --check /tmp/Memar       would an install there be refused? writes nothing
    memar install --root                  print where Memar is, one line
    memar install {ProjectName.FLAG} {ProjectName.METAVAR}           also put Memar into that project: a name `memar project`
                                          knows
    memar install {ProjectPath.FLAG} {ProjectPath.METAVAR}     also put Memar into the project whose folder is {ProjectPath.METAVAR}
    memar install --machine-only          settle this machine and skip the project and the apps
    memar install --developer             you develop Memar in this checkout: no update moves it
"""


def ask_layer(answer: Callable[[], object]) -> int:
    """Run one layer in this process; the exit status it would have ended a process with.

    A layer refuses the way a command does, by `sys.exit` with its reason, so the
    reason is printed on stderr as the interpreter would have printed it, and a
    layer that breaks prints its traceback there; neither stops the caller.
    """
    try:
        answer()
    except SystemExit as stopped:
        if stopped.code is None:
            return 0
        if isinstance(stopped.code, int):
            return stopped.code
        print(stopped.code, file=sys.stderr)
        return 1
    except Exception:  # noqa: BLE001 - a broken layer must not cost the run the layers after it
        traceback.print_exc()
        return 1
    return 0


def into_project_and_apps(project=None, *, dry_run: bool = False) -> None:
    """Put Memar into PROJECT, when one is named, and into the agent apps, in that order.

    The order is the dependency, not a preference: copying the skill into the
    apps needs the location the machine layer records, and the apps layer says
    so and stops when there is none. The project layer comes first because it is
    the one that can be skipped without a second thought — a checkout is not a
    project, and `install_project` already refuses the home directory.
    """
    from machine.console import step
    from bundles.memar.install.services import apps as install_apps
    from bundles.memar.install.services import project as install_project

    step("Into this project")
    ask_layer(lambda: install_project.into_project(project, dry_run=dry_run))
    step("Into the agent apps")
    ask_layer(lambda: install_apps.into_apps(dry_run=dry_run))


def run(args: argparse.Namespace) -> int:
    from machine.env_location import recorded_root
    from machine.fs_memar import checkout_root
    from bundles.memar.install.services import machine

    from modules.process.project.services.find import project_from_args

    project = project_from_args(args)
    if args.check:
        machine.check(args.check)
        return 0
    if args.root:
        machine.print_root()
        return 0
    if args.developer:
        machine.mark_developer()
        return 0
    if args.register:
        machine.register(args.register)
        into_project_and_apps(project, dry_run=args.dry_run)
        return 0
    # A named folder is a deliberate act and is carried out. With none named, the
    # only question left is whether Memar is already on this machine, and it is
    # answered against the record rather than by a caller that may hold a stale
    # copy of the variable.
    installed = recorded_root()
    if installed is not None:
        machine.report_installed(installed)
        # An existing install is exactly the case where the project and app
        # layers are wanted: re-running is how a project picks up a change made
        # in the checkout it was installed from.
        if not args.machine_only:
            into_project_and_apps(project, dry_run=args.dry_run)
        return 0
    # Nothing is recorded, or nothing recorded is a Memar repository, and
    # refuse_bogus_value has said so about the second case. What is left to
    # record is the checkout this file is in.
    machine.register(str(checkout_root()))
    into_project_and_apps(project, dry_run=args.dry_run)
    return 0


def describe(verbs) -> Callable[[argparse.Namespace], int]:
    parser = verbs.add_parser(VERB, help=SUMMARY, description=description())
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--register",
        metavar="PATH",
        help="record PATH as where Memar lives; it must be a Memar repository",
    )
    group.add_argument(
        "--check",
        metavar="PATH",
        help="say whether PATH would be refused as temporary, and stop",
    )
    group.add_argument(
        "--root",
        action="store_true",
        help="print where Memar is, one line, and stop; for a program that "
             "needs to find it",
    )
    group.add_argument(
        "--developer",
        action="store_true",
        help="mark the checkout Memar is recorded at as one you develop, so the "
             "daily update never moves it, and stop",
    )
    from modules.process.project.services.find import add_project_flags

    add_project_flags(
        parser,
        "the project to put Memar into; without either no project is written, and the folder the "
        "command runs in is not read",
    )
    parser.add_argument(
        "--machine-only",
        action="store_true",
        help="settle the machine and stop; skip this project and the agent apps",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="passed to the project and app layers, which print what they would "
             "write instead of writing it; the machine layer is never dry, "
             "because refusing to record a location is not a dry run of one",
    )
    return run
