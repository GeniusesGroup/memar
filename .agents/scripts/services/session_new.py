#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_new.py — one session's scratch folder opened, or taken up again.

Why one folder per session, under ONE root. Parallel agent sessions edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`machine/fs_lock.py` answer that, and `memar content write` and `edit` take one,
but advisory locks are honored by skill rule and not by the filesystem:
file-write tools bypass them, and only intent notes saying who plans what
against which base let a waiter that takes over a stale lock read what the dead
session meant. Intent notes and locks are scratch, and scratch needs a home that
survives the session: session folders give every session its own folder, and
every session works inside its own folder so nothing lands in git by accident.
That home is under <memar-root>/temp/, the ONE root the root .gitignore already
ignores — OS temp dirs are forbidden, because they are wiped by other apps
while sessions last days (the OS-temp wiped risk). Where exactly is
`machine/fs_memar.py`'s answer, and it fails closed rather than guessing.

A session writes only inside its own folder: --session-id reuses an id only to
continue the same session, and two sessions writing one folder reintroduce the
unattributed mixing this exists to remove. Reading another session's folder is
fine; a session that needs something from an old folder copies it into its own.

One session is one task, so a conversation that asks for several things, or
hands a step to a sub-agent, opens several sessions. Each records the session
it came from as its parent and the first session of the conversation, written
once with its plan: a link read off one file never needs a walk up a chain
whose folders may already be swept. The parent must be a session folder that
is there, because its conversation is read from it.

Opening is also when the day's sweep runs (`session_gc`), never touching the
session being opened or continued.

Where a new folder is made is asked of the project the plan names: a project
whose preferences set a session location gets its folders there, and every
other one in Memar's own root (`session_location`). Each run also ensures the
folder's shape — the plan and the report at its top (`session_plan`,
`session_report`), and a module's role folders for whatever else the task makes
(`module_folders`) — creating only what is missing, so a folder from an
earlier Memar is brought to the same shape as it is continued.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from machine.console import fail, note
from machine.fs_memar import session_dir
from services.module_folders import ensure_role_folders
from services.project_preferences import SESSIONS_KEY, preferences_path
from services.session_folder import folder_of, project_folder_of, read_session
from services.session_gc import reap_once_a_day
from services.session_id import new_session_id
from services.session_location import (
    in_project_location,
    memar_own_note,
    project_location,
    project_location_note,
    register,
)
from services.session_log import record
from services.session_migrate import take_up
from services.session_plan import PLAN_NAME, checked_title, plan_skeleton
from services.session_report import REPORT_NAME, write_report

NEW_COMMAND = "new"


def project_root() -> Path:
    """The git top-level of the current directory, else the current directory."""
    import subprocess

    try:
        found = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return Path.cwd()
    top = found.stdout.strip()
    return Path(top).resolve() if found.returncode == 0 and top else Path.cwd()


def linked_conversation(session_id: str, parent: str) -> str:
    """The conversation a session opened from PARENT belongs to; PARENT must be a session folder."""
    if parent == session_id:
        fail("--parent names this session itself; name the session this task came from")
    folder = folder_of(parent)
    if not folder.is_dir():
        fail(f"no session folder {parent}: --parent names a session that is there, the one this task came from")
    return read_session(folder).conversation


def write_plan(
    folder: Path,
    title: str,
    parent: str | None = None,
    conversation: str | None = None,
    project: Path | None = None,
) -> None:
    """Create FOLDER's plan.md unless one is there; an existing plan is never touched."""
    opened = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    project = project_root() if project is None else project
    text = plan_skeleton(title, opened, project, parent=parent, conversation=conversation)
    try:
        with (folder / PLAN_NAME).open("x", encoding="utf-8", newline="\n") as plan:
            plan.write(text)
    except FileExistsError:
        pass


