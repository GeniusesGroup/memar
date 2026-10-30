#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/list.py — the task folders a caller asks for, listed.

A folder is found again by what its plan says — the id, the title, the project,
the status — because an id says only when a task opened, not what it is
about; `list` reads every plan to answer, and that is cheap next to a task
that starts over because it could not find the one it continues.

The tasks of one conversation are listed together. One task is one task,
so a conversation is several tasks, and a person going back to it asks for
all of them: the conversation's tasks sit next to each other, the group
placed where its newest task falls, newest first inside it. A conversation
is named by any task in it — the first one's id is what the others record,
and a task asked for by its own id is read for the conversation it records;
a first task that has been swept is still the name its conversation goes by.

What is listed by default is Memar's own tasks alone. A project that keeps
its tasks in its own location keeps them for itself, and a list of every
project's tasks mixed into Memar's answers no question one task asks.
`--project` asks for one project's tasks wherever they lie: every task
folder in its own locations (`task_location.locations_of`), and every
other one whose plan names that project, from whatever folder `list` is run
in. The project is always named, a folder or a name the registry resolves
(`memar project find`); the folder `list` is run in is never read. A conversation crosses projects, since a delegated task may be another
project's, so `--conversation` looks in every location Memar has recorded.

A task whose plan and report disagree is marked where its status is shown,
because the two are written by one agent at two moments, and the list is where
the next one looks: a report whose Status is blocked under a plan still marked
active, or a status the plan's vocabulary does not have, is a task that will
be misread — kept forever, or picked up as finished. What disagrees is
`task_report`'s answer.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Callable
from machine.console import fail, note
from modules.management.task.services.dependency import DEPENDS_FOR, Reader
from modules.management.task.services.concerns import concerns
from modules.management.task.services.depends import DEPENDS_COMMAND, concerns_for, notes_for, reconcile_all
from modules.management.task.services.folder import Task, folder_of, measured_idle, read_task, task_folders
from modules.process.project.services.find import add_project_flags, project_by_path, project_from_args
from modules.process.project.services.task_location import locations_of, project_root, same_path
from modules.management.task.services.plan_file import PLAN_NAME, status_word
from modules.management.task.plan.primitive.priority import Priority
from modules.management.task.services.plan_labels import labels_of
from modules.management.task.primitive.record import PLAN
from modules.knowledge.status.primitive.status import Status
from modules.management.task.services.report_file import REPORT_NAME, disagreement, read_report_status
from modules.process.project.primitive.project_name import ProjectName
from modules.management.task.plan.primitive.plan_key import PlanKey
LIST_COMMAND = 'list'
NO_PLAN = f'(no {PLAN_NAME})'
NO_FRONT_MATTER = f'({PLAN_NAME} has no front matter)'
UNREADABLE_PLAN = f'({PLAN_NAME} cannot be read)'
DISAGREES = 'disagrees:'
CONCERNS = 'concerns:'

def matches(task: Task, text: str) -> bool:
    """Whether TEXT is in the task's id, title, or project, in any case.

    The id counts because it is how a task is named when one is continued:
    a caller holding `20261009T` asks for the tasks it prefixes, not for a
    title it never saw.
    """
    front = task.front or {}
    fields = (task.id, front.get(PlanKey.TITLE.key, ''), front.get(PlanKey.PROJECT.key, ''))
    needle = text.casefold()
    return any((needle in field.casefold() for field in fields))

def has_status(task: Task, status: str) -> bool:
    """Whether TASK's plan is in STATUS, named in any case."""
    if not (task.has_plan and task.readable):
        return False
    return task.status == status_word(status)

def conversation_named_by(task_id: str) -> str:
    """The conversation TASK_ID belongs to: the one its plan records, else its own id."""
    folder = folder_of(task_id)
    if folder.is_dir():
        return read_task(folder).conversation
    return task_id

def grouped(tasks: list[Task]) -> list[Task]:
    """TASKS, newest first, with each conversation's tasks next to each other."""
    groups: dict[str, list[Task]] = {}
    for task in tasks:
        groups.setdefault(task.conversation, []).append(task)
    return [task for group in groups.values() for task in group]

def project_of(project: str | None) -> Path | None:
    """The project the folder PROJECT is, its git top-level, None when none was asked.

    The flags (`add_project_flags`) have already turned a name into a folder;
    what arrives here is a folder, and `project_by_path` refuses an empty value
    or one that is not a folder. The folder the process runs in is never read.
    """
    if project is None:
        return None
    return project_root(project_by_path(project))

def of_project(task: Task, project: Path, own: list[Path]) -> bool:
    """Whether TASK is PROJECT's: it lies in one of OWN, its locations, or its plan names PROJECT."""
    if any((same_path(task.path.parent, location) for location in own)):
        return True
    named = (task.front or {}).get(PlanKey.PROJECT.key, '').strip()
    return bool(named) and same_path(named, project)

