#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_find.py — the session folders a caller asks for, listed.

A folder is found again by what its plan says — the id, the title, the project,
the status — because an id says only when a session opened, not what it is
about; `list` reads every plan to answer, and that is cheap next to a session
that starts over because it could not find the one it continues.

The sessions of one conversation are listed together. One session is one task,
so a conversation is several sessions, and a person going back to it asks for
all of them: the conversation's sessions sit next to each other, the group
placed where its newest session falls, newest first inside it. A conversation
is named by any session in it — the first one's id is what the others record,
and a session asked for by its own id is read for the conversation it records;
a first session that has been swept is still the name its conversation goes by.

What is listed by default is Memar's own sessions alone. A project that keeps
its sessions in its own location keeps them for itself, and a list of every
project's sessions mixed into Memar's answers no question one session asks.
`--project` asks for one project's sessions wherever they lie: every session
folder in its own locations (`session_location.locations_of`), and every
other one whose plan names that project, from whatever folder `list` is run
in. A conversation crosses projects, since a delegated task may be another
project's, so `--conversation` looks in every location Memar has recorded.

A session whose plan and report disagree is marked where its status is shown,
because the two are written by one agent at two moments, and the list is where
the next one looks: a report that stopped blocked under a plan still marked
open, or a status the plan's vocabulary does not have, is a session that will
be misread — kept forever, or picked up as finished. What disagrees is
`session_report`'s answer.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Callable

from machine.console import fail, note
from services.session_folder import Session, folder_of, measured_idle, read_session, session_folders
from services.session_location import locations_of, project_root, same_path
from services.session_plan import DONE_STATUS, PLAN_NAME, STATUSES, is_done
from services.session_report import REPORT_NAME, disagreement, read_stop

LIST_COMMAND = "list"
NO_PLAN = f"(no {PLAN_NAME})"
NO_FRONT_MATTER = f"({PLAN_NAME} has no front matter)"
UNREADABLE_PLAN = f"({PLAN_NAME} cannot be read)"
DISAGREES = "disagrees:"


def matches(session: Session, text: str) -> bool:
    """Whether TEXT is in the session's id, title, project, or a listed task's heading, in any case.

    The id counts because it is how a session is named when one is continued:
    a caller holding `20261009T` asks for the sessions it prefixes, not for a
    title it never saw.
    """
    front = session.front or {}
    fields = (
        session.id,
        front.get("title", ""),
        front.get("project", ""),
        *(heading for heading, _ in session.tasks),
    )
    needle = text.casefold()
    return any(needle in field.casefold() for field in fields)


def has_status(session: Session, status: str) -> bool:
    """Whether SESSION's plan is in STATUS; done is what the sweep counts as done, so the two agree."""
    if not (session.has_plan and session.readable):
        return False
    return is_done(session.status) if status == DONE_STATUS else session.status == status


def conversation_named_by(session_id: str) -> str:
    """The conversation SESSION_ID belongs to: the one its plan records, else its own id."""
    folder = folder_of(session_id)
    if folder.is_dir():
        return read_session(folder).conversation
    return session_id


def grouped(sessions: list[Session]) -> list[Session]:
    """SESSIONS, newest first, with each conversation's sessions next to each other."""
    groups: dict[str, list[Session]] = {}
    for session in sessions:
        groups.setdefault(session.conversation, []).append(session)
    return [session for group in groups.values() for session in group]


def project_of(project: str | None) -> Path | None:
    """The project `--project` names: PROJECT's project, the current folder's when it is empty, None when not asked."""
    if project is None:
        return None
    return project_root(Path(project) if project.strip() else None)


def of_project(session: Session, project: Path, own: list[Path]) -> bool:
    """Whether SESSION is PROJECT's: it lies in one of OWN, its locations, or its plan names PROJECT."""
    if any(same_path(session.path.parent, location) for location in own):
        return True
    named = (session.front or {}).get("project", "").strip()
    return bool(named) and same_path(named, project)


def find_sessions(
    text: str | None = None,
    status: str | None = None,
    conversation: str | None = None,
    project: Path | None = None,
) -> list[Session]:
    """The sessions in scope, newest first and grouped by conversation, filtered by TEXT, STATUS, CONVERSATION, and PROJECT.

    The scope is Memar's own sessions, or every recorded location's too when a
    CONVERSATION or a PROJECT is asked for.
    """
    own = locations_of(project) if project is not None else []
    everywhere = conversation is not None or project is not None
    sessions = [read_session(folder) for folder in session_folders(projects=everywhere, locations=own)]
    if project is not None:
        sessions = [session for session in sessions if of_project(session, project, own)]
    if text:
        sessions = [session for session in sessions if matches(session, text)]
    if status is not None:
        sessions = [session for session in sessions if has_status(session, status)]
    if conversation is not None:
        wanted = conversation_named_by(conversation)
        sessions = [session for session in sessions if session.conversation == wanted]
    return grouped(sessions)


