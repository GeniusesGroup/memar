#!/usr/bin/env python3
"""Record where Memar lives, and settle the machine around that checkout.

This file is the run, and the bootstrap's only step once it holds the
architecture: `install.sh` and `install.ps1` obtain Memar — the repository is a
git checkout, so obtaining it is a clone — and then run this from that checkout,
where the rest of the architecture sits on disk beside this file and an import
of a sibling is answered from there. What this does is held one concern per file
beside it, and each is asked rather than repeated here: `memar_repository.py` what
a Memar repository is, `sys_env_location.py` what the location variable says and
where that variable lives, `sys_fs_target.py` the folder this run would use,
`sys_fs_lock.py` two sessions at once, `sys_desktop_shortcut.py` the Desktop
entry, `editor_extension.py` the editor extensions, and `console.py` how a step
is printed. `memar-documentation.py`, `install-apps.py`
and `install-agents.py` import this module, which is the folder's name for the
one place that decides.

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
  or copying anything:

      install.py --register ~/GeniusesGroup/memar

And one question, asked on its own:

      install.py --check /tmp/Memar

With neither: with MEMAR_ROOT already naming a Memar repository, this says where
Memar is and stops, so re-running costs nothing; with nothing recorded, this
records the checkout this file is in, which is the one the bootstrap obtained and
the only one a file in this folder can name. With nothing recorded and nothing
holding a repository, this refuses and says so.

What recording does:

  - writes MEMAR_ROOT for the current user, into that user's shell profile on
    POSIX and into the registry-backed user environment on Windows, so it
    survives the session;
  - creates a shortcut named "Memar" on your Desktop pointing at that folder;
  - installs the editor extensions that checkout ships, under the names their
    own manifests give, writing the checkout's copy over any it installed before;
  - prints the value it wrote and where it wrote it.

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
from pathlib import Path

# The names below are also the folder's public face of this set, which is why
# several of them are imported without being used here: install-agents.py,
# install-apps.py and memar-documentation.py all say `import install`, because
# install is what
# this folder means by the one place that reads and writes MEMAR_ROOT. Splitting
# the file must not move a name out from under them.
from console import fail, note, step, use_utf8_stdio
from copy_excluded import NEVER_COPIED
from editor_extension import install_extensions
from memar_repository import is_memar_repository, not_a_repository
from sys_desktop_shortcut import create_shortcut
from sys_env_location import (
    VARIABLE,
    recorded_root,
    recorded_value,
    refuse_bogus_value,
    resolve_root,
    write_user_variable,
)
from sys_fs_lock import lock_path, release_lock, take_lock
from sys_fs_target import default_target, full_path, refuse_temporary, temporary_directory

__all__ = [
    "NEVER_COPIED",
    "VARIABLE",
    "is_memar_repository",
    "not_a_repository",
    "recorded_root",
    "recorded_value",
    "refuse_bogus_value",
    "resolve_root",
    "use_utf8_stdio",
]


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


def checkout_root() -> Path:
    """The checkout this file is in: two levels up from the scripts folder.

    The one place a run of this file can name a checkout without being told one,
    which is what a no-argument run records: the bootstrap obtained that
    checkout, and a file inside it is the only thing that knows its own root.
    """
    return Path(__file__).resolve().parents[2]


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

    step("Shortcut")
    made = create_shortcut(target)
    if made:
        note(made)

    step("Editor extensions")
    install_extensions(target)

    step(f"Memar is registered at {target}")


def register(path: str) -> None:
    """Record PATH as where Memar lives.

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


def main() -> None:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=__doc__,
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
    args = parser.parse_args()
    if args.check:
        check(args.check)
        return
    if args.register:
        register(args.register)
        return
    # A named folder is a deliberate act and is carried out. With none named, the
    # only question left is whether Memar is already on this machine, and it is
    # answered against the record rather than by a caller that may hold a stale
    # copy of the variable.
    installed = recorded_root()
    if installed is not None:
        report_installed(installed)
        return
    # Nothing is recorded, or nothing recorded is a Memar repository, and
    # refuse_bogus_value has said so about the second case. What is left to
    # record is the checkout this file is in.
    register(str(checkout_root()))


if __name__ == "__main__":
    main()
