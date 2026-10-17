#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/computer/module/services/folders.py — `memar module folders`: a module's role folders made inside a folder.

A module that carries more than one kind of work groups each kind in a folder
named for its role, so the module's root reads as a list of kinds rather than
of instances. Which roles there are, and what each holds and does not, is
declared here once, in `Role`: the name, what the folder holds, and what it does
not. `modules/README.md` names the roles and points here, and `memar module
folders --help` prints each by calling the enum, so no other place retypes a
description ([A Fact in Code Is Written Once](../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
A role folder carries its role's name exactly, which is why the names are taken
from the enum and never spelled at the call.

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
import textwrap
from enum import Enum
from pathlib import Path
from typing import Callable, NamedTuple

FOLDERS_COMMAND = "folders"


class Role(Enum):
    """A role folder a module groups a kind of work in: its name, what it holds and what it does not.

    `modules/README.md`, in its bullet "By role inside a module", names the
    roles and points here for what each holds; the list is open there, and a
    role it names is added here. `modules/computer/module/tests/folders.py` fails when
    the two differ, or when the README retypes a description. A role folder is
    named for the kind it holds, and a kind that is one thing for the whole
    module is singular (`protocol/`, `primitive/`).
    """

    PROTOCOL = (
        "protocol",
        "the module's one protocol surface: all the abstractions it states, each a concept specifying required "
        "behavior and owning no state, with the body-less signatures of their methods, including what its "
        "services take and give back. It binds every realization whatever its language; a file here in a language "
        "other than Khayyam states the same surface.",
        "no capsule, method body, state or constant value; what realizes a concept is in the module's root, "
        "primitive/, errors/ or services/. Singular: one protocol, however many files, and never a protocol/ "
        "inside services/<name>/.",
    )
    PRIMITIVE = (
        "primitive",
        "the module's primitive types: each built from none of the module's other types, only from other "
        "modules' types or from what the language gives, and the module's other types are built from them.",
        "no abstraction (protocol/), no error (errors/), no service (services/), and no type composed of "
        "the module's own types, which stands in the module's root.",
    )
    RULES = (
        "rules",
        "the executable conditions an owner holds work on the module's subject to: one folder per rule, each "
        "citing the document that states its normative claim.",
        "not a second protocol: protocol/ states what the module exposes, rules/ what an owner requires when "
        "checking work against it.",
    )
    ERRORS = (
        "errors",
        "the errors the module's work can produce, each with its own meaning: what a caller of its services "
        "may be refused with.",
        "no error that no service of the module can produce; an error belongs to the module whose work "
        "produces it.",
    )
    TESTS = (
        "tests",
        "one Test per named Process of the module, each primitive type's and each service's test, and the "
        "check that a realization satisfies its abstraction.",
        "no Test of another module's subject: a Test never leaves the module that owns its subject, and a "
        "module with no decidable expectation has no tests/.",
    )
    SERVICES = (
        "services",
        "one folder per service the module offers outside callers: each a contract a caller can read "
        "without reading the module. In a session folder, services/ holds the session's scripts.",
        "not the types a service takes or gives back: those are declared in protocol/ and primitive/ or "
        "stand in the module's root.",
    )
    DOCS = (
        "docs",
        "documents about the module that are not its specification: notes, research, reports.",
        "not the specification, which is the module's main document beside the role folders, and not a "
        "document a governing rule places beside its base artifact.",
    )
    TEMP = (
        "temp",
        "what the work makes and the module's record does not need: a draft not yet appended elsewhere, "
        "a tool's output without content value. Every module has one, every session included.",
        "nothing the record needs: it is kept out of version control and out of every archive "
        "(.agents/scripts/README.md, Temporary files).",
    )

    def __init__(self, folder: str, holds: str, holds_not: str) -> None:
        self.folder = folder
        self.holds = holds
        self.holds_not = holds_not

    @classmethod
    def entries(cls) -> str:
        """Every role as the help prints it: its folder, what it holds, what it does not."""
        def wrap(text: str, indent: str) -> str:
            return textwrap.fill(text, width=78, initial_indent=indent, subsequent_indent="  ")

        return "\n\n".join(
            wrap(f"{role.folder}/ holds {role.holds}", "") + "\n" + wrap(f"Excludes: {role.holds_not}", "  ")
            for role in cls
        )


ROLE_FOLDERS = tuple(role.folder for role in Role)
"""The role folders' names, in the enum's order, for the callers that need only the names."""

TEMP_FOLDER = Role.TEMP.folder
"""The role folder for what the work makes and the module's record does not need.

Every module has one, every session included. It is kept out of version
control in every project (`install_project` adds it to the project's
.gitignore) and out of every archive (`session_archive`); the rule is written
once, in `.agents/scripts/README.md` under "Temporary files". This is the one
place its name is spelled: `session_temp` takes it from here.
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
            "It prints what it made and what was already there. The roles, and what\n"
            "each holds and does not, are:\n\n"
            f"{Role.entries()}\n\n"
            "modules/README.md in the Memar checkout names the roles, under \"By role\n"
            "inside a module\"."
        ),
    )
    maker.add_argument("path", metavar="PATH", help="the folder to make them in; always given")
    return run


def run(args: argparse.Namespace) -> int:
    return make_folders(args.path)
