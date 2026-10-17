#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/prompts_questions_brief.py — the prompt that hands a session's questions to an agent to answer.

A coordinating session does not bring the owner a question another agent can
answer: the owner's answer is the slower one (owner, 2026-10-15). So this
prints a second fixed text, from the id alone as the plan's brief is
(`prompts_plan_brief`), which hands over not the session's task but its
questions: the lines under `Decisions needed` in its report, where a session's
questions for the owner already stand and where the digest gathers them. The
agent it is handed to takes nothing up: it runs
`memar prompts answer-session-questions` (`prompts_answering`), which prints
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

import argparse
from typing import Callable

from machine.console import fail
from services.prompts import PROMPTS_COMMAND
from services.prompts_answering import ANSWERING_COMMAND, questions_problem
from services.session_folder import folder_of, is_session_folder
from services.session_plan import PLAN_NAME
from services.session_record import REPORT
from services.session_report import REPORT_NAME

# TODO name: hand-session-questions-to-answer | hand-over-session-questions | delegate-session-questions
QUESTIONS_BRIEF_COMMAND = "hand-session-questions-to-answer"


def questions_brief_text(session_id: str) -> str:
    """The text that hands SESSION_ID's questions, not its task, to an agent that answers them, ready to paste."""
    return (
        f"Your task is to answer the questions of session {session_id}, not to take it up. "
        f"Run `memar {PROMPTS_COMMAND} {ANSWERING_COMMAND} --session-id {session_id}` first, before anything else, and follow what it prints."
    )


def print_questions_brief(session_id: str) -> None:
    """Print the text that hands SESSION_ID's questions over, once its folder, its plan and a question under its report's hand-back part are there."""
    folder = folder_of(session_id)
    if not is_session_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(f"no questions to answer in {session_id}: it has no session folder with a {PLAN_NAME}")
    problem = questions_problem(folder)
    if problem:
        fail(f"no questions to answer in {session_id}: {problem}")
    print(questions_brief_text(session_id))


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar prompts hand-session-questions-to-answer`."""
    briefer = verbs.add_parser(
        QUESTIONS_BRIEF_COMMAND,
        help="print the text that hands a session's open questions to an agent to answer",
        description=(
            "Print the text that hands the questions of the session ID, not its task, to an\n"
            "agent that answers them, with ID filled in, ready to paste. A coordinating\n"
            "session hands it over, adding nothing, before it brings a question to the owner.\n"
            f"The questions are the lines under `{REPORT.hand_back_part}` in its {REPORT_NAME}; a session\n"
            "with none is refused.\n"
            "\n"
            f"The agent runs `memar {PROMPTS_COMMAND} {ANSWERING_COMMAND} --session-id ID`, which writes nothing\n"
            "and opens no session, and returns its answers as text: which it is sure of, with\n"
            "its reasons, and which it is unsure of, which go to the owner."
        ),
    )
    briefer.add_argument("session_id", metavar="ID", help="the session whose questions are handed over")
    return run


def run(args: argparse.Namespace) -> None:
    print_questions_brief(args.session_id)
