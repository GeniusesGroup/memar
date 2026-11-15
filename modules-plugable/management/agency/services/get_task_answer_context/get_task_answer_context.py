#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.computer.software.edges.manifest.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE
from machine.console_parts import add_part_arguments
_m_answer = import_module('modules-plugable.management.agency.widgets.answer_context.answer_context')
ANSWERING_COMMAND = _m_answer.ANSWERING_COMMAND
ENDING = _m_answer.ENDING
SKILL_FILE = _m_answer.SKILL_FILE
plan_project = _m_answer.plan_project
answer_passages = _m_answer.answer_passages
answer_text = _m_answer.answer_text
get_task_answer_context = _m_answer.get_task_answer_context
AnswerContext = _m_answer.AnswerContext
questions_problem = _m_answer.questions_problem
REPORT = _m_answer.REPORT
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from bundles.memar_adaptor.cli.call_names import call_of_module
_m_questions_face = import_module('modules-plugable.management.agency.services.get_task_questions_answer_brief.get_task_questions_answer_brief')
QUESTIONS_BRIEF_CALL = call_of_module(_m_questions_face.__name__, _m_questions_face.QUESTIONS_BRIEF_COMMAND)


def task_answer_context(*, task_id: str, without_skill: bool = False, part: int = 1, most_characters: int | None = None) -> None:
    get_task_answer_context(task_id, not without_skill, part, most_characters)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_answer_context,
        name=ANSWERING_COMMAND,
        summary="print what an agent answering a task's open questions reads first; it writes nothing",
        description=f"""For an agent handed a task's questions, not its task, by
`memar {QUESTIONS_BRIEF_CALL} ID`.
The questions are the lines under `{REPORT.hand_back_part}` in the task's latest report.
Print, in parts each opened by a line `=== NAME ===`, and in this order: the task's id,
the model answering needs, the plan and the report whole (by kind), the Memar skill, the
passages of Memar's documents the `answer` kind requires and then the documents the
questions name, the command that prints every command, and how to answer.
Run it first, once.

It writes nothing and opens no task: no report, no role folder and no log line is
made, and the task is not taken up. It refuses an ID that has no plan on its timeline,
or whose report has no line under that heading.

A text too long for one tool output prints in ordered parts, each at most --most-characters
long: each part but the last ends with the exact command for the next (--part N), to run
at once; read every part before acting. Each part says "part N of M of text H", H a hash
of the whole text: a part naming another H is of another version of it.

Composition is owned by agency (`Answer_Context`); this verb is the stable command face.""",
        help={'task_id': 'the task whose questions are handed to you', 'without_skill': 'leave the Memar skill out, for an agent whose runtime already loaded it', 'part': 'print part N of a text too long for one output; each part names the command for the next', 'most_characters': 'the most characters one part holds; when not given, the preference of the project the plan names, else the default below the smallest output cut known among the runtimes in use'},
    ),
)
