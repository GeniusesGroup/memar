#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""machine/fs_copy.py — whether a folder still holds what copying another would write.

Memar copies parts of its checkout onto the machine — the skill into agent apps,
the editor extensions into the editor — and each copy falls behind as the
checkout changes. Whether one has is a question about two directory trees and
nothing of Memar's, so it is asked here, once, for every copy; which copies
exist stays with the file that makes them, and what a copy leaves out is passed
in by the caller rather than decided here.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Iterable

Ignore = Callable[[str, Iterable[str]], Iterable[str]]


def copied_files(folder: Path, ignore: Ignore) -> dict[str, Path]:
    """Each file a copy of FOLDER carries, by its path relative to FOLDER, leaving out what IGNORE names."""
    found: dict[str, Path] = {}
    for root, folders, files in os.walk(folder):
        left_out = set(ignore(root, [*folders, *files]))
        folders[:] = [name for name in folders if name not in left_out]
        for name in files:
            if name not in left_out:
                path = Path(root, name)
                found[path.relative_to(folder).as_posix()] = path
    return found


def differs(source: Path, dest: Path, ignore: Ignore) -> bool:
    """Whether DEST is not what copying SOURCE would write: a file added, gone, or changed."""
    want, have = copied_files(source, ignore), copied_files(dest, ignore)
    if want.keys() != have.keys():
        return True
    for name, path in want.items():
        other = have[name]
        if path.stat().st_size != other.stat().st_size:
            return True
        if path.read_bytes() != other.read_bytes():
            return True
    return False