def ensure_session(
    session_id: str | None = None,
    title: str | None = None,
    parent: str | None = None,
) -> tuple[str, Path]:
    """Ensure the session's folder, its plan.md and report.md, and its role folders exist; return its id and path.

    TITLE is required when the folder has no plan.md yet, and unused when it
    has one. PARENT links a new plan to the session it came from; a plan that
    is there keeps the link it was written with, and a different one is
    refused rather than ignored. A rerun with the same id is idempotent: the
    folder, its plan, and its report are kept as they are and the same id and
    path are reported again. A session an earlier Memar left in temp/ is moved
    into temp/sessions/ as it is continued, or goes on in temp/ when the system
    will not move it; no second folder is made for it. A session in a project's
    own location is continued there. A folder that is nowhere yet is made in
    the location the project's preferences set, else under Memar's root; a
    name already taken there by anything that is not a session folder is
    refused, and a location that cannot be made fails with a message. The
    first call of a day also reaps the session folders that have been idle past
    the limit, other than this one.
    """
    sid = new_session_id() if session_id is None else session_id
    folder = session_dir(sid)
    project = project_root()
    location = project_location(project)
    if session_id is not None and not folder.is_dir():
        folder = take_up(sid) or project_folder_of(sid, also=location) or folder
    if not folder.is_dir() and location is not None:
        folder = location / sid
        if folder.exists() or folder.is_symlink():
            fail(
                f"{folder} is there and is not a session folder; `new` never writes into it. "
                "Pass --session-id a name not used in that location, or none to mint one"
            )
    existed = folder.is_dir()
    has_plan = (folder / PLAN_NAME).is_file()
    title = checked_title(title, required=not has_plan)
    parent = (parent or "").strip() or None
    conversation = None
    if parent is not None:
        if has_plan:
            recorded = read_session(folder).parent
            if recorded != parent:
                fail(
                    f"session {sid} was opened with parent {recorded or '(none)'}; "
                    "a session's link is written once, with its plan"
                )
        else:
            conversation = linked_conversation(sid, parent)
    path = folder
    if not existed:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            where = f"; check `{SESSIONS_KEY}` in {preferences_path(project)}" if location is not None else ""
            fail(f"the session folder {path} could not be made ({error.strerror or error}){where}")
        record("opened", sid, f"parent {parent}" if parent else "")
    if in_project_location(path):
        register(path.parent)
    if not has_plan:
        write_plan(path, title, parent, conversation, project)
    write_report(path)
    ensure_role_folders(path)
    reap_once_a_day(keep=sid)
    return sid, path


def open_session(session_id: str | None, title: str | None, parent: str | None) -> None:
    """`new`: ensure the session and print its id, path, plan, and report, and where it is when that is a project's."""
    sid, path = ensure_session(session_id, title, parent)
    note(f"session_id: {sid}")
    note(f"path: {path}")
    note(f"plan: {path / PLAN_NAME}")
    note(f"report: {path / REPORT_NAME}")
    if in_project_location(path):
        note(project_location_note(path))
    ignored = memar_own_note(project_root())
    if ignored is not None:
        note(ignored)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session new`."""
    opener = verbs.add_parser(
        NEW_COMMAND,
        help="ensure one session folder for one task and print its id and path",
        description=(
            "Ensure one session folder, for one task, and print its id, path, plan, and\n"
            f"report. A folder with no {PLAN_NAME} needs --title; a folder that has one is\n"
            "continued as it is. With --parent, the new plan records the session this\n"
            "task came from and the first session of that conversation.\n\n"
            "What the folder holds, what to write before work on the task ends, and\n"
            "where the folder lies are said in `memar session --help`."
        ),
    )
    opener.add_argument(
        "--session-id",
        default=None,
        help="reuse this session id instead of minting one (rerun is idempotent)",
    )
    opener.add_argument(
        "--title",
        default=None,
        help=f"one line saying what the task is; required unless the folder has a {PLAN_NAME}",
    )
    opener.add_argument(
        "--parent",
        default=None,
        metavar="ID",
        help="the session this task came from: the delegating session, or the previous task of the conversation",
    )
    return run


def run(args: argparse.Namespace) -> None:
    open_session(args.session_id, args.title, args.parent)
