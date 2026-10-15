#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan_priority.py — a plan's priority: which waiting task goes first, read as a whole number from 1 to 10 and written in place.

A plan that writes none has the middle value, so every plan written before priorities existed waits as an
ordinary task; a value that is not such a number reads as the middle too, since a plan is scratch a
person edits by hand and one typo must not stop the line.
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from services.session_plan import front_matter
from services.session_plan_rewrite import key_of, line_end, rewrite
from services.session_record import PlanKey


# Which waiting task goes first: 1 to 10, the higher sooner, 5 when absent.
LOWEST_PRIORITY = 1
HIGHEST_PRIORITY = 10
DEFAULT_PRIORITY = 5


def _whole_priority(value: str) -> int | None:
    """VALUE as a priority, or None when it is not a whole number from 1 to 10."""
    value = value.strip()
    if not value.isdigit():
        return None
    number = int(value)
    return number if LOWEST_PRIORITY <= number <= HIGHEST_PRIORITY else None


def priority_of(front: dict[str, str] | None) -> int:
    """The priority FRONT matter gives its plan: its `priority`, or `DEFAULT_PRIORITY` when absent or not 1 to 10."""
    found = _whole_priority((front or {}).get(PlanKey.PRIORITY.key, ""))
    return DEFAULT_PRIORITY if found is None else found


def checked_priority(value: str | int) -> int:
    """VALUE as a priority; refused when it is not a whole number from 1 to 10."""
    found = _whole_priority(str(value))
    if found is None:
        fail(
            f"a priority is a whole number from {LOWEST_PRIORITY} to {HIGHEST_PRIORITY}, the higher sooner; "
            f"{value!r} is not one"
        )
    return found


def set_priority(path: Path, priority: int) -> None:
    """Write PRIORITY as PATH's `priority`, replacing the key or adding it last in the front matter; every other line is kept.

    A plan without front matter has no place for it and is refused.
    """
    priority = checked_priority(priority)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its priority cannot be set")
        written = f"{PlanKey.PRIORITY.written}: {priority}{line_end(lines[0])}"
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.PRIORITY.written:
                return [*lines[:index], written, *lines[index + 1:]]
        return [*lines[:start - 1], written, *lines[start - 1:]]

    rewrite(path, change)