def count_statuses(tasks: list[tuple[str, str]]) -> str:
    """How many listed tasks are in each status, e.g. `2 open, 1 done`."""
    counts = Counter(status or "no status" for _, status in tasks)
    order = (*STATUSES, *sorted(set(counts) - set(STATUSES)))
    return ", ".join(f"{counts[status]} {status}" for status in order if counts[status]) or "none"


def print_session(session: Session, *, idle: float | None = None) -> None:
    """One list line and its notes; IDLE when measured."""
    if not session.has_plan:
        print(f"{session.id}  {NO_PLAN}")
    elif not session.readable:
        print(f"{session.id}  {UNREADABLE_PLAN}")
    elif session.front is None:
        print(f"{session.id}  {NO_FRONT_MATTER}")
    else:
        print(f"{session.id}  {session.front.get('title', '')}")
        note(f"project: {session.front.get('project', '')}")
    if session.has_plan and session.readable:
        note(f"status: {session.status or 'none'}")
        why = disagreement(session.status, read_stop(session.path))
        if why:
            note(f"{DISAGREES} {why}")
        if session.tasks:
            note(f"tasks: {count_statuses(session.tasks)}")
    if session.parent:
        note(f"parent: {session.parent}")
    if session.conversation != session.id:
        note(f"conversation: {session.conversation}")
    if idle is not None:
        note(f"idle: {idle:.1f} days")
    note(f"path: {session.path}")


def list_sessions(
    text: str | None = None,
    status: str | None = None,
    idle_days: float | None = None,
    conversation: str | None = None,
    project: str | None = None,
) -> None:
    """`list`: print the sessions asked for, or say that none matches; PROJECT empty is the current one."""
    if idle_days is not None and idle_days < 0:
        fail("--idle-days counts days waited; it cannot be negative")
    shown = 0
    for session in find_sessions(text, status, conversation, project_of(project)):
        idle = measured_idle(session.path) if idle_days is not None else None
        if idle_days is not None and (idle is None or idle < idle_days):
            # A folder whose age cannot be read is not known to have waited
            # that long, so it does not answer the question asked.
            continue
        print_session(session, idle=idle)
        shown += 1
    if not shown:
        asked = text or status is not None or idle_days is not None or conversation is not None or project is not None
        note("no session folder matches" if asked else "no session folder")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session list`."""
    lister = verbs.add_parser(
        LIST_COMMAND,
        help="list session folders, newest first, a conversation's together",
        description=(
            "List Memar's own session folders, newest first, with the sessions of one\n"
            "conversation next to each other: its id, title, project, status, the\n"
            "session it came from, and its path. A folder with no plan.md, one that\n"
            "cannot be read, or one without front matter, is listed and marked so.\n"
            f"A session whose {REPORT_NAME} Stop does not agree with its plan's status, or\n"
            f"whose status is not {', '.join(STATUSES)}, is marked `{DISAGREES}`, with why.\n"
            "A folder in a project's own session location is listed only when asked\n"
            "for: with --project, every session of that project wherever it lies, in\n"
            "its own session location or in Memar's; with --conversation, every\n"
            "session linked with that one, wherever it lies. With --status, only the\n"
            "sessions in that status are shown; with --idle-days, only those quiet\n"
            "that long, each saying how long. Together they are the sessions holding\n"
            "work in the state the caller asked about, which is what a person asks\n"
            "for before going back to one."
        ),
    )
    lister.add_argument(
        "text",
        nargs="?",
        metavar="TEXT",
        help=(
            "show only sessions whose id, title, or project holds TEXT, in any case; "
            "one word or a short phrase, not a question to answer"
        ),
    )
    lister.add_argument(
        "--status",
        choices=STATUSES,
        default=None,
        help="show only sessions whose task has this status",
    )
    lister.add_argument(
        "--idle-days",
        type=float,
        default=None,
        metavar="DAYS",
        help="show only sessions in which nothing has changed for at least DAYS days, and say how long",
    )
    lister.add_argument(
        "--conversation",
        default=None,
        metavar="ID",
        help="show only the sessions of the conversation the session ID belongs to, wherever they lie",
    )
    lister.add_argument(
        "--project",
        nargs="?",
        const="",
        default=None,
        metavar="PATH",
        help=(
            "show every session of the project PATH is in, its git top-level else PATH itself, "
            "or without PATH the git top-level of the current folder: "
            "those in its own session location and those in Memar's whose plan names it"
        ),
    )
    return run


def run(args: argparse.Namespace) -> None:
    list_sessions(args.text, args.status, args.idle_days, args.conversation, args.project)
