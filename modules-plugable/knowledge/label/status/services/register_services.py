#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from machine.console import fail

set_status_service = import_module('modules-plugable.knowledge.label.status.services.set_status')
read_status_service = import_module('modules-plugable.knowledge.label.status.services.read_status')
status_widget = import_module('modules-plugable.knowledge.label.status.widgets.status').status
TaskStatusStore = import_module('modules-plugable.management.task.services.task_status_store').TaskStatusStore
is_task_folder = import_module('modules-plugable.management.task.services.folder').is_task_folder
has_plan = import_module('modules-plugable.management.task.services.task_memory').has_plan
stores_at = import_module('modules-plugable.management.task.services.task_memory').stores_at


def _status_store(task_id: str, service_id: str):
    if not task_id:
        fail(f'service {service_id} needs thing')
    if not is_task_folder(task_id) or not has_plan(task_id):
        fail(f'no task {task_id}, so there is no status to read or set')
    return TaskStatusStore(stores_at(task_id))


class Set_Status:

    def operation_id(self) -> str:
        return set_status_service.SERVICE_SET

    def summary(self) -> str:
        return 'Set Status'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        if word is None:
            fail(f'service {set_status_service.SERVICE_SET} needs thing and word')
        store = _status_store(thing, set_status_service.SERVICE_SET)
        return status_widget(store, thing, TaskStatusStore.words(), word, only_from)


class Read_Status:

    def operation_id(self) -> str:
        return read_status_service.SERVICE_READ

    def summary(self) -> str:
        return 'Read Status'

    def do(self, *, thing=None, word=None, project=None, only_from=None):
        store = _status_store(thing, read_status_service.SERVICE_READ)
        return status_widget(store, thing, TaskStatusStore.words())


def register_services(services) -> None:
    services.register(Set_Status())
    services.register(Read_Status())
