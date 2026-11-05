#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
from pathlib import Path
from typing import Callable, Iterable
Ignore = Callable[[str, Iterable[str]], Iterable[str]]

def _is_link(path: Path) -> bool:
    return os.path.islink(path) or os.path.isjunction(path)

def copied_files(folder: Path, ignore: Ignore) -> dict[str, Path]:
    found: dict[str, Path] = {}
    for root, folders, files in os.walk(folder):
        left_out = set(ignore(root, [*folders, *files]))
        folders[:] = [name for name in folders if name not in left_out and (not _is_link(Path(root, name)))]
        for name in files:
            if name not in left_out:
                path = Path(root, name)
                found[path.relative_to(folder).as_posix()] = path
    return found

def copy(source: Path, dest: Path, ignore: Ignore) -> bool:
    want, have = (copied_files(source, ignore), copied_files(dest, ignore))
    if want.keys() != have.keys():
        return True
    for name, path in want.items():
        other = have[name]
        if path.stat().st_size != other.stat().st_size:
            return True
        if path.read_bytes() != other.read_bytes():
            return True
    return False
