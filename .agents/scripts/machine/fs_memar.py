#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""machine/fs_memar.py — where Memar lives on disk: the one home for location answers.

Every script that needs a Memar path — the checkout, the recorded root, the
scratch root, a session folder — asks here instead of recomputing it. One need,
one method: a second copy of any of these answers is a second truth about where
things are, and the two drift.

It also owns the names of the folders Memar keeps inside a checkout. Those were
spelled out in three files that each had a copy — the scripts folder the command
goes on PATH from, the skill folder the app layer copies, the extensions folder
the editor layer writes — and a rename in one would have left the other two
pointing at a folder that no longer exists.
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from machine.env_location import recorded_root
from machine.fs_memar_repository import is_memar_repository

# The folder Memar's own configuration lives in, relative to a checkout root.
AGENTS_DIRNAME = ".agents"
# The one agent-scratch root every session's folder lives under. Named here
# because this is the module that joins a root to a scratch path, not because
# the string belongs to the idea of scratch on its own.
TEMP_DIRNAME = "temp"
# The sessions' own folder inside it, so a session folder is never a sibling of
# the locks, the test scratch, or whatever else scratch holds.
SESSIONS_DIRNAME = "sessions"
# Memar's record of the folders outside it that projects have had session
# folders made in, one path a line, kept beside the folders it adds to.
PROJECT_SESSIONS_NAME = "sessions.projects"

# The layout inside a checkout. Each is a path relative to the root, so a caller
# joins it to a checkout rather than spelling the join again.
SCRIPTS_RELATIVE = Path(AGENTS_DIRNAME) / "scripts"
SKILL_RELATIVE = Path(AGENTS_DIRNAME) / "skills" / "memar"
EXTENSIONS_RELATIVE = Path(AGENTS_DIRNAME) / "vscode" / "extensions"
CONSUMER_README_RELATIVE = Path(AGENTS_DIRNAME) / "memar" / "README.md"
AGENTS_INDEX_RELATIVE = Path(AGENTS_DIRNAME) / "README.md"


def checkout_root() -> Path:
    """The checkout this file is in: the parent of `.agents`.

    Counted from this file rather than from the scripts folder, because the shelf
    the file sits in is a level deep and a count that named a folder instead of
    the relation would have to change whenever the shelf did. `.agents` is a
    checkout's own, so the checkout is its parent.
    """
    return Path(__file__).resolve().parents[3]


def memar_root() -> Path:
    """The Memar root scratch lives under: recorded MEMAR_ROOT else this checkout.

    Fail-closed: when the recorded value names no repository and the checkout
    this file runs inside is no Memar repository either, there is no root to
    put scratch under, so this errors rather than guessing another folder.
    """
    recorded = recorded_root()
    if recorded is not None:
        return recorded
    checkout = checkout_root()
    if is_memar_repository(checkout):
        return checkout
    fail(
        "cannot resolve a Memar root for scratch: MEMAR_ROOT names no Memar "
        "repository and this file runs inside no checkout either. Record one "
        "(memar install) or run from inside a checkout; nothing was guessed."
    )


def scratch_root() -> Path:
    """The ONE agent-scratch root all session scratch lives under: <root>/temp/."""
    root = memar_root() / TEMP_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root


def sessions_root() -> Path:
    """The folder every session's folder lives in: <root>/temp/sessions/."""
    root = scratch_root() / SESSIONS_DIRNAME
    root.mkdir(exist_ok=True)
    return root


def project_sessions_registry() -> Path:
    """The file listing the project folders session folders were made in: <root>/temp/sessions/sessions.projects.

    The session folders a project's preferences place in the project are
    outside every Memar root, so Memar keeps where they are in its own state
    rather than searching a disk for them.
    """
    return sessions_root() / PROJECT_SESSIONS_NAME


def session_dir(session_id: str, *, create: bool = False) -> Path:
    """The folder of one session, under the sessions root. No guessing, no creation.

    The id names one folder segment, never a path: anything else is refused
    rather than resolved. Pass create=True only where the caller owns the
    session lifecycle; readers of another session's folder never create.
    """
    if not session_id or session_id in (".", "..") or "/" in session_id or "\\" in session_id:
        fail(f"refusing session id {session_id!r}: name one folder segment, not a path.")
    path = sessions_root() / session_id
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path
