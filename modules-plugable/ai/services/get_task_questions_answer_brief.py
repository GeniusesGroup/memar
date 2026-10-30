#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/ai/services/questions_brief.py — the prompt that hands a task's questions to an agent to answer.

An agent does not bring the owner a question another agent can
answer: the owner's answer is the slower one (owner, 2026-10-15). So this
prints a second fixed text, from the id alone as the plan's brief is
(`plan_brief`), which hands over not the task's task but its
questions: the lines under `Decisions needed` in its report, where a task's
questions for the owner already stand and where the digest gathers them. The
agent it is handed to takes nothing up: it runs
`memar ai get-task-answer-context`, which prints
what it reads and writes nothing, opens no task and creates none, answers
each question with its reasons, says which it is unsure of, and returns its
answers as text. What it is unsure of is what reaches the owner. A task with
no such line has no question to hand over, and is refused rather than handed an
agent with nothing to do.

The verb is named for what the prompt makes happen, questions answered (owner,
2026-10-16; `prompts`); it was a flag on the plan's brief, and is a verb of its
own so that each verb prints one text.
"""
from __future__ import annotations
from importlib import import_module
import argparse
from typing import Callable
from machine.console import fail
TASK_COMMAND = import_module('modules-plugable.ai.ai').AI_COMMAND
from .get_task_answer_context import ANSWERING_COMMAND, questions_problem
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
is_task_folder = _m_folder.is_task_folder
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
QUESTIONS_BRIEF_COMMAND = 'get-task-questions-answer-brief'

def questions_brief_text(task_id: str) -> str:
    """The text that hands TASK_ID's questions, not its task, to an agent that answers them, ready to paste."""
    return f'Your task is to answer the questions of task {task_id}, not to take it up. Run `memar {TASK_COMMAND} {ANSWERING_COMMAND} --task-id {task_id}` first, before anything else, and follow what it prints.'

def get_task_questions_answer_brief(task_id: str) -> None:
    """Print the text that hands TASK_ID's questions over, once its folder, its plan and a question under its report's hand-back part are there."""
    folder = folder_of(task_id)
    if not is_task_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(f'no questions to answer in {task_id}: it has no task folder with a {PLAN_NAME}')
    problem = questions_problem(folder)
    if problem:
        fail(f'no questions to answer in {task_id}: {problem}')
    print(questions_brief_text(task_id))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar ai get-task-questions-answer-brief`."""
    briefer = verbs.add_parser(QUESTIONS_BRIEF_COMMAND, help="print the text that hands a task's open questions to an agent to answer", description=f'Print the text that hands the questions of the task ID, not its task, to an\nagent that answers them, with ID filled in, ready to paste. An agent hands\nit over, adding nothing, before it brings a question to the owner. A task stops\nto ask as any task may stop, for an hour or for years, as an issue may: its\nreport is written then, Blocked, with the questions under its Decisions needed.\nThe questions are the lines under `{REPORT.hand_back_part}` in its {REPORT_NAME}; a task\nwith none is refused.\n\nThe agent runs `memar {TASK_COMMAND} {ANSWERING_COMMAND} --task-id ID`, which writes nothing\nand opens no task, and returns its answers as text: which it is sure of, with\nits reasons, and which it is unsure of, which go to the owner.')
    TaskId.add_positional(briefer, 'the task whose questions are handed over')
    return run

def run(args: argparse.Namespace) -> None:
    get_task_questions_answer_brief(args.task_id)
