#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/plan_brief.py — the prompt that hands a session's plan to a sub-agent to carry out.

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
else a task needs goes in its plan. The text is here alone; `session new`
prints it when it makes a session with `--parent`, `session claims` prints it
for each session it takes, and this verb prints it again for a session that is
there, so none of them can hand over different words.

The verb is named for what the prompt makes happen, a plan carried out, rather
than by one word (owner, 2026-10-16; `prompts`). The question its sibling
`questions_brief` hands over is a separate prompt with a verb of its
own, not a flag on this one, so each verb prints one text.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail
from modules.process.session.services.folder import folder_of, is_session_folder
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath
from modules.process.session.session import SESSION_COMMAND
from modules.process.session.services.start import START_COMMAND
# TODO name: hand-session-plan-to-carry-out | hand-over-session-plan | delegate-session-task
PLAN_BRIEF_COMMAND = "hand-session-plan-to-carry-out"


def brief_text(session_id: str) -> str:
    """The text that hands SESSION_ID's task to a sub-agent, ready to paste."""
    return (
        f"Your task is session {session_id}. "
        f"Run `memar {SESSION_COMMAND} {START_COMMAND} --session-id {session_id}` first, before anything else, and follow what it prints."
    )


def print_brief(session_id: str) -> None:
    """Print SESSION_ID's brief alone, once its folder and its plan are there."""
    folder = folder_of(session_id)
    if not is_session_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(
            f"no task to hand over in {session_id}: it has no session folder with a {PLAN_NAME}. "
            f"Open it with `memar session new --title T --parent ID {ProjectName.FLAG} {ProjectName.METAVAR}` (or `{ProjectPath.FLAG} {ProjectPath.METAVAR}`), ID the session handing it over, "
            f"and write the task into its {PLAN_NAME} first"
        )
    print(brief_text(session_id))


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session hand-session-plan-to-carry-out`."""
    briefer = verbs.add_parser(
        PLAN_BRIEF_COMMAND,
        help="print the text that hands a session's plan to a sub-agent to carry out",
        description=(
            "Print the text that hands the session ID to a sub-agent to carry out its plan,\n"
            "with ID filled in, ready to paste: the same text `new --parent` prints after\n"
            f"its other lines. It tells the sub-agent to run `memar {SESSION_COMMAND} {START_COMMAND} --session-id ID`\n"
            f"first. The task itself is not in it; it is in the session's {PLAN_NAME},\n"
            "which the delegating session writes before handing the text over, adding\n"
            "nothing to it.\n"
            "\n"
            "Start a new sub-agent rather than resume a long one. Sub-agents run one at a time unless\n"
            "the owner asks otherwise, and any that run at once write disjoint files, or a shared one only\n"
            "through `memar content write`. A delegated step is done only when its report.md exists: a\n"
            "sub-agent that could only return text hands back its report, and you write it as its\n"
            "report.md, marking what you could not."
        ),
    )
    briefer.add_argument("session_id", metavar="ID", help="the session whose plan is handed over")
    return run


def run(args: argparse.Namespace) -> None:
    print_brief(args.session_id)
