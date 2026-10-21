#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/ai/services/questions_brief.py — the prompt that hands a session's questions to an agent to answer.

A coordinating session does not bring the owner a question another agent can
answer: the owner's answer is the slower one (owner, 2026-10-15). So this
prints a second fixed text, from the id alone as the plan's brief is
(`plan_brief`), which hands over not the session's task but its
questions: the lines under `Decisions needed` in its report, where a session's
questions for the owner already stand and where the digest gathers them. The
agent it is handed to takes nothing up: it runs
`memar ai get-task-answer-context`, which prints
what it reads and writes nothing, opens no session and creates none, answers
each question with its reasons, says which it is unsure of, and returns its
answers as text. What it is unsure of is what reaches the owner. A session with
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
SESSION_COMMAND = import_module('modules-plugable.ai.ai').AI_COMMAND
from .get_task_answer_context import ANSWERING_COMMAND, questions_problem
from modules.management.task.services.folder import folder_of, is_task_folder
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
from modules.knowledge.documentation.record import REPORT
from modules.knowledge.documentation.report.services.report import REPORT_NAME
QUESTIONS_BRIEF_COMMAND = 'get-task-questions-answer-brief'

def questions_brief_text(task_id: str) -> str:
    """The text that hands TASK_ID's questions, not its task, to an agent that answers them, ready to paste."""
    return f'Your task is to answer the questions of session {task_id}, not to take it up. Run `memar {SESSION_COMMAND} {ANSWERING_COMMAND} --task-id {task_id}` first, before anything else, and follow what it prints.'

def get_task_questions_answer_brief(task_id: str) -> None:
    """Print the text that hands TASK_ID's questions over, once its folder, its plan and a question under its report's hand-back part are there."""
    folder = folder_of(task_id)
    if not is_task_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(f'no questions to answer in {task_id}: it has no session folder with a {PLAN_NAME}')
    problem = questions_problem(folder)
    if problem:
        fail(f'no questions to answer in {task_id}: {problem}')
    print(questions_brief_text(task_id))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar ai get-task-questions-answer-brief`."""
    briefer = verbs.add_parser(QUESTIONS_BRIEF_COMMAND, help="print the text that hands a session's open questions to an agent to answer", description=f'Print the text that hands the questions of the session ID, not its task, to an\nagent that answers them, with ID filled in, ready to paste. A coordinating\nsession hands it over, adding nothing, before it brings a question to the owner.\nThe questions are the lines under `{REPORT.hand_back_part}` in its {REPORT_NAME}; a session\nwith none is refused.\n\nThe agent runs `memar {SESSION_COMMAND} {ANSWERING_COMMAND} --task-id ID`, which writes nothing\nand opens no task, and returns its answers as text: which it is sure of, with\nits reasons, and which it is unsure of, which go to the owner.')
    briefer.add_argument('task_id', metavar='ID', help='the session whose questions are handed over')
    return run

def run(args: argparse.Namespace) -> None:
    get_task_questions_answer_brief(args.task_id)
