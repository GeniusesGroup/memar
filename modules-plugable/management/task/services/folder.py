#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/folder.py — one task as services read it.

Tasks live on the records branch. The task's identity is its id string. A Path
is only a transitional handle (tests that still mkdir a fixture, or callers that
have not moved to the id) — never the store.
"""
from __future__ import annotations
from modules.identity.thing.labels.Queued import Label_Queued
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
task_dir = _m_memar_location.task_dir
tasks_root = _m_memar_location.tasks_root
import os
import time
from pathlib import Path
from typing import NamedTuple
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
registered_locations = _m_task_location.registered_locations
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
plan_file_problem = _m_plan_file.plan_file_problem
read_plan = _m_plan_file.read_plan
has_plan = import_module('modules-plugable.management.task.services.task_memory').has_plan
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_task_files = import_module('modules-plugable.management.task.services.task_files')
TASK_FACTS_NAME = _m_task_files.TASK_FACTS_NAME
read_facts = _m_task_files.read_facts
DAY_SECONDS = 24 * 60 * 60

def _store():
    return import_module('bundles.memar_git.services.task_store')

def _task_id(task) -> str:
    return task if isinstance(task, str) else Path(task).name

def _front_from_facts(facts: dict) -> dict[str, str]:
    return {PlanKey.TITLE.key: facts.get('title', ''), PlanKey.PROJECT.key: str(facts.get('project', '')), PlanKey.PARENT.key: facts.get('parent') or '', PlanKey.CONVERSATION.key: facts.get('conversation') or '', PlanKey.PRIORITY.key: facts.get('priority') or '', PlanKey.DEPENDS_ON.key: facts.get('depends_on') or '', PlanKey.START_DATE.key: facts.get('start_date') or ''}

class Task(NamedTuple):
    """One task by id. `disk` is set only for an on-disk fixture; prefer `.id`."""
    id: str
    has_plan: bool
    front: dict[str, str] | None
    status: str
    readable: bool = True
    shape: str | None = None
    disk: Path | None = None

    @property
    def path(self) -> Path:
        """Transitional Path handle; durable state is on the records branch by `.id`."""
        return self.disk if self.disk is not None else task_dir(self.id)

    @property
    def parent(self) -> str:
        return (self.front or {}).get(PlanKey.PARENT.key, '')

    @property
    def conversation(self) -> str:
        return (self.front or {}).get(PlanKey.CONVERSATION.key, '') or self.id

def read_task(task) -> Task:
    """Read TASK (id string or Path handle) from the records branch, else a disk fixture."""
    tid = _task_id(task)
    disk = task if isinstance(task, Path) and task.is_dir() else None
    files = _store().tree(tid)
    if TASK_FACTS_NAME in files:
        facts = read_facts(tid) or {}
        return Task(tid, True, _front_from_facts(facts), (facts.get('status') or '').lower(), disk=disk)
    if PLAN_NAME in files:
        try:
            lines = files[PLAN_NAME].decode('utf-8-sig').splitlines()
            front, _ = _m_plan_file.front_matter(lines)
            if front is not None:
                front = _m_plan_file.PLAN.current({key.lower(): value for key, value in front.items() if key == _m_plan_file.front_key(key)})
            status = _m_plan_file.status_word((front or {}).get('status', ''))
            shape = _m_plan_file.plan_shape_problem(lines)
            return Task(tid, True, front, status, shape=shape, disk=disk)
        except (OSError, UnicodeDecodeError):
            return Task(tid, True, None, '', readable=False, disk=disk)
    if disk is not None and has_plan(disk):
        plan = disk / PLAN_NAME
        if (disk / TASK_FACTS_NAME).is_file():
            facts = read_facts(disk) or {}
            return Task(tid, True, _front_from_facts(facts), (facts.get('status') or '').lower(), disk=disk)
        try:
            read = read_plan(plan)
        except (OSError, UnicodeDecodeError):
            return Task(tid, True, None, '', readable=False, disk=disk)
        return Task(tid, True, read.front, read.status, shape=plan_file_problem(plan), disk=disk)
    return Task(tid, False, None, '', disk=disk)

def queued_why(task: Task) -> str | None:
    if task.status == Label_Queued.key:
        return f'its Status is {Label_Queued.title}'
    return None

def is_task_folder(entry) -> bool:
    """True when ENTRY (id or Path) names a task on the branch, a TaskId-named directory, or a disk plan fixture."""
    if isinstance(entry, str):
        return has_plan(entry) or _store().on_branch(entry)
    if entry.is_symlink():
        return False
    if has_plan(entry):
        return True
    if not entry.is_dir():
        return False
    if TaskId.is_form(entry.name):
        return True
    plan = entry / PLAN_NAME
    if not plan.is_file():
        return False
    try:
        front = read_plan(plan).front or {}
    except (OSError, UnicodeDecodeError):
        return False
    return PlanKey.TITLE.key in front and PlanKey.START_DATE.key in front

def _project_entries(task_id: str, also: Path | None) -> list[Path]:
    locations = ([also] if also is not None else []) + registered_locations()
    return [entry for entry in (location / task_id for location in locations) if entry.exists() or entry.is_symlink()]

def project_folder_of(task_id: str, also: Path | None=None) -> Path | None:
    return next((entry for entry in _project_entries(task_id, also) if is_task_folder(entry)), None)

def foreign_project_entry(task_id: str, also: Path | None=None) -> Path | None:
    return next((entry for entry in _project_entries(task_id, also) if not is_task_folder(entry)), None)

def folder_of(task_id: str) -> Path:
    """Transitional Path whose .name is TASK_ID. Prefer the id string at call sites."""
    if not task_id or task_id in ('.', '..') or '/' in task_id or '\\' in task_id:
        from machine.console import fail
        fail(f'refusing task id {task_id!r}: name one folder segment, not a path.')
    return task_dir(task_id)

def task_exists(task_id: str) -> bool:
    return _store().on_branch(task_id) or project_folder_of(task_id) is not None

def _entries(root: Path) -> list[Path]:
    try:
        return list(root.iterdir())
    except OSError:
        return []

def task_folders(*, projects: bool=False, locations: list[Path] | None=None) -> list[Path]:
    """Path handles for every task id on the records branch, newest first (transitional)."""
    folders = [task_dir(task_id) for task_id in _store().list_task_ids()]
    known = {each.name for each in folders}
    roots: list[Path] = []
    for root in [*(registered_locations() if projects else []), *(locations or [])]:
        if root.resolve() not in roots:
            roots.append(root.resolve())
    for root in roots:
        for entry in _entries(root):
            if entry.name not in known and is_task_folder(entry):
                folders.append(entry)
                known.add(entry.name)
    folders.sort(key=lambda entry: (TaskId.is_form(entry.name), entry.name), reverse=True)
    return folders

def task_ids(*, projects: bool=False, locations: list[Path] | None=None) -> list[str]:
    """Task ids on the records branch (and optional disk locations), newest first."""
    return [path.name for path in task_folders(projects=projects, locations=locations)]

def last_change(path: Path) -> float:
    if path.is_dir():
        latest = path.stat().st_mtime
        for root, folders, files in os.walk(path):
            for name in (*folders, *files):
                try:
                    changed = os.stat(os.path.join(root, name), follow_symlinks=False).st_mtime
                except OSError:
                    continue
                latest = max(latest, changed)
        return latest
    return time.time()

def measured_idle(path: Path) -> float | None:
    try:
        if not path.exists():
            return None
        return (time.time() - last_change(path)) / DAY_SECONDS
    except OSError:
        return None
