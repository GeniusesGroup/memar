#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_report.py — a session's report.md: what a report is, and when it disagrees with the plan.

plan.md says what a task is and where it stands while it is worked; report.md
says how the work on it ended — the named stop it reached, what ran, the check
and its outcome, what is left open. `session_new` writes the skeleton beside
the plan and never overwrites one, and `session_find` reads its stop to mark a
session whose report and plan disagree. One file owns the name, the
skeleton, the stops, and how each stop reads as a plan status, so the session
that writes a report and the list that checks it read it one way.

The stops are the named stops each pass of work ends on, as the Memar skill
lists them (its section "Sub-agents, briefs, and reports", citing
[Acceptance Criteria](../../../docs/agency.md#acceptance-criteria)): success
and a clean no-op leave the task done; blocked and approval-required leave it
blocked, waiting on someone; exhausted and no progress leave it open, for
another pass. A report whose Stop is empty says nothing yet and is not
checked; a stop this file does not name cannot be checked either, and is
marked as such rather than guessed.

A report is also the hand-back of a session another agent handed out: its
Stop, its path, and at most ten lines under `Decisions needed` are all the
delegating side reads, and `session_digest` gathers those lines across
sessions and marks a report that is not such a hand-back. A session with nothing to ask writes no such part, so the skeleton
does not carry one.

A report is scratch, like the plan, and goes with its folder: what lasts of it
is routed by closing by type.
"""
from __future__ import annotations

from pathlib import Path

from services.session_plan import BLOCKED_STATUS, DONE_STATUS, OPEN_STATUS, STATUSES

REPORT_NAME = "report.md"
STOP_PREFIX = "Stop:"
# Each named stop, and the plan status it leaves the task in.
STOP_STATUS = {
    "success": DONE_STATUS,
    "clean no-op": DONE_STATUS,
    "blocked": BLOCKED_STATUS,
    "approval-required": BLOCKED_STATUS,
    "exhausted": OPEN_STATUS,
    "no progress": OPEN_STATUS,
}
STOPS = tuple(STOP_STATUS)
# The parts every report carries, in order, under its stop.
PARTS = ("What ran", "Check", "Result", "Left open")
# The part a report adds when the session needs someone's decision, and the
# most lines it may hold for the report to be a hand-back.
DECISIONS_HEADING = "Decisions needed"
MAX_DECISION_LINES = 10


def stop_table(margin: str = "    ") -> str:
    """Which plan status each stop leaves, one status a line, for a help text to show."""
    statuses = dict.fromkeys(STOP_STATUS.values())
    rows = [f"Stop: {', '.join(stop for stop in STOPS if STOP_STATUS[stop] == status)}" for status in statuses]
    width = max(len(row) for row in rows) + 4
    return "\n".join(f"{margin}{row:<{width}}Status: {status}" for row, status in zip(rows, statuses))


def report_skeleton() -> str:
    """A new report.md: its heading, an empty Stop line, and the four parts."""
    return "\n".join(["# Report", STOP_PREFIX, "", *(f"## {part}" for part in PARTS)]) + "\n"


def write_report(folder: Path) -> None:
    """Create FOLDER's report.md unless one is there; an existing report is never touched."""
    try:
        with (folder / REPORT_NAME).open("x", encoding="utf-8", newline="\n") as report:
            report.write(report_skeleton())
    except FileExistsError:
        pass


def _names(value: str, stop: str) -> bool:
    """Whether VALUE is STOP, alone or followed by words that are not part of it."""
    return value == stop or (value.startswith(stop) and not value[len(stop)].isalnum())


def read_stop(folder: Path) -> str:
    """The Stop FOLDER's report.md gives, lowercased; empty when it gives none or there is no report.

    The value is the first `Stop:` line's, as written after the prefix; a stop
    the report names followed by more words — `blocked: which module?` — reads
    as that stop.
    """
    try:
        lines = (folder / REPORT_NAME).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return ""
    for line in lines:
        if line.startswith(STOP_PREFIX):
            value = line[len(STOP_PREFIX):].strip().lower()
            named = [stop for stop in STOPS if _names(value, stop)]
            return max(named, key=len) if named else value
    return ""


def disagreement(status: str, stop: str) -> str | None:
    """Why STATUS, a plan's, and STOP, its report's, disagree; None when they agree or nothing can be checked.

    A status outside the plan's vocabulary is named first, because no stop can
    agree with it. An empty status or an empty stop checks nothing.
    """
    if status and status not in STATUSES:
        return f"status {status} is not one of {', '.join(STATUSES)}"
    if not stop or not status:
        return None
    expected = STOP_STATUS.get(stop)
    if expected is None:
        return f"{REPORT_NAME} Stop {stop} is not one of {', '.join(STOPS)}"
    if expected != status:
        return f"{REPORT_NAME} Stop {stop} means status {expected}, the plan says {status}"
    return None


def decisions_needed(folder: Path) -> list[str]:
    """The non-blank lines under FOLDER's report's `## Decisions needed` heading, as written; none without one."""
    try:
        lines = (folder / REPORT_NAME).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    found: list[str] | None = None
    for line in lines:
        if line.startswith("#"):
            if found is not None:
                break
            if line.lstrip("#").strip().lower() == DECISIONS_HEADING.lower():
                found = []
        elif found is not None and line.strip():
            found.append(line.rstrip())
    return found or []


def handback_problem(folder: Path, status: str) -> str | None:
    """Why FOLDER's report is not a hand-back, given its plan's STATUS; None when it is one.

    A hand-back is a Stop this file names, agreeing with the plan's status, and
    at most `MAX_DECISION_LINES` lines under `Decisions needed`: what the
    delegating side reads is that line, the report's path, and those lines, so
    a longer one would carry the session's context back into the reader's.
    """
    stop = read_stop(folder)
    if not stop:
        return f"{REPORT_NAME} has no Stop"
    why = disagreement(status, stop)
    if why:
        return why
    count = len(decisions_needed(folder))
    if count > MAX_DECISION_LINES:
        return f"{count} lines under {DECISIONS_HEADING}, more than {MAX_DECISION_LINES}"
    return None
