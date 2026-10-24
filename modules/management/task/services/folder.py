#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/folder.py — one task's folder as the other services read it.

Finding, sweeping, and linking tasks all start from the same question — which
folders are tasks, what their plan says, and how long nothing in them has
changed — and each answer is given here once, so a task listed as active is
the task the sweep keeps.

Where the folders are is not decided here: `modules-plugable/computer/filesystem/services/fs_memar.py` owns every
Memar path, the task folder among them. Only the task root's folders are
Memar's; a folder directly in temp/ is not read as a task.
A folder in a
project's own task location (`task_location`) is continued, linked to,
and closed like any other, and listed when the caller asks for its project or
its conversation, but it is never among the folders the sweep is given: it is
the project's, not Memar's. That location is a folder
the project chose and may hold the project's own folders too, so a folder
there is a task only by the same test
(`is_task_folder`), and no other folder there is ever written into or
closed.

Idle is the latest change anywhere inside a folder, because on Windows a
folder's own time does not move when a nested file is edited. Reading changes
no modification time, so a folder that is only read still counts as idle.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
task_dir = _m_fs_memar.task_dir
tasks_root = _m_fs_memar.tasks_root
import os
import time
from pathlib import Path
from typing import NamedTuple
from modules.management.task.primitive.task_id import TaskId
from modules.process.project.services.task_location import registered_locations
from modules.management.task.services.plan_file import PLAN_NAME, plan_file_problem, read_plan
from modules.management.task.plan.primitive.plan_key import PlanKey
from modules.management.task.report.primitive.report_key import ReportKey
from modules.management.task.services.report_file import REPORT_NAME, read_report_status
from modules.knowledge.status.primitive.status import Status
DAY_SECONDS = 24 * 60 * 60

class Task(NamedTuple):
    """One task folder: its path, whether it has a plan, and what the plan says."""
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
        """The first task of this one's conversation: recorded, else this task itself."""
        return (self.front or {}).get(PlanKey.CONVERSATION.key, '') or self.id

def read_task(folder: Path) -> Task:
    plan = folder / PLAN_NAME
    if not plan.is_file():
        return Task(folder, False, None, '')
    try:
        read = read_plan(plan)
    except (OSError, UnicodeDecodeError):
        return Task(folder, True, None, '', readable=False)
    return Task(folder, True, read.front, read.status, shape=plan_file_problem(plan))

def queued_why(task: Task) -> str | None:
    """Why TASK is still queued: its plan's or its report's Status is Queued; None when neither is.

    A queued task is waiting to be taken up, and nothing that moves or
    removes a folder acts on one: its folder is the task.
    """
    queued = Status.QUEUED.key
    if task.status == queued:
        return f"its {PLAN_NAME}'s {PlanKey.STATUS.written} is {Status.QUEUED.word}"
    if read_report_status(task.path) == queued:
        return f"its {REPORT_NAME}'s {ReportKey.STATUS.written} is {Status.QUEUED.word}"
    return None

def is_task_folder(entry: Path) -> bool:
    """Whether ENTRY, a folder found by name outside the task root, is a task's.

    A name `task_id` mints, or a folder holding a plan.md that `ensure` wrote,
    with its title and the time it was opened, because `--task-id` lets a
    person name a task anything — and a folder named in a form minted
    before is a task by that plan as long as it keeps that name. Any other folder
    where a task could be — temp/'s own, or a project's beside its task
    folders — is not one, and no task verb writes into it or closes it.
    """
    if entry.is_symlink() or not entry.is_dir():
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
    """Whatever is named TASK_ID in ALSO or in a registered project location, folder or not."""
    locations = ([also] if also is not None else []) + registered_locations()
    return [entry for entry in (location / task_id for location in locations) if entry.exists() or entry.is_symlink()]

def project_folder_of(task_id: str, also: Path | None=None) -> Path | None:
    """TASK_ID's task folder in ALSO or in a registered project location, or None when it is in none."""
    return next((entry for entry in _project_entries(task_id, also) if is_task_folder(entry)), None)

def foreign_project_entry(task_id: str, also: Path | None=None) -> Path | None:
    """What is named TASK_ID in ALSO or a registered project location and is not a task folder, or None."""
    return next((entry for entry in _project_entries(task_id, also) if not is_task_folder(entry)), None)

def folder_of(task_id: str) -> Path:
    """TASK_ID's folder: under the task root, else in a registered project location.

    The first when none is there. The id is checked by `task_dir`, so a
    path is refused before a location is looked at.
    """
    folder = task_dir(task_id)
    if folder.is_dir():
        return folder
    return project_folder_of(task_id) or folder

def _entries(root: Path) -> list[Path]:
    try:
        return list(root.iterdir())
    except OSError:
        return []

def task_folders(*, projects: bool=False, locations: list[Path] | None=None) -> list[Path]:
    """Every task folder under the task root, newest first.

    With PROJECTS, the task folders in every registered project location
    too, and with LOCATIONS, those in each of these; the sweep asks with
    neither, because those are not Memar's to sweep. In every location a
    folder is a task by `is_task_folder`, since anyone may name a
    task anything with `--task-id`, and a folder named in a form minted
    before stays a task by its plan as long as it keeps that name.
    A name sort of the minted form is creation order; any other name follows
    every minted one.
    """
    folders = [entry for entry in _entries(tasks_root()) if is_task_folder(entry)]
    roots: list[Path] = []
    for root in [*(registered_locations() if projects else []), *(locations or [])]:
        if root.resolve() not in roots:
            roots.append(root.resolve())
    folders += [entry for root in roots for entry in _entries(root) if is_task_folder(entry)]
    folders.sort(key=lambda entry: (TaskId.is_form(entry.name), entry.name), reverse=True)
    return folders

def last_change(path: Path) -> float:
    """The latest modification time of PATH or of anything inside it."""
    latest = path.stat().st_mtime
    for root, folders, files in os.walk(path):
        for name in (*folders, *files):
            try:
                changed = os.stat(os.path.join(root, name), follow_symlinks=False).st_mtime
            except OSError:
                continue
            latest = max(latest, changed)
    return latest

def measured_idle(path: Path) -> float | None:
    """Days since anything inside PATH changed, or None when that cannot be read."""
    try:
        return (time.time() - last_change(path)) / DAY_SECONDS
    except OSError:
        return None
