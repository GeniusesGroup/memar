#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
"""One storage surface for AI agent-context verbs that still touch a task.

Callers pass a task id string. Durable state is the records branch; the only
Path this module opens is scratch under temp/ for the context-read record
([rewrite-uses-memory-adapter]).
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
_m_folder = import_module('modules-plugable.management.task.services.folder')
is_task_folder = _m_folder.is_task_folder
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
has_plan = _m_task_files.has_plan
plan_path = _m_task_files.plan_path
report_path = _m_task_files.report_path
plan_text = _m_task_files.plan_text
report_text = _m_task_files.report_text
plan_front = _m_task_files.plan_front
read_facts = _m_task_files.read_facts
CONTEXT_READ = 'context_read.txt'

def handle(task_id: str) -> str:
    """The task id — the durable identity. Prefer this over any Path."""
    return task_id

def tree_names(task_id: str) -> list[str]:
    held = import_module('modules-plugable.computer.git.services.task_store').tree(task_id)
    if held:
        return sorted(held)
    folder = _m_folder.folder_of(task_id)
    if folder.is_dir():
        return sorted((path.relative_to(folder).as_posix() + ('/' if path.is_dir() else '') for path in folder.rglob('*')), key=str.lower)
    return []

def context_record_path(task_id: str) -> Path:
    """Scratch path for what get-act-context already printed; never a task tree folder."""
    root = _m_memar_location.scratch_root() / 'context-read' / task_id
    root.mkdir(parents=True, exist_ok=True)
    return root / CONTEXT_READ

def project_named(task_id: str) -> Path | None:
    facts = read_facts(task_id) or {}
    named = (facts.get('project') or '').strip()
    if not named:
        front = (plan_front(task_id) or ({}, None))[0] or {}
        named = (front.get('project') or '').strip()
    return Path(named) if named else None

# Transitional re-export: callers that still asked folder_of through this module.
folder_of = _m_folder.folder_of
