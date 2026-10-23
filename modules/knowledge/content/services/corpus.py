#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/content/services/corpus.py — which files of a checkout are its content, and which are its ledgers.

Shared by `search`, `backlinks`, and `obligations`, which read the corpus, and by
`check`, whose walk of a folder leaves out the same generated and dependency
folders. One answer to what the checkout's content is, so a verb cannot see a
narrower or a wider world than the verb beside it.

The content is of sources (`CorpusSource`): the documents and the code are
files of the folders below, told apart by suffix, and are what every verb reads
by default. The tasks are not files of these folders — the archived ones are
on the records branch and the live ones under the tasks folder, both left out
of the walk below — and are read only by `find` and `search` when they are asked
for (`task_records.py`).
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_copy_excluded = plugable_load('computer.filesystem.services.fs_copy_excluded')
NEVER_COPIED_PATTERNS = _m_fs_copy_excluded.NEVER_COPIED_PATTERNS
import functools
import os
import re
import sys
from pathlib import Path
_SEARCH_EXCLUDED_SUFFIXES = ('.handoff.md', '.changelog.md')
_RESEARCH_COMPANION = re.compile('\\.research\\.\\d+\\.md$', re.IGNORECASE)
_CORPUS_DIRS = ('docs', 'modules', 'modules-plugable', 'bundles', '.agents')
_CORPUS_FILES = ('README.md', 'AGENTS.md')
_SCRATCH_DIRNAME = 'temp'

def _left_out(folders: tuple[str, ...]) -> bool:
    """Whether a file under FOLDERS, its folders from the checkout's root, is outside the corpus."""
    return _SCRATCH_DIRNAME in folders or is_generated(folders)

def _excluded_from_search(path: Path) -> bool:
    name = path.name
    if any((name.endswith(suffix) for suffix in _SEARCH_EXCLUDED_SUFFIXES)):
        return True
    return _RESEARCH_COMPANION.search(name) is not None

def is_generated(parts: tuple[str, ...]) -> bool:
    """Whether any folder on the way to a file is one this project does not own.

    Asked through `machine/fs_copy_excluded`, which already answers it for the
    two things that copy part of a checkout elsewhere. A file's own name is not
    weighed: `node_modules` as a *file* would be a different thing, and the
    patterns are folder patterns where that matters.
    """
    return any((_not_owned(part) for part in parts))

@functools.lru_cache(maxsize=None)
def _not_owned(part: str) -> bool:
    """Whether the folder name PART is one this project does not own; the same few hundred names recur across every path of a walk."""
    import fnmatch
    return any((fnmatch.fnmatch(part, pattern) for pattern in NEVER_COPIED_PATTERNS))

def content_files(root: Path, sources=None) -> list[Path]:
    """Every written file of the checkout that a reader may want to search.

    The folders `_CORPUS_DIRS` names, plus the root documents `_CORPUS_FILES`
    names, walked for Markdown and the source extensions this repository is
    written in. Generated and dependency trees are excluded by name rather than
    by a pattern, so a folder that is not content stays out even when it holds
    `.md` files — an editor's bundled README is not this repository's content.

    SOURCES, `CorpusSource` values, keeps the files of the sources named, by
    their suffixes; without it, the default ones, the documents and the code.
    The tasks are not files of these folders: they are
    `task_records.py`'s, and a corpus of the tasks alone has no files here.

    Never a silent partial answer: a checkout with none of these folders is
    refused rather than reported as an empty corpus.
    """
    from modules.knowledge.content.primitive.corpus_source import CorpusSource
    chosen = CorpusSource.default() if sources is None else tuple(sources)
    suffixes = tuple((suffix for source in chosen for suffix in source.suffixes))
    if not suffixes:
        return []
    found: list[Path] = []
    present = [root / name for name in _CORPUS_DIRS]
    if not any((directory.is_dir() for directory in present)):
        sys.exit(f"error: {root} holds none of {', '.join(_CORPUS_DIRS)}, so it is not a Memar checkout")
    for directory in present:
        if not directory.is_dir():
            continue
        for folder, dirs, files in os.walk(directory):
            dirs[:] = [name for name in dirs if name != _SCRATCH_DIRNAME and (not _not_owned(name))]
            for name in files:
                path = Path(folder, name)
                if path.suffix.lower() not in suffixes or _excluded_from_search(path):
                    continue
                found.append(path)
    for name in _CORPUS_FILES:
        candidate = root / name
        if candidate.is_file() and candidate.suffix.lower() in suffixes:
            found.append(candidate)
    return sorted(found)

def ledger_files(root: Path) -> list[Path]:
    """Every changelog ledger of the checkout, whatever folder holds it.

    A ledger is not excluded from the corpus by virtue of being a ledger: an
    undischarged propagation owed by a changelog written under `modules/` is as
    open as one written under `docs/`, and a work-list that reads half the
    ledgers reports half the work.
    """
    found: list[Path] = []
    for directory in (root / name for name in _CORPUS_DIRS):
        if not directory.is_dir():
            continue
        for path in directory.rglob('*.changelog.md'):
            if not path.is_file():
                continue
            folders = path.relative_to(root).parts[:-1]
            if _left_out(folders):
                continue
            found.append(path)
    return sorted(found)
