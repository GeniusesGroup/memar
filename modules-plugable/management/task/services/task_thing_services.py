#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import Any
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN = _m_record.PLAN
Label_Status = import_module('modules-plugable.knowledge.label.status.labels.Status').Label_Status
thing_of_task = import_module('modules-plugable.management.task.widgets.thing_of_task.thing_of_task')
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
status_word = _m_plan_text.status_word
project_root = import_module('modules-plugable.management.task.services.task_location').project_root
project_by_path = import_module('modules.computer.software.services.project_find').project_by_path
SERVICE_SET_STATUS = import_module('modules-plugable.knowledge.label.status.services.set_status').SERVICE_SET
SERVICE_READ_STATUS = import_module('modules-plugable.knowledge.label.status.services.read_status').SERVICE_READ
SERVICE_ATTACH_LABEL = '4b2d85c3-fc90-5183-9a57-6be190163752'
SERVICE_SET_PRIORITY = import_module('modules-plugable.identity.thing.priority.services.set_priority').SERVICE_UUID
SERVICE_READ_PRIORITY = import_module('modules-plugable.identity.thing.priority.services.read_priority').SERVICE_UUID
DEFAULT_PRIORITY_NOTE = '(default lowest)'
NO_STATUS = '(none)'


def status_words() -> tuple[type, ...]:
    return Label_Status.for_document(PLAN.kind)


def registry(services=None):
    if services is not None:
        return services
    return import_module('modules.process.services.composition').process_services()


def thing_id(task_id) -> str:
    return thing_of_task.open(task_id)


def project_for(task, project: Path | str | None = None) -> Path | None:
    if project is not None:
        text = str(project).strip()
        if text:
            return project_root(project_by_path(text))
    front = task if isinstance(task, dict) else None
    if front is None and not isinstance(task, (str, Path)):
        front = getattr(task, 'front', None)
    if front is None and isinstance(task, str):
        front = import_module('modules-plugable.management.task.services.folder').read_task(task).front
    named = (front or {}).get(PlanKey.PROJECT.key, '').strip()
    if not named:
        return None
    return project_root(project_by_path(named))


def _status_key(text: str) -> str:
    line = text.splitlines()[0]
    key = line.split(' status ', 1)[1].split(',', 1)[0].strip()
    if key == NO_STATUS:
        return ''
    return status_word(key)


def read_status_key(task_id: str, project: Any = None, services=None) -> str:
    held = registry(services).get_by_id(SERVICE_READ_STATUS).do(thing=thing_id(task_id), project=project)
    return _status_key(held)


def set_status(task_id, word: str, project: Any = None, only_from: tuple[str, ...] | None = None, services=None) -> None:
    arguments = {'thing': thing_id(task_id), 'word': word, 'project': project}
    if only_from is not None:
        arguments['only_from'] = only_from
    registry(services).get_by_id(SERVICE_SET_STATUS).do(**arguments)


def attach_label(task_id, label, project: Any = None, services=None) -> None:
    registry(services).get_by_id(SERVICE_ATTACH_LABEL).do(thing=thing_id(task_id), word=str(label), project=project)


def set_priority(task_id: str, value: str | int, project: Any = None, services=None) -> None:
    registry(services).get_by_id(SERVICE_SET_PRIORITY).do(thing=thing_id(task_id), word=str(int(value)), project=project)


def read_priority_rank(task_id: str, project: Any = None, services=None) -> int:
    held = registry(services).get_by_id(SERVICE_READ_PRIORITY).do(thing=thing_id(task_id), project=project)
    if DEFAULT_PRIORITY_NOTE in held:
        return int(import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank.of_absent())
    return int(held.split(' priority ', 1)[1].split()[0])
