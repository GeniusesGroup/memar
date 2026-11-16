#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
from machine.console import fail
from machine.console_parts import bound, next_command
from machine.console_parts import part_text as parted
from modules.knowledge.content.services.reference import content_root, read_text
from modules.computer.software.edges.manifest.services.preferences import most_characters_preference
_m_storage = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage')
_m_report_text = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
_decisions_needed = _m_report_text.decisions_needed
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
_m_compose = import_module('modules-plugable.management.agency.widgets.context_compose.context_compose')
commands = _m_compose.commands
marked_part = _m_compose.marked_part
marked_passages = _m_compose.marked_passages
model_part = _m_compose.model_part
step_documents = _m_compose.step_documents
documents = _m_compose.documents
_m_questions_brief = import_module('modules-plugable.management.agency.widgets.questions_answer_brief.questions_answer_brief')
questions_problem = _m_questions_brief.questions_problem
ANSWERING_COMMAND = _m_questions_brief.ANSWERING_COMMAND
_m_acts = import_module('modules.management.agency.labels.acts')
Acts = _m_acts.Acts
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from bundles.memar_adaptor.cli.call_names import call_of_module
_INIT_CALL = call_of_module(
    'modules-plugable.management.agency.widgets.context_compose.context_compose',
    'get-task-init-context',
)
_ANSWER_CALL = call_of_module(
    'modules-plugable.management.agency.widgets.answer_context.answer_context',
    ANSWERING_COMMAND,
)
_QUESTIONS_BRIEF_CALL = call_of_module(
    'modules-plugable.management.agency.widgets.questions_answer_brief.questions_answer_brief',
    'get-task-questions-answer-brief',
)
ENDING = f"You answer the questions of this task; you do not take it up. Its questions are the lines under `{REPORT.hand_back_part}` in its report (above), each with the handoff entry it points to, if any.\nYour answering opens no task and creates none: run no `memar {_INIT_CALL}`, `task_ensure`, `task_claim` or `task_claims`. It writes nothing: no content of this task, nothing in the checkout, or elsewhere; the task that handed you the questions writes what follows from your answers.\nFor each question, in the order asked: read the plan, the entry it points to, and the passages of the documents it concerns, found as the skill says; answer it with its reasons, citing the passages they rest on; and say whether you are sure. Say you are unsure where the documents do not settle it, and say so too where it is one of the kinds the Norm Application Points (above) send to the owner however well settled: those go to the owner.\nReturn the answers as your final text, one per question, each marked sure or unsure, and name the model you run on."


class _Storage:
    """One place durable state is reached until the memory/record adapter binds."""

    def is_task(self, task_id: str) -> bool:
        return _m_storage.is_task_folder(task_id)

    def has_plan(self, task_id: str) -> bool:
        return _m_storage.has_plan(task_id)

    def plan_text(self, task_id: str) -> str:
        return _m_storage.plan_text(task_id)

    def report_text(self, task_id: str) -> str:
        return _m_storage.report_text(task_id)

    def decisions_needed(self, task_id: str) -> list[str]:
        return _decisions_needed(task_id)

    def project_named(self, task_id: str):
        return _m_storage.project_named(task_id)

    def skill_relative(self):
        _m_fs = import_module('bundles.memar.services.location.memar_location')
        return (_m_fs.SKILL_RELATIVE / 'SKILL.md').as_posix()

    def skill_text(self, root) -> str:
        return read_text(root / self.skill_relative())

    def content_root(self):
        return content_root()


_storage = _Storage()


def _task_part(task_id: str) -> str:
    return marked_part('task', f'task_id: {task_id}\nplan: (latest content of kind plan)\nreport: (latest content of kind report)\nIts questions are read here, and the task is not taken up.')


def plan_project(task_id: str):
    return _storage.project_named(task_id)


class AnswerContext:

    def __init__(self, storage: _Storage | None=None) -> None:
        self.storage = storage or _storage

    def compose(self, task_id: str, with_skill: bool=True) -> list[str]:
        store = self.storage
        if not store.is_task(task_id) or not store.has_plan(task_id):
            fail(f'no questions to answer in {task_id}: it has no plan on its timeline')
        problem = questions_problem(task_id)
        if problem:
            fail(f'no questions to answer in {task_id}: {problem}')
        root = store.content_root()
        questions = store.decisions_needed(task_id)
        passages = [_task_part(task_id), model_part(Acts.ANSWER.title), marked_part('plan', store.plan_text(task_id)), marked_part('report', store.report_text(task_id)), *([marked_part('skill', store.skill_text(root))] if with_skill else []), *marked_passages('documents', documents(root, [Acts.ANSWER], step_documents(root, '\n'.join(questions)), store.project_named(task_id)).blocks), marked_part('commands', commands.card_text()), marked_part('ending', ENDING)]
        return [passage + '\n' for passage in passages[:-1]] + passages[-1:]


def answer_passages(task_id: str, with_skill: bool=True) -> list[str]:
    return AnswerContext().compose(task_id, with_skill)


def answer_text(task_id: str, with_skill: bool=True) -> str:
    return ''.join(answer_passages(task_id, with_skill))


def get_task_answer_context(task_id: str, with_skill: bool=True, part: int=1, most: int | None=None) -> None:
    words = ['memar', _ANSWER_CALL, TaskId.FLAG, task_id, *([] if with_skill else ['--without-skill'])]
    passages = answer_passages(task_id, with_skill)
    limit = bound(most, most_characters_preference(plan_project(task_id)))
    sys.stdout.write(parted(passages, part, limit, next_command(words, most)))


SKILL_FILE = _storage.skill_relative()


def task_answer_context(*, task_id: str, without_skill: bool = False, part: int = 1, most_characters: int | None = None) -> None:
    get_task_answer_context(task_id, not without_skill, part, most_characters)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(
        task_answer_context,
        name=ANSWERING_COMMAND,
        summary="print what an agent answering a task's open questions reads first; it writes nothing",
        description=f"""For an agent handed a task's questions, not its task, by
`memar {_QUESTIONS_BRIEF_CALL} ID`.
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
of the whole text: a part naming another H is of another version of it.""",
        help={'task_id': 'the task whose questions are handed to you', 'without_skill': 'leave the Memar skill out, for an agent whose runtime already loaded it', 'part': 'print part N of a text too long for one output; each part names the command for the next', 'most_characters': 'the most characters one part holds; when not given, the preference of the project the plan names, else the default below the smallest output cut known among the runtimes in use'},
    ),
)
