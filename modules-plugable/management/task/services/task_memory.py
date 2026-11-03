#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
_m_errors = import_module('modules-plugable.management.task.errors.errors')
Task_Error_NotFound = _m_errors.Task_Error_NotFound
Task_Error_WrittenByPredecessor = _m_errors.Task_Error_WrittenByPredecessor
_files = import_module('modules-plugable.management.task.services.task_files')
_adapter = import_module('modules-plugable.management.task.services.task_predecessor_adapter')
_generation = import_module('modules-plugable.management.task.services.task_generation')
OLD_SHAPE_READER = 'modules-plugable/management/task/services/task_predecessor_adapter.py'
PLAN_NAME = _adapter.PLAN_NAME
REPORT_NAME = _adapter.REPORT_NAME
TASK_FACTS_NAME = _files.TASK_FACTS_NAME
AUTHOR = _files.AUTHOR
FACTS = _files.FACTS
create_task = _files.create_task
read_facts = _files.read_facts
plan_body = _files.plan_body
plan_front = _files.plan_front
record_of = _files.record_of
facts_named_project = _files.facts_named_project


def _as_path(folder) -> Path | None:
    return folder if isinstance(folder, Path) else None


def accepts_contents(folder) -> bool:
    return _files.has_task(folder)


def _earlier_shape(folder) -> bool:
    path = _as_path(folder)
    return not accepts_contents(folder) and path is not None and (path / PLAN_NAME).is_file()


def has_task(folder) -> bool:
    if accepts_contents(folder):
        return True
    path = _as_path(folder)
    return path is not None and (path / PLAN_NAME).is_file()


def has_plan(folder) -> bool:
    return has_task(folder)


def plan_path(folder) -> Path:
    path = _as_path(folder)
    if _earlier_shape(folder) and path is not None:
        return path / PLAN_NAME
    return _files.plan_path(folder)


def report_path(folder) -> Path:
    path = _as_path(folder)
    if _earlier_shape(folder) and path is not None:
        return path / REPORT_NAME
    return _files.report_path(folder)


def plan_text(folder) -> str:
    return _adapter.read_plan(folder) if _earlier_shape(folder) else _files.plan_text(folder)


def report_text(folder) -> str:
    return _adapter.read_report(folder)[0] if _earlier_shape(folder) else _files.report_text(folder)


def has_report(folder) -> bool:
    return _adapter.read_report(folder)[1] if _earlier_shape(folder) else _files.has_report(folder)


def report_lines(folder) -> list:
    return _adapter.read_report_lines(folder) if _earlier_shape(folder) else _files.report_lines(folder)


def record_names(names) -> list:
    return _files.record_names(names) or [PLAN_NAME, REPORT_NAME]


class MemoryTaskStores(_files.FileTaskStores):

    def _folder(self, project, task) -> Path:
        folder = self.resolve(project, task)
        if not has_task(folder):
            raise Task_Error_NotFound()
        return folder

    def _read(self, project, task, fact: str) -> tuple:
        folder = self._folder(project, task)
        if accepts_contents(folder):
            return super()._read(project, task, fact)
        text = _adapter.read_fact(folder, fact)
        return (text, _files._version(text))

    def _replace(self, project, task, fact: str, value: str, expected: str) -> str:
        if not accepts_contents(self._folder(project, task)):
            raise Task_Error_WrittenByPredecessor(_generation.FIRST_GENERATION_TYPE_UUID, _generation.TASK_TYPE_UUID, _generation.CONVERSION_SERVICE)
        return super()._replace(project, task, fact, value, expected)


def stores_at(folder) -> MemoryTaskStores:
    tid = folder if isinstance(folder, str) else Path(folder).name
    return MemoryTaskStores(lambda project, task: tid)


def stores() -> MemoryTaskStores:
    def resolve(project, task):
        return task if isinstance(task, str) else Path(task).name
    return MemoryTaskStores(resolve)
