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
"""
from __future__ import annotations

import argparse
from collections import Counter
from typing import Callable

from machine.console import fail, note
from services.session_folder import Session, folder_of, measured_idle, read_session, session_folders
from services.session_plan import DONE_STATUS, PLAN_NAME, STATUSES, is_done

LIST_COMMAND = "list"
NO_PLAN = f"(no {PLAN_NAME})"
NO_FRONT_MATTER = f"({PLAN_NAME} has no front matter)"
UNREADABLE_PLAN = f"({PLAN_NAME} cannot be read)"


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


def find_sessions(
    text: str | None = None,
    status: str | None = None,
    conversation: str | None = None,
) -> list[Session]:
    """Every session folder, newest first and grouped by conversation, filtered by TEXT, STATUS, and CONVERSATION."""
    sessions = [read_session(folder) for folder in session_folders()]
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
) -> None:
    """`list`: print the sessions asked for, or say that none matches."""
    if idle_days is not None and idle_days < 0:
        fail("--idle-days counts days waited; it cannot be negative")
    shown = 0
    for session in find_sessions(text, status, conversation):
        idle = measured_idle(session.path) if idle_days is not None else None
        if idle_days is not None and (idle is None or idle < idle_days):
            # A folder whose age cannot be read is not known to have waited
            # that long, so it does not answer the question asked.
            continue
        print_session(session, idle=idle)
        shown += 1
    if not shown:
        asked = text or status is not None or idle_days is not None or conversation is not None
        note("no session folder matches" if asked else "no session folder")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session list`."""
    lister = verbs.add_parser(
        LIST_COMMAND,
        help="list session folders, newest first, a conversation's together",
        description=(
            "List every session folder, newest first, with the sessions of one\n"
            "conversation next to each other: its id, title, project, status, the\n"
            "session it came from, and its path. A folder with no plan.md, one that\n"
            "cannot be read, or one without front matter, is listed and marked so.\n"
            "With --status, only the sessions in that status are shown; with\n"
            "--idle-days, only those quiet that long, each saying how long; with\n"
            "--conversation, only the sessions linked with that one. Together they\n"
            "are the sessions holding work in the state the caller asked about,\n"
            "which is what a person asks for before going back to one."
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
        help="show only the sessions of the conversation the session ID belongs to",
    )
    return run


def run(args: argparse.Namespace) -> None:
    list_sessions(args.text, args.status, args.idle_days, args.conversation)
