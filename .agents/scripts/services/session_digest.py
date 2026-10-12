#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_digest.py — every decision the sessions hand back, gathered into one digest.

Why one digest. The owner's attention is one of the two bottlenecks of the
work, and a question asked in each of a hundred sessions is a hundred
interruptions. A session that needs someone's decision writes it in its report
under `Decisions needed` — each entry the question, its options, and a
recommendation — and ends; `digest` gathers those entries across the sessions'
reports into one text, so the owner reads every open decision at once, each
beside the session and the report it came from. What a report's decisions are
is `session_report`'s answer, and so is whether the report is a hand-back at
all (`handback_problem`).

Why the hand-back is checked here. With no launcher, the digest is where the
agent that handed sessions out reads what came back, and so where a report
that is not a hand-back — longer than the delegating side may read, or with a
Stop its plan's status disagrees with — has to be said: it is marked as a
failed hand-back beside its entries, for the owner to see, rather than
trusted. Each session's priority is shown too, since the owner answering
decisions answers the most pressing first.

Which sessions. Memar's own, newest first as `list` shows them, or one
conversation's with `--conversation`, wherever its sessions lie; the
coordinator that handed a conversation's sessions out asks for that one. Of
those, a session is in the digest when its report has entries or is a failed
hand-back, the second even with no entries, since a session that handed back
nothing usable is itself what the owner has to see. A done session is left
out, its task over, and so is a queued one, which no one has worked yet and
which has handed nothing back; one with no entries and a sound hand-back is
left out too: the digest is the decisions, not the sessions.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import note
from services.session_find import find_sessions
from services.session_plan import DONE_STATUS, QUEUED_STATUS, priority_of
from services.session_report import DECISIONS_HEADING, REPORT_NAME, decisions_needed, handback_problem, read_stop

DIGEST_COMMAND = "digest"


def print_digest(conversation: str | None = None) -> None:
    """`digest`: print every session's decisions and failed hand-backs in one digest, or say there are none."""
    gathered = []
    for session in find_sessions(conversation=conversation):
        if session.status in (DONE_STATUS, QUEUED_STATUS):
            continue
        entries = decisions_needed(session.path)
        problem = handback_problem(session.path, session.status)
        if entries or problem:
            gathered.append((session, entries, problem))
    if not gathered:
        note("no decisions needed, and no failed hand-back")
        return
    count = sum(len(entries) for _, entries, _ in gathered)
    print(f"{DECISIONS_HEADING} — {len(gathered)} sessions, {count} entries")
    for session, entries, problem in gathered:
        print()
        print(f"{session.id}  {(session.front or {}).get('title', '')}")
        note(f"priority: {priority_of(session.front)}")
        note(f"stop: {read_stop(session.path) or 'none'}")
        if problem:
            note(f"failed hand-back: {problem}")
        note(f"report: {session.path / REPORT_NAME}")
        for entry in entries:
            note(entry)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session digest`."""
    digester = verbs.add_parser(
        DIGEST_COMMAND,
        help="gather every session's decisions needed into one digest",
        description=(
            f"Print one digest of every entry under `{DECISIONS_HEADING}` in the sessions'\n"
            f"{REPORT_NAME}s: each session with entries, its title, priority, Stop, and\n"
            "report, and its entries as written. A report that is not a short\n"
            "hand-back is in it too, entries or not, marked `failed hand-back`, with\n"
            "why. Done and queued sessions are left out. Memar's own sessions, or\n"
            "with --conversation one conversation's, wherever they lie: the\n"
            "coordinator passes the id of a session of its own conversation. What a\n"
            "report's decisions are is said in `memar session --help`."
        ),
    )
    digester.add_argument(
        "--conversation",
        default=None,
        metavar="ID",
        help="gather only the sessions of the conversation the session ID belongs to",
    )
    return run


def run(args: argparse.Namespace) -> None:
    print_digest(args.conversation)
