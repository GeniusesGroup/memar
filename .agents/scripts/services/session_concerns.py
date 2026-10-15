#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_concerns.py — what a plan gives away about work that looks finished or abandoned yet is not complete.

Why this exists. The sweep moves only `complete` sessions, because idle is not
finished and a folder is what carries an unfinished task to the next session.
The price is that a session whose agent forgot to set its status stays for
ever, and the owner has to audit the folders by hand to find which ones are
that. `concerns` answers for one session, from its plan alone, whether it looks
like one of three such cases, so `list`, `gc`, and `digest` can say so beside
the session. It only says: nothing here moves, writes, or closes a folder, and
whether a flagged session is finished is the person's word, given to `close`.

The three cases, each a fact about the plan and no judgment of the work:
every step of the plan is checked while the status is still active; the Request
is empty, so no one was told what the task is, and the plan has been quiet for
a day, long enough that it is not simply a plan being written; and the plan
has no status at all. A status that is present but outside the vocabulary is
named by `session_report.disagreement`, which `list` already shows, so it is
not named twice. A complete session raises nothing, however it looks, and a plan of
the earlier sectioned form is not judged by a Request or by steps it never had.
"""
from __future__ import annotations

import re

from services.status import Status
from services.session_folder import Session, measured_idle
from services.session_plan import is_complete, part_text
from services.session_report import report_shape_problem

# How long an empty Request may sit before it is read as abandoned rather than
# not yet written.
EMPTY_REQUEST_IDLE_DAYS = 1
_CHECKBOX = re.compile(r"^\s*[-*]\s+\[([ xX])\]")


def all_steps_checked(steps: str) -> bool:
    """Whether STEPS, a plan's Steps text, holds at least one checkbox and every one is checked."""
    boxes = [match.group(1) for line in steps.splitlines() if (match := _CHECKBOX.match(line))]
    return bool(boxes) and all(box != " " for box in boxes)


def concerns(session: Session) -> list[str]:
    """The reasons SESSION looks finished or abandoned though it is not done; none for a sound or unreadable one."""
    if not (session.has_plan and session.readable):
        return []
    found: list[str] = []
    for problem in (session.shape, report_shape_problem(session.path)):
        if problem:
            found.append(problem)
    if session.shape or session.front is None or is_complete(session.status):
        return found
    plan = session.path / "plan.md"
    if not session.status:
        found.append("it has no status")
    try:
        if session.status == Status.ACTIVE.key and all_steps_checked(part_text(plan, "Steps")):
            found.append("every step is checked, yet the status is active")
        if not part_text(plan, "Request"):
            idle = measured_idle(session.path)
            if idle is not None and idle >= EMPTY_REQUEST_IDLE_DAYS:
                found.append(f"its Request is empty and nothing has changed for {idle:.1f} days")
    except OSError:
        pass
    return found
