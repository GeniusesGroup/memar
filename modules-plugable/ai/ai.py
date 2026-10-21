#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/ai/ai.py — `memar ai`: agent-context verbs (start, briefs, answering, new chats).

Groups the how-agents-run verbs that left process/session. Not Task. Each verb
is declared by its own service under services/.
"""
from __future__ import annotations
AI_COMMAND = 'ai'
SUMMARY = 'load and hand agent context for a task folder; not the task queue itself'
DESCRIPTION = "memar ai — agent context around a task folder\n\nVerbs here get what an agent reads first (`get-task-init-context`), answer a task's open\nquestions (`get-task-answer-context`), and hand briefs or ask for new chats.\nQueue, claim, and list live under `memar task`. Records keep/sweep live under\n`memar git`.\n\nEach verb below says what it does in its own --help.\n"

def describe(verbs) -> None:
    """`memar ai`, which only groups its verbs."""
    verbs.add_parser(AI_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
