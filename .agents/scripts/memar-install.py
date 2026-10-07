#!/usr/bin/env python3
"""Record where Memar lives, then settle the machine and everything around it.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar install --help` prints: it is addressed to whoever is
putting Memar on a machine, and it says what the run does and what the person
must do afterwards, and stops. Everything from here down is addressed to whoever
opens this file, and it is here rather than in the help output because the
person running the install has no use for the mechanism that performs it. The
help is the interface; this is the reasoning behind it, and a module that
printed its own reasoning to its caller would be a caller reading the same text
twice.

This file is the run, and the bootstrap's only step once it holds the
architecture: `install.sh` and `install.ps1` obtain Memar — the repository is a
git checkout, so obtaining it is a clone — and then run this from that checkout,
where the rest of the architecture sits on disk beside this file, some of it on a
shelf below. What this does is held one concern per file, and each is asked rather
than repeated here: `memar_repository.py` what a Memar repository is,
`machine/env_location.py` what the location variable says and where that variable
lives, `machine/fs_target.py` the folder this run would use, `machine/fs_lock.py` two
sessions at once, `machine/fs_memar.py` where the checkout and its scratch live,
`editor_extension.py` the editor extensions, and `memar_console.py` how a step is
printed.

**A bare run installs everything, in the only order that works.** Three layers:
onto the machine (the variable, the command on `PATH`, the editor extensions);
into the project this is run from, when the directory is one; and into the agent
apps this machine has, when the machine layer has left a location to copy from.
The order is not a preference — the third layer needs the root the first one
writes, so a project that is not under version control is simply reported and
skipped while the rest still runs, and a run with nothing to do in one layer is
not a failure of the run. What it never does is go beyond installing: obtaining
the checkout belongs to the bootstrap, and a bare run does not create a
repository, edit a version-control configuration, or touch anything else it was
not asked about.

One mechanism decides where Memar lives: the MEMAR_ROOT environment variable.
This script writes it, for the current user, persistently, and reads it back for
everything that needs to know where Memar is. Nothing else decides it, and
nothing keeps a second copy of the repository. What the variable says is what
the platform's record of it says, not merely what this process was started with:
a session that opened before the value was written still finds it.

Obtaining the repository is not here, and the reason is where it belongs: the
bootstrap is what puts a checkout on a machine, and this file is only ever run
from one. So what is left is the recording, and there is one mode of it named
here:

  Record a Memar folder that already exists where you want it, without moving
  or copying anything, and then put Memar into this project and into the agent
  apps as well:

      memar-install.py --register ~/GeniusesGroup/memar

And one question, asked on its own — it writes nothing, clones nothing, and
touches neither the variable nor the editor:

      memar-install.py --check /tmp/Memar

With neither: with MEMAR_ROOT already naming a Memar repository, this says where
Memar is and stops, so re-running costs nothing; with nothing recorded, this
records the checkout this file is in, which is the one the bootstrap obtained and
the only one a file in this folder can name. With nothing recorded and nothing
holding a repository, this refuses and says so.

What recording does, and then what the run does around it:

  - writes MEMAR_ROOT for the current user, into that user's shell profile on
    POSIX and into the registry-backed user environment on Windows, so it
    survives the session;
  - puts the `memar` command on the user's PATH;
  - installs the editor extensions that checkout ships, under the names their
    own manifests give, writing the checkout's copy over any it installed before;
  - asks `memar-install-agents.py` to put Memar into the current project when
    the current directory is one, and `memar-install-apps.py` to copy the skill
    into the agent apps this machine has — each declaring its own interface;
  - prints the value it wrote and where it wrote it.

`--check` stops before all of that and writes nothing. The two "into" layers are
separately runnable when only one of them is wanted, and their own `--help`
says so.

A folder that is not a Memar repository is refused, so the variable is never
pointed at an arbitrary directory. A destination under a temporary directory is
refused for the same reason: a copy there is machine-local and does not survive,
which is the failure this script exists to prevent. --check prints the folder,
the temporary directory the refusal is decided against, and the refusal an
install would print — or that there would be none. It writes nothing, clones
nothing, and touches neither the variable nor the editor, so the refusal can be
proved on a machine that is already installed.

Two sessions arriving at once never record one folder at once: the recording is
taken under a lock file, and it is idempotent, so the second waits and then
finds the work already done.

MEMAR_ROOT takes effect for programs started *after* it is written. Other
programs — your editor, your shell, this session's parent — must be restarted
before they see it: a running program does not read a new value. This process
sets it for itself so it can go on. When this process's own copy disagrees with
the record, the record is used and the disagreement is printed.

Needs Python 3 and the modules this file is split into beside it. A bootstrap
sits beside this one (install.sh, install.ps1): it obtains the checkout and then
runs this from it. Run this directly if you have a checkout of your own.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


from memar_console import fail, note, step, use_utf8_stdio
from machine.editor_extension import install_extensions
from memar_repository import is_memar_repository, not_a_repository
from machine.env_location import (
    VARIABLE,
    recorded_root,
    recorded_value,
    refuse_bogus_value,
    resolve_root,
    write_user_variable,
)
from machine.env_path import ensure_on_path
from machine.fs_lock import lock_path, release_lock, take_lock
from machine.fs_memar import checkout_root, memar_root
from machine.fs_target import default_target, full_path, refuse_temporary, temporary_directory

LAUNCHER = "memar"
# The two files that put Memar into a project and into the agent apps. They are
# run as children rather than imported, because a hyphen is not a legal module
# name: a file named for a domain and a subject keeps the hyphen that names it
# domain-first, and pays for it by being run rather than imported. Asking a
# child process is the same composition `host/git.py` does with `host/fs.py`, and
# it has the second virtue that each of the three stays independently runnable.
INTO_PROJECT = Path(__file__).resolve().parent / "memar-install-agents.py"
INTO_APPS = Path(__file__).resolve().parent / "memar-install-apps.py"


def temporary_consequence() -> str:
    """What refusing an install's target under the temporary directory says."""
    return (
        "Memar installed there would be machine-local and would not survive. "
        f"Name a folder that persists, such as {default_target()}."
    )


