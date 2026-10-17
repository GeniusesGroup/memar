#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/report/services/report.py — a session's report.md: what a report is, and when it disagrees with the plan.

plan.md says what a task is and where it stands while it is worked; report.md
says how the work on it ended — the Status it reached, what ran, the check
and its result, what is left open. `session_new` writes the skeleton beside
the plan and never overwrites one, and `session_find` reads its Status to mark
a session whose report and plan disagree. One file owns the name, the
skeleton, and the Statuses a report may state, so the session that writes a report and the list that checks it
read it one way.

A report states a Status of the one vocabulary
[Status](../../../modules/knowledge/documentation/documentation.md#status) defines, held in
`modules/knowledge/documentation/primitive/status.py`, and no second field for how the run ended: each Status a
report may state says in the type how a run that stated it ended
(`Status.report_ending`). A report whose Status is empty says nothing yet and is not checked; a Status the
table does not give a report cannot be checked either, and is marked as such
rather than guessed.

Only today's shape is read: the Status in the front matter, in PascalCase. A
report written before in another (an `Outcome` key beside the Status, the
outcome in a `Stop:` line under the heading and no front matter, a lower-case
key, the words `open` and `done`) says no Status, and `report_shape_problem`
names it, with the same remedy a plan's gets (`session_plan`): only today's
shape is read, and where it is shown; no conversion is named.

A report is also the hand-back of a session another agent handed out: its
Status, its path, and at most ten lines under `Decisions needed` are all the
delegating side reads, and `session_digest` gathers those lines across
sessions and marks a report that is not such a hand-back. A session with nothing to ask writes no such part, so the skeleton
does not carry one.

A report is scratch, like the plan, and goes with its folder: what lasts of it
is routed by closing by type.
"""
from __future__ import annotations

from pathlib import Path

from modules.knowledge.documentation.plan.services.plan import (
    EARLIER_SHAPE_REMEDY,
    EARLIER_STATUS_WORDS,
    front_key,
    front_matter,
    status_word,
)
from modules.knowledge.documentation.record import PLAN, REPORT
from modules.knowledge.documentation.report.primitive.report_key import ReportKey
from modules.knowledge.documentation.primitive.status import Status

# The report's shape and the Statuses it may state are declared once, in
# `record` and `status`; the name is derived from them, not repeated.
REPORT_NAME = REPORT.file_name
# What marks a report of an earlier shape, so it can be named.
EARLIER_OUTCOME_KEY = "Outcome"
EARLIER_STOP_PREFIX = "Stop:"


def report_skeleton(session: str, title: str | None = None) -> str:
    """A new report.md: front matter naming its session with an empty Status (and the TITLE, when known), its heading, and the four parts.

    SESSION is the id of the session the report belongs to, written into the
    record so that a reader finds it inside the document rather than by
    reading the name of the folder the record sits in
    ([Documentation — Report](../../../modules/knowledge/documentation/report/report.md)).
    An empty Status is left for the session to fill when it ends; until it
    does, the report says nothing and is not checked.
    """
    front = [
        "---",
        f"{ReportKey.ID.written}: {session}",
        *([f"{ReportKey.TITLE.written}: {title}"] if title else []),
        f"{ReportKey.STATUS.written}:",
        "---",
    ]
    return "\n".join([*front, f"# {REPORT.heading}", "", *(f"## {part}" for part in REPORT.parts)]) + "\n"


def write_report(folder: Path, session: str, title: str | None = None) -> None:
    """Create FOLDER's report.md unless one is there; an existing report is never touched."""
    try:
        with (folder / REPORT_NAME).open("x", encoding="utf-8", newline="\n") as report:
            report.write(report_skeleton(session, title))
    except FileExistsError:
        pass


def _lines(folder: Path) -> list[str]:
    """FOLDER's report.md as lines; none when there is no readable report."""
    try:
        return (folder / REPORT_NAME).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return []


def _front(lines: list[str]) -> dict[str, str]:
    """The report's front matter, the keys written in PascalCase lowercased so callers ask for `status`; empty without one."""
    front, _ = front_matter(lines)
    return REPORT.current({key.lower(): value for key, value in (front or {}).items() if key == front_key(key)})


def read_report_status(folder: Path) -> str:
    """The Status FOLDER's report.md states, as `session_plan` reads a status; empty when it states none or there is no report.

    The value is the front matter's `Status`, lowercased. A report of an
    earlier shape states none (`report_shape_problem`), and none is not a
    disagreement.
    """
    return status_word(_front(_lines(folder)).get(ReportKey.STATUS.key, ""))


def report_shape_problem(folder: Path) -> str | None:
    """Why FOLDER's report is in an earlier shape, with where today's is shown; None when it is not, or there is none."""
    lines = _lines(folder)
    front, start = front_matter(lines)
    found = []
    if any(line.startswith(EARLIER_STOP_PREFIX) for line in lines[start:]):
        found.append("a `Stop:` line")
    if front is not None:
        if EARLIER_OUTCOME_KEY in front or EARLIER_OUTCOME_KEY.lower() in front:
            found.append("an `Outcome` key")
        if any(key != front_key(key) and key.lower() in {report_key.key for report_key in REPORT.keys} for key in front):
            found.append("keys in lower case")
        if status_word(front.get(ReportKey.STATUS.written, "")) in EARLIER_STATUS_WORDS:
            found.append(f"the status word {status_word(front[ReportKey.STATUS.written])}")
    if not found:
        return None
    return f"{REPORT_NAME} is in an earlier shape ({'; '.join(found)}); {EARLIER_SHAPE_REMEDY}"


def disagreement(status: str, report_status: str = "") -> str | None:
    """Why STATUS, a plan's, and REPORT_STATUS, its report's, disagree; None when they agree or nothing can be checked.

    A status outside the plan's vocabulary is named first, because no report
    status can agree with it. An empty status or an empty report status checks
    nothing.
    """
    status = status_word(status)
    report_status = status_word(report_status)
    if status and status not in Status.keys(PLAN.kind):
        return f"status {status} is not one of {', '.join(Status.keys(PLAN.kind))}"
    if report_status and status:
        if report_status not in Status.keys(REPORT.kind):
            return f"{REPORT_NAME} Status {report_status} is not one of {', '.join(Status.keys(REPORT.kind))}"
        if report_status != status:
            return f"{REPORT_NAME} Status {report_status} is not the plan's {status}"
    return None


def report_part(folder: Path, heading: str) -> list[str]:
    """The non-blank lines under FOLDER's report's `## HEADING` heading, as written; none without one."""
    found: list[str] | None = None
    for line in _lines(folder):
        if line.startswith("#"):
            if found is not None:
                break
            if line.lstrip("#").strip().lower() == heading.lower():
                found = []
        elif found is not None and line.strip():
            found.append(line.rstrip())
    return found or []


def decisions_needed(folder: Path) -> list[str]:
    """The non-blank lines under FOLDER's report's `## Decisions needed` heading, as written; none without one."""
    return report_part(folder, REPORT.hand_back_part)


def handback_problem(folder: Path, status: str) -> str | None:
    """Why FOLDER's report is not a hand-back, given its plan's STATUS; None when it is one.

    A hand-back is a Status this file names, agreeing with the plan's status,
    and at most `REPORT.hand_back_max_lines` lines under its hand-back part: what the
    delegating side reads is that line, the report's path, and those lines, so
    a longer one would carry the session's context back into the reader's.
    """
    shape = report_shape_problem(folder)
    if shape:
        return shape
    report_status = read_report_status(folder)
    if not report_status:
        return f"{REPORT_NAME} has no Status"
    why = disagreement(status, report_status)
    if why:
        return why
    count = len(decisions_needed(folder))
    if count > REPORT.hand_back_max_lines:
        return f"{count} lines under {REPORT.hand_back_part}, more than {REPORT.hand_back_max_lines}"
    return None
