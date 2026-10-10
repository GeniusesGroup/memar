#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_reference.py — a reference in Memar's content, resolved to the file it names.

Shared by every `memar content` verb that is handed a reference rather than a
path: `path`, `meta`, `section`, `backlinks`, `obligations`, and
`changelog-append`. One resolution, so two verbs never disagree about which file
a reference means.

**Where a reference resolves.** Every path Memar's own documents use —
`/docs/...`, `./foo.md`, `../bar.md`, anchors — is relative to the checkout
root, never to the reading machine or a consuming project. On shells that
rewrite a leading `/` into a Windows path before the program sees it (Git
Bash/MSYS), pass a bare repo-relative name (`docs/cognition.md`).

A reference that leaves the checkout, or names a file this clone does not hold,
is refused rather than guessed: an unpublished draft is reported as one.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def content_root() -> Path:
    """The checkout the verbs read, asked of the module that resolves it.

    Resolved once per run: a verb that re-asked would be a verb that could
    disagree with the verb beside it.
    """
    from machine.fs_memar import memar_root

    return memar_root()


def resolve_ref(ref: str, root: Path, from_file: Path | None) -> Path:
    anchor_split = re.split(r"[#?]", ref, maxsplit=1)
    clean = anchor_split[0].strip()
    if not clean:
        sys.exit(f"error: reference '{ref}' has no file part")

    windows_drive = len(clean) > 1 and clean[1] == ":"
    if clean.startswith("/") and not windows_drive:
        candidate = root / clean.lstrip("/")
    elif not windows_drive and (clean == "docs" or clean.startswith("docs/")):
        # Root-relative without the leading slash: shell-proof on MSYS,
        # which rewrites leading-`/` arguments.
        candidate = root / clean
    elif clean.startswith("~"):
        candidate = Path(clean).expanduser()
    else:
        base = from_file.parent if from_file else root
        candidate = base / clean
    candidate = candidate.resolve()

    root_resolved = root.resolve()
    try:
        candidate.relative_to(root_resolved)
    except ValueError:
        sys.exit(
            f"error: '{ref}' resolves outside the Memar root "
            f"({candidate} vs {root_resolved})"
        )
    if not candidate.is_file():
        sys.exit(
            f"error: '{ref}' -> {candidate} does not exist in this clone; "
            "it may be an unpublished draft — say so instead of guessing"
        )
    return candidate


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError as error:
        sys.exit(f"error: cannot read {path}: {error}")
