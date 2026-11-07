#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.console import fail

set_priority = import_module('modules-plugable.identity.thing.priority.services.set_priority').set_priority
read_priority = import_module('modules-plugable.identity.thing.priority.services.read_priority').read_priority
rank = import_module('modules-plugable.identity.thing.priority.services.read_priority').rank
SET_UUID = import_module('modules-plugable.identity.thing.priority.services.set_priority').SERVICE_UUID
READ_UUID = import_module('modules-plugable.identity.thing.priority.services.read_priority').SERVICE_UUID
FactsRankStore = import_module('modules-plugable.identity.thing.priority.services.facts_rank_store').FactsRankStore
TaskLabelStore = import_module('modules-plugable.management.task.services.task_label_store').TaskLabelStore
stores_at = import_module('modules-plugable.management.task.services.task_memory').stores_at


def _priority_stores(task_id: str, project):
    facts = stores_at(task_id)
    return TaskLabelStore(facts, project), FactsRankStore(facts, project)


class Set_Priority:

    def operation_id(self) -> str:
        return SET_UUID

    def summary(self) -> str:
        return 'Set Priority'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        if not thing or word is None:
            fail(f'service {SET_UUID} needs thing and word')
        labels, ranks = _priority_stores(thing, project)
        set_priority(labels, ranks, thing, word)
        return f'{thing}  priority {word}'


class Read_Priority:

    def operation_id(self) -> str:
        return READ_UUID

    def summary(self) -> str:
        return 'Read Priority'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        if not thing:
            fail(f'service {READ_UUID} needs thing')
        labels, ranks = _priority_stores(thing, project)
        value, found = read_priority(labels, ranks, thing)
        note = ' (default lowest)' if not found else ''
        return f'{thing}  priority {int(value)}{note}  rank {rank(labels, ranks, thing)}'


def register_services(services) -> None:
    services.register(Set_Priority())
    services.register(Read_Priority())
