#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import argparse
import re
from pathlib import Path
Why = import_module('modules-plugable.knowledge.documentation.plan.primitive.why').Why
from typing import Callable
from machine.console import fail
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DependsOn = _m_dependency.DependsOn
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from .get_task_plan_carry_out_brief import brief_text
_m_storage = import_module('modules-plugable.ai.services.agent_task_storage')
folder_of = _m_storage.handle
is_task_folder = _m_storage.is_task_folder
has_plan = _m_storage.has_plan
plan_front = _m_storage.plan_front
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
part_text = _m_plan_file.part_text
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
NEW_CHATS_COMMAND = 'get-new-chats-ask'
INTRO = 'Please run each task below in a completely new chat: open the chat, paste the text under its title, and let it end. A task marked "blocks" stops the work of the chat that asked until it is done; say "<id> is done" there when it ends. A task marked "independent" can run now, at the same time as the others, in its own chat.'

def _first_sentence(text: str) -> str:
    one_line = ' '.join(text.split())
    return re.split('(?<=[.!?])\\s', one_line, maxsplit=1)[0] if one_line else ''

def _front(folder) -> dict:
    held = plan_front(folder)
    if held is not None:
        return held[0] or {}
    return {}

def own_task_blocking(own_task_id: str, task_ids: list[str]) -> list[str]:
    if not is_task_folder(own_task_id) or not has_plan(own_task_id):
        fail(f'no task {own_task_id}: it has no task with a plan (task.yaml and a plan content, or {PLAN_NAME})')
    cited = DependsOn.of(_front(own_task_id)).ids()
    return [each for each in task_ids if each in cited]

def chats_text(task_ids: list[str], blocking: list[str]) -> str:
    parts = [INTRO]
    for task_id in task_ids:
        front = _front(task_id)
        mark = 'blocks' if task_id in blocking else 'independent'
        why = _first_sentence(part_text(Path(task_id) / PLAN_NAME, Why.heading))
        parts.append(f"{front.get('title', task_id)} — priority {front.get('priority', '?')} — {mark}\nWhy: {why}\n{brief_text(task_id)}")
    return '\n\n'.join(parts)

def get_new_chats_ask(task_ids: list[str], blocking: list[str], own_task_id: str | None=None) -> None:
    for task_id in task_ids:
        if not is_task_folder(task_id) or not has_plan(task_id):
            fail(f'no task to ask a chat for in {task_id}: it has no task with a plan (task.yaml and a plan content, or {PLAN_NAME})')
    outside = [each for each in blocking if each not in task_ids]
    if outside:
        fail(f"--blocking names {', '.join(outside)}, not among the tasks asked for")
    if own_task_id is not None:
        planned = own_task_blocking(own_task_id, task_ids)
        blocking = [*planned, *(each for each in blocking if each not in planned)]
    print(chats_text(task_ids, blocking))

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    asker = verbs.add_parser(NEW_CHATS_COMMAND, help='print the message that asks the owner to run tasks each in a completely new chat', description=f"Print the message that asks the owner to run each task ID in a completely\nnew chat, ready to show: for each its title, priority, the first sentence of\nits Why, and the text that hands it over (the one `get-task-plan-carry-out-brief`\nprints). A task the asking chat cannot go on without is marked blocks, the others\nindependent, to run in parallel. The chat's own task, given with {TaskId.FLAG}, says\nwhich: those in its {PlanKey.DEPENDS_ON.written}. --blocking marks more by hand. Writes nothing.\n\nWhere your agent app has a tool that starts a chat, start one per task and hand it only\nthe text `get-task-plan-carry-out-brief` prints; where it has none, show this message and\nsay in one line that you cannot start a chat. You cannot learn that another chat ended: ask\nthe owner to say when each blocking one is done, meanwhile do only the work no waiting\ntask touches, and end your turn when none is left. An independent task is written\nwhole, opened or listed, and then left: its exchanges with the owner and its end are not\nyours to follow; two that change the same files are listed one after the other. Say how many chats you opened.\n\nWork your chat needs that cannot be specified exactly to an agent, because it needs\nback-and-forth with the owner, is neither done nor delegated by your chat: set your plan\nBlocked on its task, open its chat for the owner, say in one message which chat to go\nto and what it must produce, and stop until the owner says it is done.")
    asker.add_argument('task_ids', nargs='+', metavar='ID', help='the tasks to run, one chat each')
    TaskId.add_flag(asker, f"the asking chat's own task: each ID in its plan's {PlanKey.DEPENDS_ON.written} is marked as blocking")
    asker.add_argument('--blocking', action='append', default=[], metavar='ID', help='a task the asking chat waits for, in addition; may be repeated')
    return run

def run(args: argparse.Namespace) -> None:
    get_new_chats_ask(args.task_ids, args.blocking, args.task_id)
