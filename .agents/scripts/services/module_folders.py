#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/module_folders.py — `memar module folders`: a module's role folders made inside a folder.

A module that carries more than one kind of work groups each kind in a folder
named for its role, so the module's root reads as a list of kinds rather than
of instances. Which roles there are, and what each holds, is
`modules/README.md`'s answer (its bullet "By role inside a module"); this file
holds the names only, in ROLE_FOLDERS, so making the folders is one act
rather than six a person or an agent types and mistypes. A role folder carries
its role's name exactly, which is why the names are taken from one constant
and never spelled at the call.

Making is all it does. A folder already there is left as it is, and nothing is
deleted or renamed: an empty folder in a module is a decision made visible
(`modules/README.md`), and one that is not wanted is removed by a person
through the tools that keep a deletion recoverable. A file standing where a
role folder would go is reported and left.

`session_new` asks the same of every session folder, so a session's work is
filed by kind from its first step, beside the plan and the report at its top.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, NamedTuple

FOLDERS_COMMAND = "folders"

ROLE_FOLDERS = ("protocol", "rules", "errors", "tests", "services", "docs")
"""The role folders a module groups its kinds of work in, each named exactly as its role.

`modules/README.md`, in its bullet "By role inside a module", owns what each
role means and which roles there are; the list is open there, and a role it
names is added here. `services/tests/module_folders.py` fails when the two
differ.
"""


class RoleFolders(NamedTuple):
    """What one call did inside a folder: the role folders it made, found there, and found a file in the way of."""

    made: list[str]
    present: list[str]
    blocked: list[str]


def ensure_role_folders(folder: Path) -> RoleFolders:
    """Make each role folder missing inside FOLDER; never delete, rename, or touch one that is there."""
    done = RoleFolders([], [], [])
    for role in ROLE_FOLDERS:
        path = folder / role
        if path.is_dir():
            done.present.append(role)
            continue
        try:
            path.mkdir()
        except FileExistsError:
            done.blocked.append(role)
            continue
        done.made.append(role)
    return done


def listed(roles: list[str] | tuple[str, ...]) -> str:
    """ROLES as folder names, e.g. `rules/, tests/`."""
    return ", ".join(f"{role}/" for role in roles)


def make_folders(path: str) -> int:
    """`folders`: make the missing role folders inside PATH and say what was made and what was there."""
    from machine.console import fail, note

    folder = Path(path)
    if not folder.is_dir():
        fail(f"{folder} is not a folder; name a folder that is there")
    done = ensure_role_folders(folder)
    note(f"in: {folder.resolve()}")
    if done.made:
        note(f"made: {listed(done.made)}")
    if done.present:
        note(f"already there: {listed(done.present)}")
    if done.blocked:
        note(f"not made, a file of that name is there: {listed(done.blocked)}")
    return 1 if done.blocked else 0


def describe(verbs) -> Callable[[argparse.Namespace], int]:
    """`memar module folders`."""
    maker = verbs.add_parser(
        FOLDERS_COMMAND,
        help="make a module's role folders inside a folder, the ones it lacks",
        description=(
            "Make inside the folder PATH each of a module's role folders it lacks:\n"
            f"{listed(ROLE_FOLDERS)}.\n"
            "A folder already there is left as it is; nothing is deleted or renamed.\n"
            "It prints what it made and what was already there. What each role holds\n"
            "is said in modules/README.md in the Memar checkout, under \"By role inside a\n"
            "module\"."
        ),
    )
    maker.add_argument("path", metavar="PATH", help="the folder to make them in; always given")
    return run


def run(args: argparse.Namespace) -> int:
    return make_folders(args.path)
