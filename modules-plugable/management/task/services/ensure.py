#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/ensure.py — one task's folder, plan and report ensured, wherever the project keeps its tasks.

What `ensure` and `get-task-init-context` both ask: the folder is found or made in the location the project names, its
plan is written or kept (`task_plan_write`), its report and its folders (`task_layout`) are made, and the id and
path come back. The verb's own help and what it prints are in `task_new`.

A task writes only inside its own folder: --task-id reuses an id only to continue the same
task, and two tasks writing one folder reintroduce the unattributed mixing task folders
exist to remove. The parent a new task names must be a task folder that is there, because its
conversation is read from it. Where exactly a folder is made is asked of the project the plan
names (`task_location`), and the day's sweep runs when one is opened (`task_gc`), never
touching the task being opened or continued.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
task_dir = _m_fs_memar.task_dir
from pathlib import Path
from machine.console import fail
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DependsOn = _m_dependency.DependsOn
Reader = _m_dependency.Reader
Ref = _m_dependency.Ref
refused_for_writing = _m_dependency.refused_for_writing
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
from modules.process.project.services.find import project_by_path
from modules.process.project.services.preferences import TASKS_KEY, preferences_path
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
project_folder_of = _m_folder.project_folder_of
read_task = _m_folder.read_task
_m_gc = plugable_load('computer.git.services.sweep_idle_task_folders')
reap_once_a_day = _m_gc.reap_once_a_day
_m_layout = import_module('modules-plugable.management.task.services.layout')
ensure_folders = _m_layout.ensure_folders
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
from modules.process.project.services.task_location import in_project_location, project_location, project_root, register
_m_log = plugable_load('computer.git.services.log')
record = _m_log.record
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
checked_title = _m_plan_file.checked_title
_m_depends = import_module('modules-plugable.management.task.services.depends')
BLOCKED_EVENT = _m_depends.BLOCKED_EVENT
reconcile = _m_depends.reconcile
_m_plan_depends = import_module('modules-plugable.management.task.services.plan_depends')
set_depends_on = _m_plan_depends.set_depends_on
_m_plan_labels = import_module('modules-plugable.management.task.services.plan_labels')
add_label = _m_plan_labels.add_label
checked_label = _m_plan_labels.checked_label
registry_for = _m_plan_labels.registry_for
_m_plan_priority = import_module('modules-plugable.management.task.services.plan_priority')
set_priority = _m_plan_priority.set_priority
_m_plan_write = import_module('modules-plugable.management.task.services.plan_write')
queue_plan = _m_plan_write.queue_plan
write_plan = _m_plan_write.write_plan
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
write_report = _m_report_file.write_report
from modules.knowledge.label.primitive.label import Labels
from modules.knowledge.status.primitive.status import Status
from modules.process.project.primitive.project_name import ProjectName
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
ENSURE_COMMAND = 'ensure'
PROJECT_REQUIRED = f'{ENSURE_COMMAND} needs {ProjectName.either_words()} to make a task folder: the project is always named, by a name `memar project find` resolves or by a folder, and the folder this runs in is never read; a task that is already there is continued without it'

def named_project(project: str | None) -> Path | None:
    """The project whose folder is PROJECT, its git top-level, or None when none was named.

    The flags (`add_project_flags`) have already turned a name into a folder;
    `project_by_path` refuses an empty value or one that is not a folder;
    nothing here reads the folder the process runs in.
    """
    if project is None:
        return None
    return project_root(project_by_path(project))

def recorded_project(folder: Path) -> Path | None:
    """The project FOLDER's plan records, when it names a folder that is there, else None."""
    named = ((read_task(folder).front or {}).get(PlanKey.PROJECT.key) or '').strip()
    if not named:
        return None
    where = Path(named)
    return where if where.is_dir() else None

def linked_conversation(task_id: str, parent: str) -> str:
    """The conversation a task opened from PARENT belongs to; PARENT must be a task folder."""
    if parent == task_id:
        fail('--parent names this task itself; name the task this task came from')
    folder = folder_of(parent)
    if not folder.is_dir():
        fail(f'no task folder {parent}: --parent names a task that is there, the one this task came from')
    return read_task(folder).conversation

