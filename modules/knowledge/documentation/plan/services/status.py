#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/plan/services/status.py — a plan's Status line rewritten: queued or claimed, and nothing else touched.
"""
from __future__ import annotations
from pathlib import Path
from machine.console import fail
from modules.knowledge.documentation.plan.services.plan import front_matter, status_word
from modules.knowledge.documentation.plan.services.rewrite import key_of, line_end, rewrite
from modules.knowledge.documentation.record import PLAN
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.status import Status

def set_status(path: Path, status: str, expected: tuple[str, ...] | None=None) -> None:
    """Set PATH's front matter Status to STATUS, keeping every other line and its newlines as written.

    A plan in an earlier shape is refused (`rewrite`), and so is one with no
    front matter, which has nowhere to keep a status. A plan with front matter
    and no Status is given one, last. With EXPECTED, the status is set only
    while it is still one of those, checked on the plan as it is when written
    (`rewrite`); otherwise the plan is left as it is and the caller refused.
    STATUS and EXPECTED are statuses a task plan may take (`PLAN.statuses`); any other word is refused.
    """
    status = status_word(status)
    wanted = None if expected is None else tuple((status_word(word) for word in expected))
    for word in (status, *(wanted or ())):
        if word not in Status.keys(PLAN.kind):
            fail(f"{word!r} is not a status; the statuses are {', '.join(Status.keys(PLAN.kind))}")

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its status cannot be set to {status}')
        written = f'{PlanKey.STATUS.written}: {status.capitalize()}'
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.STATUS.written:
                found = status_word(lines[index].partition(':')[2])
                if wanted is not None and found not in wanted:
                    fail(f"{path} is {found or 'without a status'} now, no longer {' or '.join(expected)}, so it is not set to {status}")
                return [*lines[:index], written + line_end(lines[index]), *lines[index + 1:]]
        if wanted is not None:
            fail(f"{path} is without a status now, no longer {' or '.join(expected)}, so it is not set to {status}")
        return [*lines[:start - 1], written + line_end(lines[0]), *lines[start - 1:]]
    rewrite(path, change)
