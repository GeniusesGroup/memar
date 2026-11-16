#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.console import fail
_m_storage = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage')
_m_folder = import_module('modules-plugable.management.task.services.folder')
from bundles.memar_adaptor.cli.call_names import call_of_module
ANSWERING_COMMAND = 'get-task-answer-context'
ANSWER_CALL = call_of_module(
    'modules-plugable.management.agency.widgets.answer_context.answer_context',
    ANSWERING_COMMAND,
)
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
_m_report_text = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
_decisions_needed = _m_report_text.decisions_needed
QUESTIONS_BRIEF_COMMAND = 'get-task-questions-answer-brief'


class _Storage:
    """One place durable state is reached until the memory/record adapter binds."""

    def is_task(self, task_id: str) -> bool:
        return _m_storage.is_task_folder(task_id) or _m_folder.project_folder_of(task_id) is not None

    def has_plan(self, task_id: str) -> bool:
        if _m_storage.has_plan(task_id):
            return True
        found = _m_folder.project_folder_of(task_id)
        return found is not None and _m_storage.has_plan(found)

    def decisions_needed(self, task_id: str) -> list[str]:
        held = _decisions_needed(task_id)
        if held:
            return held
        found = _m_folder.project_folder_of(task_id)
        return _decisions_needed(found) if found is not None else []


_storage = _Storage()


def questions_problem(task_id: str) -> str | None:
    if _storage.decisions_needed(task_id):
        return None
    return f"its report has no line under `{REPORT.hand_back_part}`, where a task's questions stand. Post each question there first, one line each"


class QuestionsAnswerBrief:

    def __init__(self, storage: _Storage | None=None) -> None:
        self.storage = storage or _storage

    def text_of(self, task_id: str) -> str:
        return f'Your task is to answer the questions of task {task_id}, not to take it up. Run `memar {ANSWER_CALL} --task-id {task_id}` first, before anything else, and follow what it prints. Where Memar\'s MCP tools are listed, call the tool `{ANSWER_CALL}` with the same arguments instead of running the command.'

    def print(self, task_id: str) -> None:
        store = self.storage
        if not store.is_task(task_id) or not store.has_plan(task_id):
            fail(f'no questions to answer in {task_id}: it has no plan on its timeline')
        problem = questions_problem(task_id)
        if problem:
            fail(f'no questions to answer in {task_id}: {problem}')
        print(self.text_of(task_id))


def questions_brief_text(task_id: str) -> str:
    return QuestionsAnswerBrief().text_of(task_id)


def get_task_questions_answer_brief(task_id: str) -> None:
    QuestionsAnswerBrief().print(task_id)


def task_questions_answer_brief(task_id: str) -> None:
    get_task_questions_answer_brief(task_id)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_questions_answer_brief,
        name=QUESTIONS_BRIEF_COMMAND,
        summary="print the text that hands a task's open questions to an agent to answer",
        description=f'Print the text that hands the questions of the task ID, not its task, to an\nagent that answers them, with ID filled in, ready to paste. An agent hands\nit over, adding nothing, before it brings a question to the owner. A task stops\nto ask as any task may stop, for an hour or for years, as an issue may: its\nreport is written then, Blocked, with the questions under its Decisions needed.\nThe questions are the lines under `{REPORT.hand_back_part}` in its latest report; a task\nwith none is refused.\n\nThe agent runs `memar {ANSWER_CALL} --task-id ID`, which writes nothing\nand opens no task, and returns its answers as text: which it is sure of, with\nits reasons, and which it is unsure of, which go to the owner.',
        takes=('task_id',),
        help={'task_id': 'the task whose questions are handed over'},
    ),
)