def ensure_task(task_id: str | None=None, title: str | None=None, parent: str | None=None, queued: bool=False, priority: int | str | None=None, labels: list[str] | None=None, project: str | None=None, depends_on: list[str] | None=None) -> tuple[str, Path]:
    """Ensure the task's folder, its plan.md and report.md, and its folders exist; return its id and path.

    TITLE is required when the folder has no plan.md yet, and unused when it
    has one. PARENT links a new plan to the task it came from; a plan that
    is there keeps the link it was written with, and a different one is
    refused rather than ignored. A rerun with the same id is idempotent: the
    folder, its plan, and its report are kept as they are and the same id and
    path are reported again. A task an earlier Memar left in temp/ is
    continued where it is; no second folder is made for it. A task in a project's
    own location is continued there. A folder that is nowhere yet is made in
    the location the project's preferences set, else .agents/tasks/ inside the project (the Memar checkout's own is under Memar's root); a
    name already taken there by anything that is not a task folder is
    refused, and a location that cannot be made fails with a message. The
    first call of a day also reaps the task folders that have been idle past
    the limit, other than this one. QUEUED leaves a new plan queued, or queues
    an active one; PRIORITY, checked before anything is made, is written into a
    new plan or set on the one that is there; so are LABELS, each `KIND=WORD`
    checked against its kind before anything is made and added to the plan
    (several of one kind are kept, none is twice); a topic the project
    declares nowhere is refused, with the declaration to write and the
    declared topics near it (`checked_label`).

    PROJECT, a name or a folder, is required to make a folder, and an empty
    one is refused: the project is always named, and the folder the process
    runs in is never read. A folder that is there is continued without it, its
    project the one its plan records.

    DEPENDS_ON, references to tasks, are checked before anything is made
    (`depends_on.refused_for_writing`) and added to the plan's key; a new
    task with an unmet one is written Blocked, and an existing queued one
    becomes Blocked (`task_depends`).
    """
    priority = None if priority is None else Priority.checked(priority)
    cited = DependsOn.normalized((Ref.parse(word) for word in depends_on or []))
    sid = TaskId.new() if task_id is None else task_id
    folder = task_dir(sid)
    project = named_project(project)
    location = project_location(project) if project is not None else None
    if task_id is not None and (not folder.is_dir()):
        folder = project_folder_of(sid, also=location) or folder
    if project is None and folder.is_dir():
        project = recorded_project(folder)
        location = project_location(project) if project is not None else None
    if project is None and (not (folder.is_dir() and (folder / PLAN_NAME).is_file())):
        fail(PROJECT_REQUIRED)
    if not folder.is_dir() and location is not None:
        folder = location / sid
        if folder.exists() or folder.is_symlink():
            fail(f'{folder} is there and is not a task folder; `ensure` never writes into it. Pass --task-id a name not used in that location, or none to mint one')
    given = None
    if labels is not None:
        given, registry = (Labels(), registry_for(project))
        for text in labels:
            given = given.with_label(checked_label(text, project, registry))
    existed = folder.is_dir()
    has_plan = (folder / PLAN_NAME).is_file()
    title = checked_title(title, required=not has_plan)
    parent = (parent or '').strip() or None
    conversation = None
    if parent is not None:
        if has_plan:
            recorded = read_task(folder).parent
            if recorded != parent:
                fail(f"task {sid} was opened with parent {recorded or '(none)'}; a task's link is written once, with its plan")
        else:
            conversation = linked_conversation(sid, parent)
    reader = Reader(project)
    now = DependsOn.normalized([*(DependsOn.of(read_task(folder).front) if has_plan else ()), *cited])
    if cited:
        refused_for_writing(sid, now, reader, cited)
    path = folder
    if not existed:
        try:
            path.mkdir(parents=True, exist_ok=True)
        except OSError as error:
            where = f'; check `{TASKS_KEY}` in {preferences_path(project)}' if location is not None and project is not None else ''
            fail(f'the task folder {path} could not be made ({error.strerror or error}){where}')
        record('opened', sid, f'parent {parent}' if parent else '', folder=path)
    if in_project_location(path):
        register(path.parent, project)
    if not has_plan:
        waits = bool(cited) and bool(reader.unmet(cited))
        status = Status.BLOCKED.key if waits else Status.QUEUED.key if queued else Status.ACTIVE.key
        write_plan(path, sid, title, parent, conversation, project, status, priority, given, now.text() or None)
        if waits:
            record(BLOCKED_EVENT, sid, '; '.join(reader.unmet(cited)), folder=path)
    else:
        if queued:
            queue_plan(path)
        if priority is not None:
            set_priority(path / PLAN_NAME, priority)
        for label in given or ():
            add_label(path / PLAN_NAME, label)
        if cited:
            set_depends_on(path / PLAN_NAME, now)
            reconcile(read_task(path), reader)
    write_report(path, sid, (read_task(path).front or {}).get(PlanKey.TITLE.key))
    ensure_folders(path)
    reap_once_a_day(keep=sid)
    return (sid, path)
