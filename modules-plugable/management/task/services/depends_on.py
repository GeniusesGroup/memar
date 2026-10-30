#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/depends_on.py — the verb `memar task depends-on`: a task's dependencies shown, added and dropped.

What a dependency is and when it is met is `modules-plugable/management/task/services/dependency.py`'s; the
key is written by `task_plan_depends`; what it does to a task's Status
is `task_depends`'s. This file is the verb's face over them: it checks what
is added, writes the key, brings the Status up to date and says what is.
"""
from __future__ import annotations
from importlib import import_module
import argparse
from typing import Callable
from machine.console import fail, note
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DEPENDS_FOR = _m_dependency.DEPENDS_FOR
DependsOn = _m_dependency.DependsOn
Reader = _m_dependency.Reader
Ref = _m_dependency.Ref
refused_for_writing = _m_dependency.refused_for_writing
_m_depends = import_module('modules-plugable.management.task.services.depends')
DEPENDS_COMMAND = _m_depends.DEPENDS_COMMAND
concerns_for = _m_depends.concerns_for
home_of = _m_depends.home_of
notes_for = _m_depends.notes_for
problems = _m_depends.problems
reconcile = _m_depends.reconcile
_m_list = import_module('modules-plugable.management.task.services.list')
find_tasks = _m_list.find_tasks
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
is_task_folder = _m_folder.is_task_folder
read_task = _m_folder.read_task
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_plan_depends = import_module('modules-plugable.management.task.services.plan_depends')
set_depends_on = _m_plan_depends.set_depends_on
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
from modules.knowledge.status.primitive.status import Status
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId

def change(task_id: str, add: list[str], drop: list[str]) -> None:
    """`depends-on`: add and drop references in TASK_ID's key, checked, then bring its Status up to date and say what is."""
    folder = folder_of(task_id)
    plan = folder / PLAN_NAME
    if not is_task_folder(folder) or not plan.is_file():
        fail(f'no task {task_id} with a {PLAN_NAME}, so there is no {PlanKey.DEPENDS_ON.written} to set')
    task = read_task(folder)
    was = DependsOn.of(task.front)
    reader = Reader(home_of(task))
    if add or drop:
        dropped = [Ref.parse(word) for word in drop]
        missing = [str(ref) for ref in dropped if ref not in was]
        if missing:
            fail(f"{', '.join(missing)} is not in {task_id}'s {PlanKey.DEPENDS_ON.written} ({was.text() or 'none'}), so it is not dropped")
        added = DependsOn.normalized((Ref.parse(word) for word in add))
        now = DependsOn.normalized([*(ref for ref in was if ref not in dropped), *added])
        refused_for_writing(task_id, now, reader, added)
        set_depends_on(plan, now)
        task = read_task(folder)
        reconcile(task, reader)
        task = read_task(folder)
        print(f"{task_id}  {PlanKey.DEPENDS_ON.written}: {now.text() or '(none)'}, was {was.text() or '(none)'}")
    else:
        print(f"{task_id}  {PlanKey.DEPENDS_ON.written}: {was.text() or '(none)'}")
        reconcile(task, reader)
        task = read_task(folder)
    note(f'status: {task.status}')
    for line in notes_for(task, reader, find_tasks(project=home_of(task))):
        note(line)
    for line in concerns_for(task, reader):
        note(f'concerns: {line}')
    if task.status == Status.ACTIVE.key and problems(task, reader):
        note('it is Active, so its Status is not changed; set it Blocked if it cannot go on until they are Complete')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task depends-on`."""
    key = PlanKey.DEPENDS_ON.written
    changer = verbs.add_parser(DEPENDS_COMMAND, help='show, add or drop the tasks a task cannot start without', description=f"A task's {key} names the tasks that must be Complete (their plan and their report both)\nbefore it can start: it cannot be claimed or started until they are, and while one is not, its\nStatus is Blocked, with the unmet ids as the reason. Each is an id, or project/id for a task\nof another project, the project resolved as `memar project find` resolves a name. Without --add\nand --drop this shows the key, where each stands, and the tasks that depend on this one\n({DEPENDS_FOR}, derived, never written). --add is refused for the task itself, an id or a\nproject that does not resolve, and a cycle of any length; --drop is how a dependency that no\nlonger exists is removed. A queued task with an unmet dependency becomes Blocked; one whose\ndependencies are all met after Memar blocked it becomes queued again; an Active task is\nnot changed. Why a task waits goes in its plan's Next, and whoever makes its own task\nwait tells the owner at once that the work waits. Anyone may change it. ({key} means\nwhat the documents' Depends_on means, stronger in time: it cannot start until the cited task is Complete.)")
    TaskId.add_positional(changer, 'the task whose dependencies to show or change')
    changer.add_argument('--add', action='append', default=[], metavar='REF', help='a task to depend on, ID or project/ID; may be repeated')
    changer.add_argument('--drop', action='append', default=[], metavar='REF', help='a dependency to remove, as it is written in the key; may be repeated')
    return run

def run(args: argparse.Namespace) -> None:
    change(args.task_id, args.add, args.drop)
