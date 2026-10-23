#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/knowledge/module-skeleton/services/module_ensure_folders.py — `memar module ensure-folders`: a module's role folders made inside a folder.

A module that carries more than one kind of work groups each kind in a folder
named for its role, so the module's root reads as a list of kinds rather than
of instances. Which roles there are, and what each holds and does not, is
declared here once, in `Role`: the name, what the folder holds, and what it does
not. `modules/README.md` names the roles and points here, and `memar module
ensure-folders --help` prints each by calling the enum, so no other place retypes a
description ([A Fact in Code Is Written Once](../../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
A role folder carries its role's name exactly, which is why the names are taken
from the enum and never spelled at the call.

Making is all it does. A folder already there is left as it is, and nothing is
deleted or renamed: an empty folder in a module is a decision made visible
(`modules/README.md`), and one that is not wanted is removed by a person
through the tools that keep a deletion recoverable. A file standing where a
role folder would go is reported and left.

Which roles there are is a choice another organization could make otherwise,
so it is this pluggable module's and not the kernel's
([Kernel Neutrality](../../../../modules/knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule);
owner, 2026-10-20). No kernel module imports it: a task keeps its own small
layout (`task_layout`), the name of the `temp` folder is
`modules-plugable/computer/filesystem/services/fs_memar.py`'s, and the tools that must not take a role folder for a
module ask `modules-plugable/computer/filesystem/services/fs_memar.py`'s `role_folders()`, which reads `ROLE_FOLDERS` here.
The file is named `module_` and then its verb, as the router's rule for a
capability kept outside its domain's folder asks: the router offers it under
`memar module` only because its name starts with that domain and an underscore.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
import argparse
import textwrap
from enum import Enum
from pathlib import Path
from typing import Callable, NamedTuple
FOLDERS_COMMAND = 'ensure-folders'

class Role(Enum):
    """A role folder a module groups a kind of work in: its name, what it holds and what it does not.

    `modules/README.md`, in its bullet "By role inside a module", names the
    roles and points here for what each holds; the list is open there, and a
    role it names is added here. `tests/module_ensure_folders.py` beside this shelf fails when
    the two differ, or when the README retypes a description. A role folder is
    named for the kind it holds, and a kind that is one thing for the whole
    module is singular (`protocol/`, `primitive/`).
    """
    PROTOCOL = ('protocol', "the module's one protocol surface: all the abstractions it states, each a concept specifying required behavior and owning no state, with the body-less signatures of their methods, including what its services take and give back. It binds every realization whatever its language; a file here in a language other than Khayyam states the same surface.", "no capsule, method body, state or constant value; what realizes a concept is in the module's root, primitive/, errors/ or services/. Singular: one protocol, however many files, and never a protocol/ inside services/<name>/.")
    PRIMITIVE = ('primitive', "the module's primitive types: each built from none of the module's other types, only from other modules' types or from what the language gives, and the module's other types are built from them.", "no abstraction (protocol/), no error (errors/), no service (services/), and no type composed of the module's own types, which stands in the module's root.")
    RULES = ('rules', "the executable conditions an owner holds work on the module's subject to: one folder per rule, each citing the document that states its normative claim.", 'not a second protocol: protocol/ states what the module exposes, rules/ what an owner requires when checking work against it.')
    ERRORS = ('errors', "the errors the module's work can produce, each with its own meaning: what a caller of its services may be refused with.", 'no error that no service of the module can produce; an error belongs to the module whose work produces it.')
    TESTS = ('tests', "one Test per named Process of the module, each primitive type's and each service's test, and the check that a realization satisfies its abstraction.", "no Test of another module's subject: a Test never leaves the module that owns its subject, and a module with no decidable expectation has no tests/.")
    SERVICES = ('services', "one folder per service the module offers outside callers: each a contract a caller can read without reading the module. In a task folder, services/ holds the task's scripts.", "not the types a service takes or gives back: those are declared in protocol/ and primitive/ or stand in the module's root.")
    DOCS = ('docs', 'documents about the module that are not its specification: notes, research, reports.', "not the specification, which is the module's main document beside the role folders, and not a document a governing rule places beside its base artifact.")
    TEMP = (TEMP_FOLDER, "what the work makes and the module's record does not need: a draft not yet appended elsewhere, a tool's output without content value. Every module has one, every task included.", 'nothing the record needs: it is kept out of version control and out of every archive (modules-plugable/computer/filesystem/services/fs_memar.py, TEMP_FOLDER).')

    def __init__(self, folder: str, holds: str, holds_not: str) -> None:
        self.folder = folder
        self.holds = holds
        self.holds_not = holds_not

    @classmethod
    def entries(cls) -> str:
        """Every role as the help prints it: its folder, what it holds, what it does not."""

        def wrap(text: str, indent: str) -> str:
            return textwrap.fill(text, width=78, initial_indent=indent, subsequent_indent='  ', break_on_hyphens=False)
        return '\n\n'.join((wrap(f'{role.folder}/ holds {role.holds}', '') + '\n' + wrap(f'Excludes: {role.holds_not}', '  ') for role in cls))
ROLE_FOLDERS = tuple((role.folder for role in Role))
"The role folders' names, in the enum's order, for the callers that need only the names."

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
    return ', '.join((f'{role}/' for role in roles))

def make_folders(path: str) -> int:
    """`ensure-folders`: make the missing role folders inside PATH and say what was made and what was there."""
    from machine.console import fail, note
    folder = Path(path)
    if not folder.is_dir():
        fail(f'{folder} is not a folder; name a folder that is there')
    done = ensure_role_folders(folder)
    note(f'in: {folder.resolve()}')
    if done.made:
        note(f'made: {listed(done.made)}')
    if done.present:
        note(f'already there: {listed(done.present)}')
    if done.blocked:
        note(f'not made, a file of that name is there: {listed(done.blocked)}')
    return 1 if done.blocked else 0

def describe(verbs) -> Callable[[argparse.Namespace], int]:
    """`memar module ensure-folders`."""
    maker = verbs.add_parser(FOLDERS_COMMAND, help="make a module's role folders inside a folder, the ones it lacks", description=f"""Make inside the folder PATH each of a module's role folders it lacks:\n{listed(ROLE_FOLDERS)}.\nA folder already there is left as it is; nothing is deleted or renamed.\nIt prints what it made and what was already there. The roles, and what\neach holds and does not, are:\n\n{Role.entries()}\n\nmodules/README.md in the Memar checkout names the roles, under "By role\ninside a module".""")
    maker.add_argument('path', metavar='PATH', help='the folder to make them in; always given')
    return run

def run(args: argparse.Namespace) -> int:
    return make_folders(args.path)
