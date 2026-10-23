#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/keep.py — which files of a task folder its records keep, and which they leave out.

A task's record is its folder: the plan, the report, and every file the work
made, filed by kind in the role folders (`task_layout`). A report links the
files it presents; a file it does not link may still be what a later task
needs, so the folder is kept whole and only what has no
place in a record is left out:

    the claim            Memar's mark that an agent holds the task, meaningless on another clone
    __pycache__          a cache the interpreter makes, rebuilt on demand
    a .git part          a repository inside the folder (a test's scratch repository): a path
                         with that part cannot be a tree entry of another repository
    a link               not a file, and it may point out of the folder
    the folder's `temp`  what the work made that the record does not need (`task_temp`)
    a binary file        a NUL in its first BINARY_PROBE_BYTES bytes: an archive, a cache, an index
    a large file         over KEEP_LIMIT_BYTES and not a document; a document, written text, is
                         kept at any size, since text is the record
    a name a manifest    holding a tab or a line break, which the file `_host_git_cli.py record`
    cannot carry         reads cannot hold

Each leave-out is reported with its reason and its size, a folder once with
the files it held, so the commit that records the task says what it did not
keep and why (`task_archive`).
"""
from __future__ import annotations
import os
from enum import Enum
from pathlib import Path
from typing import NamedTuple
from modules.management.task.services.temp import TEMP_FOLDER
from modules.management.task.primitive.claim import Claim
KEEP_LIMIT_BYTES = 256 * 1024
'The size above which a file that is not a document is left out.'
BINARY_PROBE_BYTES = 8000
'How much of a file is read to tell whether it is binary.'
DOCUMENT_SUFFIXES = ('.md',)
'The suffixes of a document: written text, which the size limit does not reach.'
CACHE_FOLDER = '__pycache__'
GIT_PART = '.git'

class Reason(Enum):
    """Why a path is left out of a task's records."""
    CLAIM = "Memar's claim, not part of the record"
    CACHE = 'a Python cache, rebuilt on demand'
    GIT = 'a .git part: a repository inside the task'
    TEMP = f"the task's {TEMP_FOLDER}/ folder, never archived"
    LINK = 'a link, not a file'
    BINARY = f'binary: a NUL in its first {BINARY_PROBE_BYTES} bytes'
    LARGE = f'over {KEEP_LIMIT_BYTES // 1024} KB and not a document'
    NAME = 'a name holding a tab or a line break'

    @property
    def sentence(self) -> str:
        return self.value

class Left(NamedTuple):
    """One path left out: where (a folder once, for the files it held), why, how many files, how many bytes."""
    path: str
    reason: Reason
    files: int
    size: int

class Selection(NamedTuple):
    """What a task folder's records keep, as posix paths from the folder, sorted; and what they leave out."""
    kept: tuple[str, ...]
    left: tuple[Left, ...]

def _measured(path: Path) -> tuple[int, int]:
    """How many files PATH holds, and their bytes: PATH itself when a file."""
    if not path.is_dir() or path.is_symlink():
        try:
            return (1, path.lstat().st_size)
        except OSError:
            return (1, 0)
    files = size = 0
    for root, _, names in os.walk(path):
        for name in names:
            try:
                size += os.lstat(os.path.join(root, name)).st_size
            except OSError:
                pass
            files += 1
    return (files, size)

def _is_binary(path: Path) -> bool:
    try:
        with path.open('rb') as stream:
            return b'\x00' in stream.read(BINARY_PROBE_BYTES)
    except OSError:
        return True

def _folder_reason(name: str, at_top: bool) -> Reason | None:
    if name == CACHE_FOLDER:
        return Reason.CACHE
    if name.lower() == GIT_PART:
        return Reason.GIT
    if at_top and name == TEMP_FOLDER:
        return Reason.TEMP
    return None

def select(folder: Path) -> Selection:
    """The files of FOLDER its records keep, and the paths they leave out."""
    kept: list[str] = []
    left: list[Left] = []

    def leave(path: Path, reason: Reason) -> None:
        files, size = _measured(path)
        left.append(Left(path.relative_to(folder).as_posix(), reason, files, size))
    for root, folders, names in os.walk(folder):
        here = Path(root)
        at_top = here == folder
        for name in sorted(folders):
            path = here / name
            reason = Reason.LINK if path.is_symlink() else _folder_reason(name, at_top)
            if reason is not None:
                leave(path, reason)
        folders[:] = [name for name in folders if not (here / name).is_symlink() and _folder_reason(name, at_top) is None]
        for name in sorted(names):
            path = here / name
            if at_top and name in Claim.NAMES:
                leave(path, Reason.CLAIM)
            elif name.lower() == GIT_PART:
                leave(path, Reason.GIT)
            elif path.is_symlink() or not path.is_file():
                leave(path, Reason.LINK)
            elif '\t' in name or '\n' in name:
                leave(path, Reason.NAME)
            elif _is_binary(path):
                leave(path, Reason.BINARY)
            elif path.stat().st_size > KEEP_LIMIT_BYTES and (not name.lower().endswith(DOCUMENT_SUFFIXES)):
                leave(path, Reason.LARGE)
            else:
                kept.append(path.relative_to(folder).as_posix())
    return Selection(tuple(sorted(kept)), tuple(sorted(left)))
