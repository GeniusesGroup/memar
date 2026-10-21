#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/ai/services/new_chats.py — the prompt that asks the owner to run sessions each in a completely new chat.

A chat that meets sessions it cannot do in its own context (owner, 2026-10-16)
hands each to a new chat, because a chat that takes in several sessions'
reading and their questions and answers grows past 500K tokens and every later
turn pays for all of it. Where the agent cannot open a chat itself, this text is
what it shows the owner: for each session its title, its priority, the first
sentence of its Why, and the text that hands the session over, which is
`plan_brief`'s, taken from its function so the words cannot differ. The
text is built from the ids alone and writes nothing; the agent adds nothing to
it, and says in one line, outside it, that its runtime cannot open a chat.

Which sessions block the chat's work is the coordinator's plan to state, in its
`Depends_on` (`depends_on`): `--coordinator ID` names the coordinator's session,
and each session asked for that its plan cites is marked "blocks", the text
then telling the owner to say when each of those is done. `--blocking` marks
more by hand, over what the plan says.
"""
from __future__ import annotations
import argparse
import re
from modules.knowledge.documentation.plan.primitive.plan_part import PlanPart
from typing import Callable
from machine.console import fail
from modules.management.task.services.dependency import DependsOn
from .get_task_plan_carry_out_brief import brief_text
from modules.management.task.services.folder import folder_of, is_task_folder
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, part_text, read_plan
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
NEW_CHATS_COMMAND = 'get-new-chats-ask'
INTRO = 'Please run each session below in a completely new chat: open the chat, paste the text under its title, and let it end. A session marked "blocks" stops the work of the chat that asked until it is done; say "<id> is done" there when it ends. A session marked "independent" can run now, at the same time as the others, in its own chat.'

def _first_sentence(text: str) -> str:
    """The first sentence of TEXT, on one line; empty when TEXT is."""
    one_line = ' '.join(text.split())
    return re.split('(?<=[.!?])\\s', one_line, maxsplit=1)[0] if one_line else ''

def coordinator_blocking(coordinator: str, task_ids: list[str]) -> list[str]:
    """The sessions among TASK_IDS that COORDINATOR's plan cites in its Depends_on: the ones it cannot go on without."""
    folder = folder_of(coordinator)
    if not is_task_folder(folder) or not (folder / PLAN_NAME).is_file():
        fail(f'no coordinator session {coordinator}: it has no session folder with a {PLAN_NAME}')
    cited = DependsOn.of(read_plan(folder / PLAN_NAME).front).ids()
    return [each for each in task_ids if each in cited]

def chats_text(task_ids: list[str], blocking: list[str]) -> str:
    """The message asking for one new chat per session in TASK_IDS, those in BLOCKING marked as blocking."""
    parts = [INTRO]
    for task_id in task_ids:
        plan = folder_of(task_id) / PLAN_NAME
        front = read_plan(plan).front or {}
        mark = 'blocks' if task_id in blocking else 'independent'
        why = _first_sentence(part_text(plan, PlanPart.WHY.heading))
        parts.append(f"{front.get('title', task_id)} — priority {front.get('priority', '?')} — {mark}\nWhy: {why}\n{brief_text(task_id)}")
    return '\n\n'.join(parts)

def get_new_chats_ask(task_ids: list[str], blocking: list[str], coordinator: str | None=None) -> None:
    """Print the message for TASK_IDS, once each one's folder and plan are there and BLOCKING names only among them."""
    for task_id in task_ids:
        folder = folder_of(task_id)
        if not is_task_folder(folder) or not (folder / PLAN_NAME).is_file():
            fail(f'no session to ask a chat for in {task_id}: it has no session folder with a {PLAN_NAME}')
    outside = [each for each in blocking if each not in task_ids]
    if outside:
        fail(f"--blocking names {', '.join(outside)}, not among the sessions asked for")
    if coordinator is not None:
        planned = coordinator_blocking(coordinator, task_ids)
        blocking = [*planned, *(each for each in blocking if each not in planned)]
    print(chats_text(task_ids, blocking))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar ai get-new-chats-ask`."""
    asker = verbs.add_parser(NEW_CHATS_COMMAND, help='print the message that asks the owner to run sessions each in a completely new chat', description=f"Print the message that asks the owner to run each session ID in a completely\nnew chat, ready to show: for each its title, priority, the first sentence of\nits Why, and the text that hands it over (the one `get-task-plan-carry-out-brief`\nprints). A session the asking chat cannot go on without is marked blocks, the others\nindependent, to run in parallel. The chat's own session, given with --coordinator, says\nwhich: those in its {PlanKey.DEPENDS_ON.written}. --blocking marks more by hand. Writes nothing.\n\nWhere your agent app has a tool that starts a chat, start one per session and hand it only\nthe text `get-task-plan-carry-out-brief` prints; where it has none, show this message and\nsay in one line that you cannot start a chat. You cannot learn that another chat ended: ask\nthe owner to say when each blocking one is done, meanwhile do only the work no waiting\nsession touches, and end your turn when none is left. An independent session is written\nwhole, opened or listed, and then left: its exchanges with the owner and its end are not\nyours to follow; two that change the same files are listed one after the other.\n\nWork your chat needs that cannot be specified exactly to an agent, because it needs\nback-and-forth with the owner, is neither done nor delegated by your chat: set your plan\nBlocked on its session, open its chat for the owner, say in one message which chat to go\nto and what it must produce, and stop until the owner says it is done.")
    asker.add_argument('task_ids', nargs='+', metavar='ID', help='the sessions to run, one chat each')
    asker.add_argument('--coordinator', default=None, metavar='ID', help=f"the asking chat's own session: each ID in its plan's {PlanKey.DEPENDS_ON.written} is marked as blocking")
    asker.add_argument('--blocking', action='append', default=[], metavar='ID', help='a session the asking chat waits for, in addition; may be repeated')
    return run

def run(args: argparse.Namespace) -> None:
    get_new_chats_ask(args.task_ids, args.blocking, args.coordinator)
