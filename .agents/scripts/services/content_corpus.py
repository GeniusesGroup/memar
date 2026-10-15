#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_corpus.py — which files of a checkout are its content, and which are its ledgers.

Shared by `search`, `backlinks`, and `obligations`, which read the corpus, and by
`check`, whose walk of a folder leaves out the same generated and dependency
folders. One answer to what the checkout's content is, so a verb cannot see a
narrower or a wider world than the verb beside it.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Companion facets that are *not* the explanatory surface. Blind `search`
# is for finding what to study or follow; these companions are reached only
# when explicitly named (`path` / `meta` / `section`) or linked from a base
# document — never as search hits during an explanatory / Q&A session:
#   - .handoff.md        — resume developing the base document
#   - .changelog.md      — audit history
#   - .research.<NNN>.md — inquiry trail (same role as changelog for readers
#                         of settled explanation; matched by pattern below)
# Practice companions (.practice.md) stay in search: their reader
# relationship is "follow to accomplish," which discovery must surface.
# Governing specs such as documentation-research.md are Explanation-facet
# documents (hyphen, not `.research.<NNN>`), so search still finds them.
_SEARCH_EXCLUDED_SUFFIXES = (".handoff.md", ".changelog.md")
_RESEARCH_COMPANION = re.compile(r"\.research\.\d+\.md$", re.IGNORECASE)

# What counts as the checkout's content: the written files a reader of this
# repository might be looking for. Markdown is the documentation surface and
# `.kh` the model surface; a `.py` or a `.ts` is searched and checked because it
# is content of the repository and not of a third party, and a consuming
# project gets the same rule for its own files.
CONTENT_SUFFIXES = (".md", ".kh")

# The one corpus. `docs/` is where the model is argued, not where the
# repository's content ends: `modules/` holds the model definitions, the rule
# catalog, and the protocol implementations, `bundles/` holds what runs or
# aggregates them (the Khayyam toolchain with its rules among them), `.agents/`
# holds the configuration a session is driven by, and all are read by the same
# questions. A tool named
# for content that stopped at `docs/` would be a tool for documents wearing the
# name of the larger thing. Folders excluded from the corpus are named here
# rather than inferred, so what a verb cannot see is stated in one place.
_CORPUS_DIRS = ("docs", "modules", "bundles", ".agents")
_CORPUS_FILES = ("README.md", "AGENTS.md")
# The session scratch root is inside the checkout and holds whatever a session
# left there, so a corpus walk must not read it. It is named here rather than
# derived, because `temp` is this tool's own home and a rule that inferred it
# would change whenever a new folder appeared.
_SCRATCH_DIRNAME = "temp"


def _left_out(folders: tuple[str, ...]) -> bool:
    """Whether a file under FOLDERS, its folders from the checkout's root, is outside the corpus."""
    return _SCRATCH_DIRNAME in folders or is_generated(folders)


def _excluded_from_search(path: Path) -> bool:
    name = path.name
    if any(name.endswith(suffix) for suffix in _SEARCH_EXCLUDED_SUFFIXES):
        return True
    return _RESEARCH_COMPANION.search(name) is not None


def is_generated(parts: tuple[str, ...]) -> bool:
    """Whether any folder on the way to a file is one this project does not own.

    Asked through `machine/fs_copy_excluded`, which already answers it for the
    two things that copy part of a checkout elsewhere. A file's own name is not
    weighed: `node_modules` as a *file* would be a different thing, and the
    patterns are folder patterns where that matters.
    """
    import fnmatch

    from machine.fs_copy_excluded import NEVER_COPIED_PATTERNS

    return any(
        fnmatch.fnmatch(part, pattern)
        for part in parts
        for pattern in NEVER_COPIED_PATTERNS
    )


def content_files(root: Path) -> list[Path]:
    """Every written file of the checkout that a reader may want to search.

    The folders `_CORPUS_DIRS` names, plus the root documents `_CORPUS_FILES`
    names, walked for Markdown and the source extensions this repository is
    written in. Generated and dependency trees are excluded by name rather than
    by a pattern, so a folder that is not content stays out even when it holds
    `.md` files — an editor's bundled README is not this repository's content.

    Never a silent partial answer: a checkout with none of these folders is
    refused rather than reported as an empty corpus.
    """
    found: list[Path] = []
    present = [root / name for name in _CORPUS_DIRS]
    if not any(directory.is_dir() for directory in present):
        sys.exit(
            f"error: {root} holds none of "
            f"{', '.join(_CORPUS_DIRS)}, so it is not a Memar checkout"
        )
    for directory in present:
        if not directory.is_dir():
            continue
        for path in directory.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in CONTENT_SUFFIXES:
                continue
            if _excluded_from_search(path):
                continue
            folders = path.relative_to(root).parts[:-1]
            if _left_out(folders):
                continue
            found.append(path)
    for name in _CORPUS_FILES:
        candidate = root / name
        if candidate.is_file():
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
        for path in directory.rglob("*.changelog.md"):
            if not path.is_file():
                continue
            folders = path.relative_to(root).parts[:-1]
            if _left_out(folders):
                continue
            found.append(path)
    return sorted(found)
