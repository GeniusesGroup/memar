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
priority_on_graph = import_module('modules-plugable.identity.thing.priority.services.graph_priority_ops').priority_on_graph
graph_thing = import_module('modules-plugable.knowledge.label.services.graph_thing')
wired_opener = import_module('modules-plugable.management.task.services.graph_wiring').wired_opener


class Set_Priority:

    def __init__(self, opener=None) -> None:
        self.opener = opener or wired_opener

    def operation_id(self) -> str:
        return SET_UUID

    def summary(self) -> str:
        return 'Set Priority'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        if not thing or word is None:
            fail(f'service {SET_UUID} needs thing and word')
        stores = graph_thing.graph_stores(thing, project, self.opener, SET_UUID)
        try:
            set_priority(stores.labels, priority_on_graph(stores.graph), stores.thing, word)
        except graph_thing.REFUSED as refused:
            fail(str(refused))
        return f'{thing}  priority {word}'


class Read_Priority:

    def __init__(self, opener=None) -> None:
        self.opener = opener or wired_opener

    def operation_id(self) -> str:
        return READ_UUID

    def summary(self) -> str:
        return 'Read Priority'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        if not thing:
            fail(f'service {READ_UUID} needs thing')
        stores = graph_thing.graph_stores(thing, project, self.opener, READ_UUID)
        try:
            value, found = read_priority(stores.labels, priority_on_graph(stores.graph), stores.thing)
            held_rank = rank(stores.labels, priority_on_graph(stores.graph), stores.thing)
        except graph_thing.REFUSED as refused:
            fail(str(refused))
        note = ' (default lowest)' if not found else ''
        return f'{thing}  priority {int(value)}{note}  rank {held_rank}'


def register_services(services, opener=None) -> None:
    held = opener or wired_opener
    services.register(Set_Priority(held))
    services.register(Read_Priority(held))
