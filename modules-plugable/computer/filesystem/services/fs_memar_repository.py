#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/filesystem/services/fs_memar_repository.py — what a Memar repository is, on disk.

The one definition of the question, and the one place the words of a refusal
about it are written. Every other file in this folder — and every shell that
installs Memar — asks here instead of carrying its own copy of the test, which
is the only way two of them cannot come to disagree.

The answer is a question about files and folders and nothing else, so it sits on
the machine shelf, below everything that asks it: where Memar lives
(`machine/env_location.py`, `modules-plugable/computer/filesystem/services/fs_memar.py`) as well as the installer, the
content check, and the update. How far a checkout of one is behind its upstream
is the update's, in `bundles/memar/services/update/services/checkout.py`.
"""
from __future__ import annotations
from pathlib import Path
SKILL_MARKER = Path('.agents') / 'skills' / 'memar' / 'SKILL.md'

def is_memar_repository(path: Path) -> bool:
    """A Memar repository: the entry document, the docs tree, and the skill."""
    return (path / 'README.md').is_file() and (path / 'docs').is_dir() and (path / SKILL_MARKER).is_file()

def not_a_repository(path: Path) -> str:
    """Why PATH is not a Memar repository, in the words every refusal uses."""
    return f'{path} is not a Memar repository (no README.md, docs/, and {SKILL_MARKER.as_posix()})'

def enclosing_repository(start: Path) -> Path | None:
    """The Memar repository a path sits inside, or None.

    `is_memar_repository` answers about a folder you name. This answers about a
    file you name, which is the question a caller actually has when it checks
    `docs/cognition.md` rather than the repository root: the file is a Memar
    document because of where it is, not because of what is in it. The walk stops
    at the first ancestor that qualifies, so a repository inside a repository
    resolves to the inner one — which is the one whose conventions its documents
    are written under.
    """
    current = start if start.is_dir() else start.parent
    for candidate in (current, *current.parents):
        if is_memar_repository(candidate):
            return candidate
    return None
