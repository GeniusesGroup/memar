#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/ai/services/plan_brief.py — the prompt that hands a session's plan to a sub-agent to carry out.

A sub-agent starts with none of the delegating session's context, so the
delegating session opens the sub-agent's session itself, linked to its own,
and writes the whole task into that session's plan. What the sub-agent is
then handed is the same text for every task, with only the session's id in
it, and it says to run `memar ai get-task-init-context`, which prints what the sub-agent
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
from importlib import import_module
import argparse
from typing import Callable
from machine.console import fail
from modules.management.task.services.folder import folder_of, is_task_folder
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath
SESSION_COMMAND = import_module('modules-plugable.ai.ai').AI_COMMAND
from .get_task_init_context import START_COMMAND
PLAN_BRIEF_COMMAND = 'get-task-plan-carry-out-brief'

def brief_text(task_id: str) -> str:
    """The text that hands TASK_ID's task to a sub-agent, ready to paste."""
    return f'Your task is session {task_id}. Run `memar {SESSION_COMMAND} {START_COMMAND} --task-id {task_id}` first, before anything else, and follow what it prints.'

def get_task_plan_carry_out_brief(task_id: str) -> None:
    """Print TASK_ID's brief alone, once its folder and its plan are there."""
    folder = folder_of(task_id)
    if not is_task_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(f'no task to hand over in {task_id}: it has no session folder with a {PLAN_NAME}. Open it with `memar task ensure --title T --parent ID {ProjectName.FLAG} {ProjectName.METAVAR}` (or `{ProjectPath.FLAG} {ProjectPath.METAVAR}`), ID the task handing it over, and write the task into its {PLAN_NAME} first')
    print(brief_text(task_id))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar ai get-task-plan-carry-out-brief`."""
    briefer = verbs.add_parser(PLAN_BRIEF_COMMAND, help="print the text that hands a session's plan to a sub-agent to carry out", description=f"Print the text that hands the session ID to a sub-agent to carry out its plan,\nwith ID filled in, ready to paste: the same text `ensure --parent` prints after\nits other lines. It tells the sub-agent to run `memar {SESSION_COMMAND} {START_COMMAND} --task-id ID`\nfirst. The task itself is not in it; it is in the session's {PLAN_NAME},\nwhich the delegating session writes before handing the text over, adding\nnothing to it.\n\nStart a new sub-agent rather than resume a long one. Sub-agents run one at a time unless\nthe owner asks otherwise, and any that run at once write disjoint files, or a shared one only\nthrough `memar content write`. A delegated step is done only when its report.md exists: a\nsub-agent that could only return text hands back its report, and you write it as its\nreport.md, marking what you could not.")
    briefer.add_argument('task_id', metavar='ID', help='the session whose plan is handed over')
    return run

def run(args: argparse.Namespace) -> None:
    get_task_plan_carry_out_brief(args.task_id)
