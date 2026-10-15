#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_brief.py — the one text that hands a session's task to a sub-agent.

A sub-agent starts with none of the delegating session's context, so the
delegating session opens the sub-agent's session itself, linked to its own,
and writes the whole task into that session's plan. What the sub-agent is
then handed is the same text for every task, with only the session's id in
it, and it says to run `memar session start`, which prints what the sub-agent
needs in its context (`session_start`): everything that differs between tasks is
in the plan, stated once in the delegator's words, and everything the skill
requires is printed by that command, so the brief carries no rule, no path,
and no word about the machine: a line naming a folder and a shell is what made
agents fail their first command. The text is produced here from the id alone,
so the delegating session has nothing to add and nothing to get wrong; whatever
else a task needs goes in its plan. The text is here alone; `new`
prints it when it makes a session with `--parent`, and `brief` prints it again
for a session that is there, so the two can never hand over different words.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail
from services.session_folder import folder_of, is_session_folder
from services.session_plan import PLAN_NAME

BRIEF_COMMAND = "brief"
# Declared in `session_start`, which owns the command; named here so the brief cannot name another.
START_COMMAND = "start"


def brief_text(session_id: str) -> str:
    """The text that hands SESSION_ID's task to a sub-agent, ready to paste."""
    return (
        f"Your task is session {session_id}. "
        f"Run `memar session {START_COMMAND} --session-id {session_id}` first, before anything else, and follow what it prints."
    )


def print_brief(session_id: str) -> None:
    """`brief`: print SESSION_ID's brief alone, once its folder and its plan are there."""
    folder = folder_of(session_id)
    if not is_session_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(
            f"no task to hand over in {session_id}: it has no session folder with a {PLAN_NAME}. "
            "Open it with `memar session new --title T --parent ID --project NAME` (or `--project-path PATH`), ID the session handing it over, "
            f"and write the task into its {PLAN_NAME} first"
        )
    print(brief_text(session_id))


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session brief`."""
    briefer = verbs.add_parser(
        BRIEF_COMMAND,
        help="print the text that hands a session's task to a sub-agent",
        description=(
            "Print the text that hands the session ID to a sub-agent, with ID filled\n"
            "in, ready to paste: the same text `new --parent` prints after its other\n"
            f"lines. The task itself is not in it; it is in the session's {PLAN_NAME},\n"
            "which the delegating session writes before handing the brief over."
        ),
    )
    briefer.add_argument("session_id", metavar="ID", help="the session whose task is handed over")
    return run


def run(args: argparse.Namespace) -> None:
    print_brief(args.session_id)
