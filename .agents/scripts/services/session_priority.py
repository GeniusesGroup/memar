#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_priority.py — a session moved up or down the line queued sessions are taken in.

Why its own verb. A priority is set when a task is queued (`new --queued
--priority N`), but what matters most changes after that: the owner reads the
queue in the morning and wants one task done first, or an agent finds a task
another is waiting on. Anyone — a person or an agent — may change it, so it is
a verb of its own rather than an edit to the plan by hand, which would be one
more place the key could be written two ways. What a priority is, and how it
is written into the plan, is `session_plan`'s; this file only finds the
session and says what changed.

Any status is accepted. A priority decides only the order `claims` takes
queued sessions in, but a session open or blocked now may be queued again
later, and refusing to rank it until then would make the owner wait to say
what they already know.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail
from services.session_folder import folder_of, is_session_folder
from services.session_plan import PLAN_NAME, read_plan
from services.priority import Priority
from services.session_plan_priority import set_priority

PRIORITY_COMMAND = "priority"


def set_session_priority(session_id: str, value: str) -> None:
    """`priority`: write VALUE as SESSION_ID's priority and say what it was."""
    priority = Priority.checked(value)
    folder = folder_of(session_id)
    plan = folder / PLAN_NAME
    if not is_session_folder(folder) or not plan.is_file():
        fail(f"no session {session_id} with a {PLAN_NAME}, so there is no priority to set")
    was = Priority.of(read_plan(plan).front)
    set_priority(plan, priority)
    print(f"{session_id}  priority {priority}, was {was}")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session priority`."""
    ranker = verbs.add_parser(
        PRIORITY_COMMAND,
        help=f"change how soon a queued session is taken: {Priority.range_words()}, the higher sooner",
        description=(
            f"Set the session ID's priority to N, a whole number from {Priority.range_words()}:\n"
            "the higher goes sooner when `claims` takes queued sessions. "
            f"{Priority.default_words().capitalize()} when it is read.\n"
            "Anyone, a person or an agent, may change it, whatever the session's status."
        ),
    )
    ranker.add_argument("session_id", metavar="ID", help="the session to rank")
    ranker.add_argument("priority", metavar="N", help=f"{Priority.range_words()}, the higher sooner")
    return run


def run(args: argparse.Namespace) -> None:
    set_session_priority(args.session_id, args.priority)
