#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import argparse
from typing import Callable
from modules.computer.software.edges.manifest.services.preferences import MOST_CHARACTERS_KEY, PREFERENCES_RELATIVE
from machine.console_parts import add_part_arguments
TASK_COMMAND = import_module('modules-plugable.ai.ai').AI_COMMAND
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


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar ai get-task-answer-context`."""
    answerer = verbs.add_parser(ANSWERING_COMMAND, help="print what an agent answering a task's open questions reads first; it writes nothing", description=f"""For an agent handed a task's questions, not its task, by\n`memar {TASK_COMMAND} get-task-questions-answer-brief ID`.\nThe questions are the lines under `{REPORT.hand_back_part}` in the task's latest report.\nPrint, in parts each opened by a line `=== NAME ===`, and in this order: the task's id,\nthe model answering needs, the plan and the report whole (by kind), the Memar skill, the\npassages of Memar's documents the `answer` kind requires and then the documents the\nquestions name, the command that prints every command, and how to answer.\nRun it first, once.\n\nIt writes nothing and opens no task: no report, no role folder and no log line is\nmade, and the task is not taken up. It refuses an ID that has no plan on its timeline,\nor whose report has no line under that heading.\n\nA text too long for one tool output prints in ordered parts, each at most --most-characters\nlong: each part but the last ends with the exact command for the next (--part N), to run\nat once; read every part before acting. Each part says "part N of M of text H", H a hash\nof the whole text: a part naming another H is of another version of it.\n\nComposition is owned by agency (`Answer_Context`); this verb is the stable command face.""")
    TaskId.add_flag(answerer, 'the task whose questions are handed to you', required=True)
    answerer.add_argument('--without-skill', action='store_true', help='leave the Memar skill out, for an agent whose runtime already loaded it')
    add_part_arguments(answerer, f'the `{MOST_CHARACTERS_KEY}` in the {PREFERENCES_RELATIVE.as_posix()} of the project the plan names')
    return run


def run(args: argparse.Namespace) -> None:
    get_task_answer_context(args.task_id, not args.without_skill, args.part, args.most_characters)
