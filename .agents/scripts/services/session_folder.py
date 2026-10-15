#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_folder.py — one session's folder as the other services read it.

Finding, sweeping, and linking sessions all start from the same question — which
folders are sessions, what their plan says, and how long nothing in them has
changed — and each answer is given here once, so a session listed as active is
the session the sweep keeps.

Where the folders are is not decided here: `machine/fs_memar.py` owns every
Memar path, the session folder among them. Only the session root's folders are
Memar's; a folder directly in temp/ is not read as a session.
A folder in a
project's own session location (`session_location`) is continued, linked to,
and closed like any other, and listed when the caller asks for its project or
its conversation, but it is never among the folders the sweep is given: it is
the project's, not Memar's. That location is a folder
the project chose and may hold the project's own folders too, so a folder
there is a session only by the same test
(`is_session_folder`), and no other folder there is ever written into or
closed.

Idle is the latest change anywhere inside a folder, because on Windows a
folder's own time does not move when a nested file is edited. Reading changes
no modification time, so a folder that is only read still counts as idle.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import NamedTuple

from machine.fs_memar import session_dir, sessions_root
from services.session_id import is_session_id
from services.session_location import registered_locations
from services.session_plan import PLAN_NAME, plan_file_problem, read_plan
from services.session_record import PlanKey, ReportKey
from services.session_report import REPORT_NAME, read_report_status
from services.status import Status

DAY_SECONDS = 24 * 60 * 60


class Session(NamedTuple):
    """One session folder: its path, whether it has a plan, and what the plan says."""

    path: Path
    has_plan: bool
    front: dict[str, str] | None
    status: str
    readable: bool = True
    # Why the plan is in an earlier shape (with where today's shape is shown), else None.
    shape: str | None = None

    @property
    def id(self) -> str:
        return self.path.name

    @property
    def parent(self) -> str:
        return (self.front or {}).get(PlanKey.PARENT.key, "")

    @property
    def conversation(self) -> str:
        """The first session of this one's conversation: recorded, else this session itself."""
        return (self.front or {}).get(PlanKey.CONVERSATION.key, "") or self.id


def read_session(folder: Path) -> Session:
    plan = folder / PLAN_NAME
    if not plan.is_file():
        return Session(folder, False, None, "")
    try:
        read = read_plan(plan)
    except (OSError, UnicodeDecodeError):
        return Session(folder, True, None, "", readable=False)
    return Session(folder, True, read.front, read.status, shape=plan_file_problem(plan))


def queued_why(session: Session) -> str | None:
    """Why SESSION is still queued: its plan's or its report's Status is Queued; None when neither is.

    A queued session is waiting to be taken up, and nothing that moves or
    removes a folder acts on one: its folder is the task.
    """
    queued = Status.QUEUED.key
    if session.status == queued:
        return f"its {PLAN_NAME}'s {PlanKey.STATUS.written} is {Status.QUEUED.word}"
    if read_report_status(session.path) == queued:
        return f"its {REPORT_NAME}'s {ReportKey.STATUS.written} is {Status.QUEUED.word}"
    return None


def is_session_folder(entry: Path) -> bool:
    """Whether ENTRY, a folder found by name outside the session root, is a session's.

    A name `session_id` mints, or a folder holding a plan.md that `new` wrote,
    with its title and the time it was opened, because `--session-id` lets a
    person name a session anything — and a folder named in a form minted
    before is a session by that plan as long as it keeps that name. Any other folder
    where a session could be — temp/'s own, or a project's beside its session
    folders — is not one, and no session verb writes into it or closes it.
    """
    if entry.is_symlink() or not entry.is_dir():
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


def _project_entries(session_id: str, also: Path | None) -> list[Path]:
    """Whatever is named SESSION_ID in ALSO or in a registered project location, folder or not."""
    locations = ([also] if also is not None else []) + registered_locations()
    return [entry for entry in (location / session_id for location in locations) if entry.exists() or entry.is_symlink()]


def project_folder_of(session_id: str, also: Path | None = None) -> Path | None:
    """SESSION_ID's session folder in ALSO or in a registered project location, or None when it is in none."""
    return next((entry for entry in _project_entries(session_id, also) if is_session_folder(entry)), None)


def foreign_project_entry(session_id: str, also: Path | None = None) -> Path | None:
    """What is named SESSION_ID in ALSO or a registered project location and is not a session folder, or None."""
    return next((entry for entry in _project_entries(session_id, also) if not is_session_folder(entry)), None)


def folder_of(session_id: str) -> Path:
    """SESSION_ID's folder: under the session root, else in a registered project location.

    The first when none is there. The id is checked by `session_dir`, so a
    path is refused before a location is looked at.
    """
    folder = session_dir(session_id)
    if folder.is_dir():
        return folder
    return project_folder_of(session_id) or folder


def _entries(root: Path) -> list[Path]:
    try:
        return list(root.iterdir())
    except OSError:
        return []


def session_folders(*, projects: bool = False, locations: list[Path] | None = None) -> list[Path]:
    """Every session folder under the session root, newest first.

    With PROJECTS, the session folders in every registered project location
    too, and with LOCATIONS, those in each of these; the sweep asks with
    neither, because those are not Memar's to sweep. In every location a
    folder is a session by `is_session_folder`, since anyone may name a
    session anything with `--session-id`, and a folder named in a form minted
    before stays a session by its plan as long as it keeps that name.
    A name sort of the minted form is creation order; any other name follows
    every minted one.
    """
    folders = [entry for entry in _entries(sessions_root()) if is_session_folder(entry)]
    roots: list[Path] = []
    for root in [*(registered_locations() if projects else []), *(locations or [])]:
        if root.resolve() not in roots:
            roots.append(root.resolve())
    folders += [entry for root in roots for entry in _entries(root) if is_session_folder(entry)]
    folders.sort(key=lambda entry: (is_session_id(entry.name), entry.name), reverse=True)
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