def report_installed(path: Path) -> None:
    """Say where Memar is already, and bring the editor up to that checkout.

    The bootstrap scripts used to make this decision in their own dialect, before
    this file existed as the one that answers for every entry point alike. They
    do not decide anything now: they make sure git and Python are here, obtain
    the checkout, and then run this file. So the question whether Memar is
    already on this machine is asked here, against the record, and not by a shell
    reading a copy of the variable that a session opened earlier may not hold.

    A re-run costs nothing, so it also writes this checkout's editor extension
    over the installed one: re-running is how an agent updates the editor after
    a change, and a run that only reported would leave the editor on the code it
    was first given.
    """
    step(f"Memar is already installed at {path}")
    note(f"{VARIABLE} = {path}")
    install_extensions(path)


def record(target: Path) -> None:
    if not is_memar_repository(target):
        fail(
            f"{not_a_repository(target)}, so {VARIABLE} was not written. Nothing "
            f"was deleted."
        )
    step("Recorded the location")
    where = write_user_variable(str(target))
    # For this process, so this run can go on. Other programs still need the
    # restart the message below names.
    os.environ[VARIABLE] = str(target)
    note(f"{VARIABLE} = {target}")
    note(f"written to {where}")
    note("other programs must be restarted before they see it")

    step("The memar command")
    for line in ensure_on_path(
        target / ".agents" / "scripts",
        lambda d: (d / LAUNCHER).is_file(),
    ):
        note(line)

    step("Editor extensions")
    install_extensions(target)

    step(f"Memar is registered at {target}")


def run_child(script: Path, arguments: list[str], label: str) -> int:
    """Ask one of the two "into" layers to do its part, and say what it did.

    A child process rather than an import, because these files carry a hyphen and
    that is what a hyphenated name costs its owner: each stays a command a person
    can run on its own, and the composition is stated here where the order lives
    rather than being implied by an import.

    The child's own output is not captured, so what it says reaches the reader as
    it happens — this layer is running, not inspecting, and a swallowed copy of
    a child's report would be a second interface for one act. Its exit status is
    returned rather than raised, because a layer that cannot apply is not a
    broken install: a directory that is not a project, or a machine with no agent
    apps, is a fact about this machine and the remaining layers still belong to
    the run.
    """
    step(label)
    return subprocess.run([sys.executable, str(script), *arguments]).returncode


