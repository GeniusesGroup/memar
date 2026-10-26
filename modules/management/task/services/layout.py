#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/layout.py — what stands at a task folder's top, and which folder takes the rest.

A task folder's top holds its plan and its report, and the claim Memar
writes there while an agent holds the task; everything else the task makes is
filed by kind in the folders `task_new` makes in it (FOLDERS), so another
task reads the top as the task and finds its material by kind. That answer
is given here once: the help `memar task --help` prints is built from it.

The layout is the task's own and small (owner, 2026-10-20, C4): a task
folder is not a module, and which role folders a module has is a pluggable
profile's choice that no kernel module may import
([Kernel Neutrality](../../../knowledge/modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)).
The folders are the ones its kinds go in, its tests, and its temporary files.

A kind is told by the file's suffix, and only the kinds named in KINDS are
told: a note is Markdown and goes in docs/, a script goes in services/. A file
of any other suffix, and a folder, have no kind here, so nothing guesses where
they belong; whoever made them files them.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
from pathlib import Path
from typing import NamedTuple
from modules.management.task.primitive.claim import Claim
from modules.management.task.services.plan_file import PLAN_NAME
from modules.management.task.services.report_file import REPORT_NAME
TOP_NAMES = (PLAN_NAME, REPORT_NAME, *Claim.NAMES)
"The files a task folder's top holds besides its folders: the plan, the report, and Memar's claim."

class Kind(NamedTuple):
    """A kind of file a task makes: its name, the folder it goes in, and the suffixes that tell it."""
    name: str
    folder: str
    suffixes: tuple[str, ...]

    def takes(self, file_name: str) -> bool:
        return file_name.lower().endswith(self.suffixes)
KINDS = (Kind('note', 'docs', ('.md',)), Kind('script', 'services', ('.py', '.mjs', '.js', '.ps1', '.sh')))
TESTS_FOLDER = 'tests'
"The folder a task's tests go in."
FOLDERS = (*(kind.folder for kind in KINDS), TESTS_FOLDER, TEMP_FOLDER)
'The folders a task folder holds below its top: one per kind, its tests, and its temporary files.'

def belongs_at_top(name: str) -> bool:
    """Whether an entry named NAME may stand at a task folder's top: a top file or one of its folders."""
    return name in TOP_NAMES or name in FOLDERS

def kind_of(file_name: str) -> Kind | None:
    """The kind a file named FILE_NAME is, by its suffix; None when it is of no kind named here."""
    return next((kind for kind in KINDS if kind.takes(file_name)), None)

def kinds_listing() -> str:
    """KINDS as one line for a help text, e.g. `a note (.md) in docs/`."""
    return ', '.join((f"a {kind.name} ({', '.join(kind.suffixes)}) in {kind.folder}/" for kind in KINDS))

def folders_listing() -> str:
    """FOLDERS as folder names, e.g. `docs/, services/`."""
    return ', '.join((f'{folder}/' for folder in FOLDERS))

def ensure_folders(path: Path) -> None:
    """Make each of FOLDERS missing inside PATH; one there, or a file of its name, is left as it is."""
    for folder in FOLDERS:
        if not (path / folder).exists():
            (path / folder).mkdir()
