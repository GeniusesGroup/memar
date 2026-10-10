#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_folder.py — one session's folder as the other services read it.

Finding, sweeping, and linking sessions all start from the same question — which
folders are sessions, what their plan says, and how long nothing in them has
changed — and each answer is given here once, so a session listed as open is
the session the sweep keeps.

Where the folders are is not decided here: `machine/fs_memar.py` owns every
Memar path, the session folder among them. Which folder directly in temp/ is a
session an earlier Memar left there is decided here, because until
`session_migrate` has moved it, it is still that session's folder: it is
listed, swept, continued, linked to, and closed where it is.

Idle is the latest change anywhere inside a folder, because on Windows a
folder's own time does not move when a nested file is edited. Reading changes
no modification time, so a folder that is only read still counts as idle.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import NamedTuple

from machine.fs_memar import SESSIONS_DIRNAME, scratch_root, session_dir, sessions_root
from services.session_id import is_dated_session_id, is_session_id
from services.session_plan import CONVERSATION_KEY, PARENT_KEY, PLAN_NAME, read_plan

DAY_SECONDS = 24 * 60 * 60


class Session(NamedTuple):
    """One session folder: its path, whether it has a plan, and what the plan says."""

    path: Path
    has_plan: bool
    front: dict[str, str] | None
    status: str
    tasks: list[tuple[str, str]]
    readable: bool = True

    @property
    def id(self) -> str:
        return self.path.name

    @property
    def parent(self) -> str:
        return (self.front or {}).get(PARENT_KEY, "")

    @property
    def conversation(self) -> str:
        """The first session of this one's conversation: recorded, else this session itself."""
        return (self.front or {}).get(CONVERSATION_KEY, "") or self.id


def read_session(folder: Path) -> Session:
    plan = folder / PLAN_NAME
    if not plan.is_file():
        return Session(folder, False, None, "", [])
    try:
        read = read_plan(plan)
    except (OSError, UnicodeDecodeError):
        return Session(folder, True, None, "", [], readable=False)
    return Session(folder, True, read.front, read.status, read.tasks)


def is_left_session(entry: Path) -> bool:
    """Whether ENTRY, directly in temp/, is a session folder an earlier Memar left there.

    A name `session_id` mints or has minted, or a folder holding a plan.md that
    `new` wrote, with its title and the time it was opened, because
    `--session-id` lets a person name a session anything.
    """
    if entry.name == SESSIONS_DIRNAME or entry.is_symlink() or not entry.is_dir():
        return False
    if is_session_id(entry.name):
        return True
    plan = entry / PLAN_NAME
    if not plan.is_file():
        return False
    try:
        front = read_plan(plan).front or {}
    except (OSError, UnicodeDecodeError):
        return False
    return "title" in front and "opened" in front


def folder_of(session_id: str) -> Path:
    """SESSION_ID's folder: under the session root, else where an earlier Memar left it in temp/.

    The first when neither is there. The id is checked by `session_dir`, so a
    path is refused before temp/ is looked at.
    """
    folder = session_dir(session_id)
    if folder.is_dir():
        return folder
    left = scratch_root() / session_id
    return left if is_left_session(left) else folder


def session_folders() -> list[Path]:
    """Every folder named as a session under the session root or left directly in temp/, newest first.

    A name sort of the dated form is creation order; the earlier form carries
    no clock and was minted before any dated id.
    """
    folders = [
        entry
        for root in (sessions_root(), scratch_root())
        for entry in root.iterdir()
        if is_session_id(entry.name) and entry.is_dir() and not entry.is_symlink()
    ]
    folders.sort(key=lambda entry: (is_dated_session_id(entry.name), entry.name), reverse=True)
    return folders


def last_change(path: Path) -> float:
    """The latest modification time of PATH or of anything inside it."""
    latest = path.stat().st_mtime
    for root, folders, files in os.walk(path):
        for name in (*folders, *files):
            try:
                changed = os.stat(os.path.join(root, name), follow_symlinks=False).st_mtime
            except OSError:
                continue
            latest = max(latest, changed)
    return latest


def measured_idle(path: Path) -> float | None:
    """Days since anything inside PATH changed, or None when that cannot be read."""
    try:
        return (time.time() - last_change(path)) / DAY_SECONDS
    except OSError:
        return None