def into_project_and_apps(arguments: list[str] | None = None) -> None:
    """Put Memar into this project and into the agent apps, in that order.

    The order is the dependency, not a preference: copying the skill into the
    apps needs the location the machine layer records, and the apps layer says
    so and stops when there is none. The project layer comes first because it is
    the one that can be skipped without a second thought — a checkout is not a
    project, and `memar-install-agents.py` already refuses the home directory.
    """
    run_child(INTO_PROJECT, list(arguments or []), "Into this project")
    run_child(INTO_APPS, list(arguments or []), "Into the agent apps")


def register(path: str, arguments: list[str] | None = None) -> None:
    """Record PATH as where Memar lives, then finish the rest of the install.

    Nothing is moved, copied, cloned, or deleted here: the bootstrap has already
    obtained the checkout — a clone, a pull, or the one the user pointed at — so
    what is left is to write down where it is, and everything the machine needs
    beside it. Whether PATH is a Memar repository is asked here, through the
    module that holds the test, and a folder that is not one is refused.
    """
    target = full_path(path)
    refuse_temporary(
        target,
        "Memar registered from there would not survive the machine's housekeeping.",
    )
    refuse_bogus_value()
    step("Memar location")
    note(f"target: {target}")
    note("mode: register (the bootstrap obtained this checkout)")
    lock = lock_path(target)
    take_lock(lock)
    try:
        record(target)
    finally:
        release_lock(lock)
    into_project_and_apps(arguments)


def check(path: str) -> None:
    """Ask the temporary-directory check a question, and stop.

    The refusal printed here is the refusal a record would print, because it is
    the refusal, and nothing after it runs: no clone, no write to the variable,
    nothing written to the editor. That is what makes the refusal provable on a
    machine that already has Memar on it.
    """
    target = full_path(path)
    step("Checking a target")
    note(f"target: {target}")
    note(f"temporary directory: {temporary_directory()}")
    refuse_temporary(target, temporary_consequence())
    note("not refused: that folder is not under the temporary directory")


def print_root() -> None:
    """Print where Memar is, and nothing else.

    A program that needs to find Memar has three ways to learn where it is, and
    this is the one that survives all of them. A recorded environment variable
    answers only when the program was started after the install and after the
    shell read it; a path typed into a configuration answers only while that
    configuration is intact. Asking the installed command answers by definition,
    because the command is the thing installed — the same reason `go env GOROOT`
    is how a program asks a Go toolchain where it lives rather than reading a
    variable the toolchain also writes.

    It lives here rather than among the content verbs because it is not about
    content: where Memar lives is what the installer decides, so this is the
    installer's own question. One line on stdout and nothing else, so it can be
    captured by substitution without parsing.
    """
    print(memar_root())


DESCRIPTION = """memar install — put Memar on this machine, and into this project

One run installs three layers, in the only order that works:

  - onto this machine: where Memar lives, the `memar` command on your PATH, and
    the editor extensions this checkout ships;
  - into the project you run it from, if the directory is one;
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
    memar install --machine-only          settle this machine and skip the project and the apps
"""


def main() -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
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
    args = parser.parse_args()
    if args.check:
        check(args.check)
        return 0
    if args.root:
        print_root()
        return 0
    forwarded: list[str] = []
    if args.dry_run:
        forwarded.append("--dry-run")
    if args.register:
        register(args.register, forwarded)
        return 0
    # A named folder is a deliberate act and is carried out. With none named, the
    # only question left is whether Memar is already on this machine, and it is
    # answered against the record rather than by a caller that may hold a stale
    # copy of the variable.
    installed = recorded_root()
    if installed is not None:
        report_installed(installed)
        # An existing install is exactly the case where the project and app
        # layers are wanted: re-running is how a project picks up a change made
        # in the checkout it was installed from.
        if not args.machine_only:
            into_project_and_apps(forwarded)
        return 0
    # Nothing is recorded, or nothing recorded is a Memar repository, and
    # refuse_bogus_value has said so about the second case. What is left to
    # record is the checkout this file is in.
    register(str(checkout_root()), forwarded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


if __name__ == "__main__":
    main()
