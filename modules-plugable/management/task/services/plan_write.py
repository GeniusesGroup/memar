#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/plan_write.py — a new plan.md written, and an existing one queued.

The two acts on a plan that `task_ensure` asks of a task folder. A plan that is there is never
written over; a plan is queued only while it is active and no agent has claimed it, so a task
being worked, or one finished, is never put back in line.
"""
from __future__ import annotations
from importlib import import_module
from datetime import datetime, timezone
from pathlib import Path
from machine.console import fail
is_claimed = import_module('modules-plugable.management.task.services.claim').is_claimed
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
plan_file_problem = _m_plan_file.plan_file_problem
plan_skeleton = _m_plan_file.plan_skeleton
read_plan = _m_plan_file.read_plan
_m_plan_status = import_module('modules-plugable.management.task.services.plan_status')
set_status = _m_plan_status.set_status
from modules.knowledge.label.primitive.label import Labels
from modules.knowledge.status.primitive.status import Status

def write_plan(folder: Path, task: str, title: str, parent: str | None, conversation: str | None, project: Path, status: str=Status.ACTIVE.key, priority: int | None=None, labels: Labels | None=None, depends_on: str | None=None) -> None:
    """Create FOLDER's plan.md unless one is there; an existing plan is never touched.

    TASK is the id of the task the plan belongs to, and is written into
    the plan itself (`task_plan.plan_skeleton`).
    """
    opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    text = plan_skeleton(task, title, opened, project, parent=parent, conversation=conversation, status=status, priority=priority, labels=labels, depends_on=depends_on)
    try:
        with (folder / PLAN_NAME).open('x', encoding='utf-8', newline='\n') as plan:
            plan.write(text)
    except FileExistsError:
        pass

def queue_plan(folder: Path) -> None:
    """Queue FOLDER's existing plan: active and unclaimed becomes queued, queued stays; anything else is refused."""
    shape = plan_file_problem(folder / PLAN_NAME)
    if shape:
        fail(f'task {folder.name}: {shape}')
    status = read_plan(folder / PLAN_NAME).status
    if status == Status.QUEUED.key:
        return
    if is_claimed(folder):
        fail(f'task {folder.name} is claimed by an agent; it is queued again only once that claim has lapsed')
    if status != Status.ACTIVE.key:
        fail(f"task {folder.name} is {status or 'without a status'}; only an active task is queued")
    set_status(folder / PLAN_NAME, Status.QUEUED.key)
