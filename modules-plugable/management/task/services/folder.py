#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/folder.py — one task as services read it.

Tasks live on the records branch. A Path here is only a handle whose .name is
the task id — not a directory agents should open.
"""
from __future__ import annotations
from modules.identity.thing.labels.Label_Queued import Label_Queued
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
task_dir = _m_fs_memar.task_dir
tasks_root = _m_fs_memar.tasks_root
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
    return import_module('modules-plugable.computer.git.services.task_store')

class Task(NamedTuple):
    """One task: a Path handle (.name == id), whether it has a plan, and what the plan says."""
    path: Path
    has_plan: bool
    front: dict[str, str] | None
    status: str
    readable: bool = True
    shape: str | None = None

    @property
    def id(self) -> str:
        return self.path.name

    @property
    def parent(self) -> str:
        return (self.front or {}).get(PlanKey.PARENT.key, '')

    @property
    def conversation(self) -> str:
        return (self.front or {}).get(PlanKey.CONVERSATION.key, '') or self.id

def read_task(folder: Path) -> Task:
    """Read TASK from the records branch (or a real directory if tests still use one)."""
    if folder.is_dir() and has_plan(folder):
        plan = folder / PLAN_NAME
        if (folder / TASK_FACTS_NAME).is_file():
            facts = read_facts(folder) or {}
            front = {PlanKey.TITLE.key: facts.get('title', ''), PlanKey.PROJECT.key: str(facts.get('project', '')), PlanKey.PARENT.key: facts.get('parent') or '', PlanKey.CONVERSATION.key: facts.get('conversation') or '', PlanKey.PRIORITY.key: facts.get('priority') or '', PlanKey.DEPENDS_ON.key: facts.get('depends_on') or '', PlanKey.START_DATE.key: facts.get('start_date') or ''}
            return Task(folder, True, front, (facts.get('status') or '').lower())
        try:
            read = read_plan(plan)
        except (OSError, UnicodeDecodeError):
            return Task(folder, True, None, '', readable=False)
        return Task(folder, True, read.front, read.status, shape=plan_file_problem(plan))
    files = _store().tree(folder.name)
    if TASK_FACTS_NAME in files:
        facts = read_facts(folder.name) or {}
        front = {PlanKey.TITLE.key: facts.get('title', ''), PlanKey.PROJECT.key: str(facts.get('project', '')), PlanKey.PARENT.key: facts.get('parent') or '', PlanKey.CONVERSATION.key: facts.get('conversation') or '', PlanKey.PRIORITY.key: facts.get('priority') or '', PlanKey.DEPENDS_ON.key: facts.get('depends_on') or '', PlanKey.START_DATE.key: facts.get('start_date') or ''}
        return Task(folder, True, front, (facts.get('status') or '').lower())
    if PLAN_NAME in files:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.md', delete=False) as handle:
            handle.write(files[PLAN_NAME])
            temp = Path(handle.name)
        try:
            read = read_plan(temp)
        except (OSError, UnicodeDecodeError):
            return Task(folder, True, None, '', readable=False)
        finally:
            temp.unlink(missing_ok=True)
        return Task(folder, True, read.front, read.status, shape=plan_file_problem(temp) if temp.exists() else None)
    return Task(folder, False, None, '')

def queued_why(task: Task) -> str | None:
    if task.status == Label_Queued.key:
        return f'its Status is {Label_Queued.word}'
    return None

def is_task_folder(entry: Path) -> bool:
    if entry.is_symlink() or not entry.is_dir():
        return False
    if TaskId.is_form(entry.name):
        return True
    plan = entry / PLAN_NAME
    if not has_plan(entry):
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
    """Path handle for TASK_ID (.name == id). Not a directory; content is on the records branch."""
    return task_dir(task_id)

def task_exists(task_id: str) -> bool:
    return _store().on_branch(task_id) or project_folder_of(task_id) is not None

def _entries(root: Path) -> list[Path]:
    try:
        return list(root.iterdir())
    except OSError:
        return []

def task_folders(*, projects: bool=False, locations: list[Path] | None=None) -> list[Path]:
    """Path handles for every task id on the records branch, newest first."""
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
        return (time.time() - last_change(path)) / DAY_SECONDS
    except OSError:
        return None