def find_tasks(text: str | None=None, status: str | None=None, conversation: str | None=None, project: Path | None=None) -> list[Task]:
    """The tasks in scope, newest first and grouped by conversation, filtered by TEXT, STATUS, CONVERSATION, and PROJECT.

    The scope is Memar's own tasks, or every recorded location's too when a
    CONVERSATION or a PROJECT is asked for.
    """
    own = locations_of(project) if project is not None else []
    everywhere = conversation is not None or project is not None
    tasks = [read_task(folder) for folder in task_folders(projects=everywhere, locations=own)]
    if project is not None:
        tasks = [task for task in tasks if of_project(task, project, own)]
    if text:
        tasks = [task for task in tasks if matches(task, text)]
    if status is not None:
        tasks = [task for task in tasks if has_status(task, status)]
    if conversation is not None:
        wanted = conversation_named_by(conversation)
        tasks = [task for task in tasks if task.conversation == wanted]
    return grouped(tasks)

def print_task(task: Task, *, idle: float | None=None, reader: Reader | None=None, everyone: list[Task] | None=None) -> None:
    """One list line and its notes; IDLE when measured; with READER, the task's dependencies and who depends on it, among EVERYONE."""
    if not task.has_plan:
        print(f'{task.id}  {NO_PLAN}')
    elif not task.readable:
        print(f'{task.id}  {UNREADABLE_PLAN}')
    elif task.front is None:
        print(f'{task.id}  {NO_FRONT_MATTER}')
    else:
        print(f"{task.id}  {task.front.get('title', '')}")
        note(f"project: {task.front.get('project', '')}")
    if task.has_plan and task.readable:
        note(f"status: {task.status or 'none'}")
        note(f'priority: {Priority.of(task.front)}')
        if labels_of(task.front):
            note(f"labels: {', '.join((label.word for label in labels_of(task.front)))}")
        why = disagreement(task.status, read_report_status(task.path))
        if why:
            note(f'{DISAGREES} {why}')
        for concern in concerns(task):
            note(f'{CONCERNS} {concern}')
        if reader is not None:
            for line in notes_for(task, reader, everyone or []):
                note(line)
            for concern in concerns_for(task, reader):
                note(f'{CONCERNS} {concern}')
    if task.parent:
        note(f'parent: {task.parent}')
    if task.conversation != task.id:
        note(f'conversation: {task.conversation}')
    if idle is not None:
        note(f'idle: {idle:.1f} days')
    note(f'path: {task.path}')

def list_tasks(text: str | None=None, status: str | None=None, idle_days: float | None=None, conversation: str | None=None, project: str | None=None) -> None:
    """`list`: print the tasks asked for, or say that none matches; PROJECT empty is the current one."""
    if idle_days is not None and idle_days < 0:
        fail('--idle-days counts days waited; it cannot be negative')
    shown = 0
    # TODO(memory-port): this reads every task's plan twice (two calls of find_tasks); with the memory port (task 20261023-T074643Z-5420) read each record once per command, in one batch.
    everyone = find_tasks(None, None, conversation, project_of(project))
    reader = Reader(None)
    reconcile_all(everyone, reader)
    everyone = find_tasks(None, None, conversation, project_of(project))
    chosen = grouped([task for task in everyone if (not text or matches(task, text)) and (status is None or has_status(task, status))])
    for task in chosen:
        idle = measured_idle(task.path) if idle_days is not None else None
        if idle_days is not None and (idle is None or idle < idle_days):
            continue
        print_task(task, idle=idle, reader=reader, everyone=everyone)
        shown += 1
    if not shown:
        asked = text or status is not None or idle_days is not None or (conversation is not None) or (project is not None)
        note('no task folder matches' if asked else 'no task folder')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar task list`."""
    lister = verbs.add_parser(LIST_COMMAND, help="list task folders, newest first, a conversation's together", description=f"List Memar's own task folders, newest first, with the tasks of one conversation next\nto each other: id, title, project, status, priority, the task it came from, path. A folder\nwith no plan.md, one that cannot be read, or one without front matter is listed and marked so.\nA task whose {REPORT_NAME} Status disagrees with its plan's, or whose status is not\n{', '.join(Status.keys(PLAN.kind))}, is marked `{DISAGREES}`, with why; one not complete that looks\nfinished or abandoned is marked `{CONCERNS}`. A mark moves nothing. A task with a `{PlanKey.DEPENDS_ON.written}` shows\neach task it cites and where that stands, and a cited task shows who depends on it as `{DEPENDS_FOR}`;\nlisting also brings the Status of a task with dependencies up to date, as `claims` does\n(`memar task depends-on --help`). A plan or a report in an\nearlier shape is marked likewise. A folder in a project's own task location is listed only\nwhen asked for: {ProjectName.FLAG} lists every task of that project, --conversation every task\nlinked with that one; --status and --idle-days keep only what they name.")
    lister.add_argument('text', nargs='?', metavar='TEXT', help='show only tasks whose id, title, or project holds TEXT, in any case; one word or a short phrase, not a question to answer')
    lister.add_argument('--status', type=status_word, choices=Status.keys(PLAN.kind), default=None, help='show only tasks whose task has this status')
    lister.add_argument('--idle-days', type=float, default=None, metavar='DAYS', help='show only tasks in which nothing has changed for at least DAYS days, and say how long')
    lister.add_argument('--conversation', default=None, metavar='ID', help='show only the tasks of the conversation the task ID belongs to, wherever they lie')
    add_project_flags(lister, "show every task of the project: those in its own task location and those in Memar's whose plan names it; the calling folder is never read and one of the two is required to ask for a project")
    return run

def run(args: argparse.Namespace) -> None:
    list_tasks(args.text, args.status, args.idle_days, args.conversation, project_from_args(args))
