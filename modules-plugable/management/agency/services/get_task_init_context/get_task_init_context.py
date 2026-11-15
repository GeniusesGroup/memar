#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from bundles.memar_adaptor.cli.call_names import call_of_module
_m_status_face = import_module('modules-plugable.knowledge.label.status.services.status_of_thing')
SET_STATUS_LINE = f"memar {call_of_module(_m_status_face.__name__, 'set')} ID WORD --project NAME"
from modules.computer.software.edges.manifest.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE
ACTS = import_module('modules-plugable.knowledge.documentation.plan.services.plan_acts').ACTS
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from machine.console_parts import add_part_arguments
_m_compose = import_module('modules-plugable.management.agency.widgets.context_compose.context_compose')
START_COMMAND = _m_compose.START_COMMAND
SKILL_FILE = _m_compose.SKILL_FILE
ALWAYS_HELP = _m_compose.ALWAYS_HELP
CARD_POINTER = _m_compose.CARD_POINTER
ENDING = _m_compose.ENDING
commands = _m_compose.commands
marked_part = _m_compose.marked_part
marked_passages = _m_compose.marked_passages
model_part = _m_compose.model_part
step_documents = _m_compose.step_documents
documents = _m_compose.documents
named_commands = _m_compose.named_commands
plan_project = _m_compose.plan_project
start_passages = _m_compose.start_passages
start_text = _m_compose.start_text
get_task_init_context = _m_compose.get_task_init_context
_help_of = _m_compose._help_of
ContextCompose = _m_compose.ContextCompose


def task_init_context(*, task_id: str, without_skill: bool = False, part: int = 1, most_characters: int | None = None) -> None:
    get_task_init_context(task_id, not without_skill, part, most_characters)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_init_context,
        name=START_COMMAND,
        summary='print, in one output, everything an agent taking up a task needs in its context',
        description=f"""For every agent that takes up a task: a sub-agent handed one, and the agent of a task after\n`ensure` opened its own. Print, in parts each opened by a line `=== NAME ===`, and in this\norder: the task's id, the model its Kind needs, its plan (latest content of kind plan), the\nfolder's listing, the Memar skill, the passages of Memar's documents the plan's Kind requires\n(as `memar content_get_act_context --kind K` prints them; the core alone for a plan with no\nKind) and then the documents the plan's Steps name that those do not hold, the help of the\ncommands every task uses and those the plan names, and how to end. Run it first, once, and\nread nothing else before acting on the plan.\n\nA text too long for one tool output prints in ordered parts, each at most --most-characters\nlong: each part but the last ends with the exact command for the next (--part N), to run\nat once; read every part before acting. The same task prints the same parts, and each\npart says "part N of M of text H", H a hash of the whole text: a part naming another H\nis of another version of it.\n\nThe kinds a plan carries: {', '.join(ACTS)}.\n\nA task holds contents: its plan is its latest content of kind plan and its report its latest\nof kind report; a new plan or report is added with `memar conversation_post`, never written\nover. Read them with `memar git_show_task_records` (by kind). Facts change through task verbs\n(`{SET_STATUS_LINE}`, …).\n\nIt is `task_ensure --task-id ID` as well, so the role folders are there after it; it opens no new\ntask, and refuses an ID that has no plan on its timeline.\n\nComposition is owned by agency (`Context_Compose`); this verb is the stable command face.""",
        help={'task_id': 'the task handed to you', 'without_skill': 'leave the Memar skill out, for an agent whose runtime already loaded it', 'part': 'print part N of a text too long for one output; each part names the command for the next', 'most_characters': 'the most characters one part holds; when not given, the preference of the project the plan names, else the default below the smallest output cut known among the runtimes in use'},
    ),
)
