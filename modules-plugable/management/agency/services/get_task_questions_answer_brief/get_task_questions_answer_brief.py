#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_brief = import_module('modules-plugable.management.agency.widgets.questions_answer_brief.questions_answer_brief')
QUESTIONS_BRIEF_COMMAND = _m_brief.QUESTIONS_BRIEF_COMMAND
ANSWERING_COMMAND = _m_brief.ANSWERING_COMMAND
questions_brief_text = _m_brief.questions_brief_text
questions_problem = _m_brief.questions_problem
get_task_questions_answer_brief = _m_brief.get_task_questions_answer_brief
QuestionsAnswerBrief = _m_brief.QuestionsAnswerBrief
REPORT = _m_brief.REPORT
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from bundles.memar_adaptor.cli.call_names import call_of_module
ANSWER_CALL = call_of_module(
    'modules-plugable.management.agency.services.get_task_answer_context.get_task_answer_context',
    ANSWERING_COMMAND,
)


def task_questions_answer_brief(task_id: str) -> None:
    get_task_questions_answer_brief(task_id)


declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_questions_answer_brief,
        name=QUESTIONS_BRIEF_COMMAND,
        summary="print the text that hands a task's open questions to an agent to answer",
        description=f'Print the text that hands the questions of the task ID, not its task, to an\nagent that answers them, with ID filled in, ready to paste. An agent hands\nit over, adding nothing, before it brings a question to the owner. A task stops\nto ask as any task may stop, for an hour or for years, as an issue may: its\nreport is written then, Blocked, with the questions under its Decisions needed.\nThe questions are the lines under `{REPORT.hand_back_part}` in its latest report; a task\nwith none is refused.\n\nThe agent runs `memar {ANSWER_CALL} --task-id ID`, which writes nothing\nand opens no task, and returns its answers as text: which it is sure of, with\nits reasons, and which it is unsure of, which go to the owner.\n\nComposition is owned by agency (`Questions_Answer_Brief`); this verb is the stable command face.',
        takes=('task_id',),
        help={'task_id': 'the task whose questions are handed over'},
    ),
)
