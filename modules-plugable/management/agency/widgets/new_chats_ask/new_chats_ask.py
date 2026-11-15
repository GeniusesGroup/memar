#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import re
Why = import_module('modules-plugable.knowledge.documentation.plan.primitive.why').Why
from machine.console import fail
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DependsOn = _m_dependency.DependsOn
_m_storage = import_module('modules-plugable.management.agency.services.agent_task_storage.agent_task_storage')
_m_folder = import_module('modules-plugable.management.task.services.folder')
_m_plan_brief = import_module('modules-plugable.management.agency.widgets.plan_carry_out_brief.plan_carry_out_brief')
brief_text = _m_plan_brief.brief_text
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
rank_of = import_module('modules-plugable.management.task.services.task_thing_services').read_priority_rank
NEW_CHATS_COMMAND = 'get-new-chats-ask'
INTRO = 'Please run each task below in a completely new chat: open the chat, paste the text under its title, and let it end. A task marked "blocks" stops the work of the chat that asked until it is done; say "<id> is done" there when it ends. A task marked "independent" can run now, at the same time as the others, in its own chat.'


class _Storage:
    """One place durable state is reached until the memory/record adapter binds."""

    def _handle(self, task_id: str):
        if _m_storage.has_plan(task_id) or _m_storage.is_task_folder(task_id):
            return task_id
        return _m_folder.project_folder_of(task_id) or task_id

    def is_task(self, task_id: str) -> bool:
        return _m_storage.is_task_folder(task_id) or _m_folder.project_folder_of(task_id) is not None

    def has_plan(self, task_id: str) -> bool:
        handle = self._handle(task_id)
        return _m_storage.has_plan(handle)

    def plan_front(self, task_id: str) -> dict:
        held = _m_storage.plan_front(self._handle(task_id))
        if held is not None:
            return held[0] or {}
        return {}

    def plan_text(self, task_id: str) -> str:
        return _m_storage.plan_text(self._handle(task_id))


_storage = _Storage()


def _first_sentence(text: str) -> str:
    one_line = ' '.join(text.split())
    return re.split('(?<=[.!?])\\s', one_line, maxsplit=1)[0] if one_line else ''


def _heading_part(text: str, part: str) -> str:
    found: list[str] | None = None
    for line in text.splitlines():
        if line.startswith('## '):
            if found is not None:
                break
            if line[3:].strip() == part:
                found = []
        elif found is not None:
            found.append(line)
    return '\n'.join(found or []).strip()


def own_task_blocking(own_task_id: str, task_ids: list[str], storage: _Storage | None=None) -> list[str]:
    store = storage or _storage
    if not store.is_task(own_task_id) or not store.has_plan(own_task_id):
        fail(f'no task {own_task_id}: it has no plan on its timeline')
    cited = DependsOn.of(store.plan_front(own_task_id)).ids()
    return [each for each in task_ids if each in cited]


class NewChatsAsk:

    def __init__(self, storage: _Storage | None=None) -> None:
        self.storage = storage or _storage

    def text_of(self, task_ids: list[str], blocking: list[str]) -> str:
        store = self.storage
        parts = [INTRO]
        for task_id in task_ids:
            front = store.plan_front(task_id)
            mark = 'blocks' if task_id in blocking else 'independent'
            why = _first_sentence(_heading_part(store.plan_text(task_id), Why.heading))
            parts.append(f"{front.get('title', task_id)} — priority {rank_of(task_id, front.get('project'))} — {mark}\nWhy: {why}\n{brief_text(task_id)}")
        return '\n\n'.join(parts)

    def print(self, task_ids: list[str], blocking: list[str], own_task_id: str | None=None) -> None:
        store = self.storage
        for task_id in task_ids:
            if not store.is_task(task_id) or not store.has_plan(task_id):
                fail(f'no task to ask a chat for in {task_id}: it has no plan on its timeline')
        outside = [each for each in blocking if each not in task_ids]
        if outside:
            fail(f"--blocking names {', '.join(outside)}, not among the tasks asked for")
        if own_task_id is not None:
            planned = own_task_blocking(own_task_id, task_ids, store)
            blocking = [*planned, *(each for each in blocking if each not in planned)]
        print(self.text_of(task_ids, blocking))


def chats_text(task_ids: list[str], blocking: list[str]) -> str:
    return NewChatsAsk().text_of(task_ids, blocking)


def get_new_chats_ask(task_ids: list[str], blocking: list[str], own_task_id: str | None=None) -> None:
    NewChatsAsk().print(task_ids, blocking, own_task_id)
