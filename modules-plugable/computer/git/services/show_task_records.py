#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/show.py — a task's plan and report, or the files an agent asks for, wherever they are.

A task's folder is scratch and goes once its task is done; its records stay
on its project's records branch (`task_archive`). A reader who has a task
id from a changelog, a handoff or a report wants what the task said, not to
know which of the two places holds it today, so one command returns it (owner,
2026-10-15): the folder in the main repository's temp first, because while the
folder exists it is the task's latest state, then the branch. Each file is
looked for in that order on its own, and each is printed under a line naming
where it came from, so a reader of a folder that has moved on past what was
archived sees which is which.

A file is named by its path from the task's folder, never by one that
leaves it; the branch is read with git's read-only commands, in the project
told by `--project` or `--project-path`, never the folder this runs in.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
import argparse
import sys
from pathlib import Path, PurePosixPath
from typing import Callable
from machine.console import fail
from . import branch as task_branch
from modules.process.project.services.find import add_project_flags, project_from_args
from .branch import folder_on_branch, reference
from modules.management.task.services.dependency import Reader
from modules.management.task.services.depends import concerns_for, home_of, notes_for
from modules.management.task.services.list import find_tasks
from modules.management.task.services.folder import folder_of, read_task
from modules.management.task.services.plan_file import PLAN_NAME, read_plan
from modules.management.task.services.report_file import REPORT_NAME, decisions_needed, handback_problem, read_report_status
from modules.process.project.primitive.project_name import ProjectName
from modules.management.task.primitive.task_id import TaskId
SHOW_COMMAND = 'show-task-records'
PROJECT_REQUIRED = f"name the project the task belongs to with {ProjectName.either_words()}: the branch is the project's"

def _relative(path: str) -> str:
    """PATH as a plain relative path from the task's folder, refused when it could leave it."""
    posix = path.replace('\\', '/')
    parts = PurePosixPath(posix).parts
    if not path or posix.startswith('/') or ':' in posix or any((part in ('..', '.') for part in parts)):
        fail(f"{path!r} is not a path inside the task's folder; name it from the folder, like docs/note.md")
    return PurePosixPath(posix).as_posix()

def listing(task_id: str, project_path: Path) -> list[str]:
    """The files the task has: those in its folder when it is in temp, else those the branch holds for it."""
    folder = folder_of(task_id)
    if folder.is_dir():
        return sorted((each.relative_to(folder).as_posix() for each in folder.rglob('*') if each.is_file() and (not each.is_symlink())))
    found = sorted(task_branch.held(project_path, task_id))
    if not found:
        fail(f'no task {task_id}: not in temp, and {RECORDS_BRANCH} of {project_path} holds nothing for it')
    return found

def show(task_id: str, project_path: Path, files: list[str]) -> None:
    """Print each of FILES (the plan and the report when none) of TASK_ID, its folder first and then the branch."""
    folder = folder_of(task_id)
    names = [_relative(each) for each in files] or [PLAN_NAME, REPORT_NAME]
    printed = 0
    for name in names:
        local = folder / name
        if folder.is_dir() and local.is_file():
            source, data = (str(local), local.read_bytes())
        else:
            data = task_branch.read(project_path, task_id, name)
            source = f'{reference(task_id)}{name}'
        if data is None:
            where = f'in {folder}, and ' if folder.is_dir() else ''
            fail(f'{name} of task {task_id} is not {where}on the branch {RECORDS_BRANCH} of {project_path} ({folder_on_branch(task_id)}/{name}); `show --list` names the files it has')
        try:
            text = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            fail(f'{name} of task {task_id} is not text, so it is not printed')
        sys.stdout.write(f'=== {name} ({source})\n{text}')
        if not text.endswith('\n'):
            sys.stdout.write('\n')
        sys.stdout.write('\n')
        printed += 1
    if not files and (folder / PLAN_NAME).is_file():
        dependency_lines(read_task(folder), project_path)

def dependency_lines(task, project_path: Path) -> None:
    """Print, under the plan, where each of TASK's dependencies stands and which tasks depend on it (derived, from Memar's tasks and the project's); nothing when neither."""
    reader = Reader(home_of(task) or project_path)
    everyone = {each.id: each for each in [*find_tasks(), *find_tasks(project=project_path)]}
    lines = [*notes_for(task, reader, everyone.values()), *(f'concerns: {each}' for each in concerns_for(task, reader))]
    if lines:
        sys.stdout.write('=== dependencies\n' + '\n'.join(lines) + '\n\n')

def hand_back(task_id: str) -> None:
    """Print TASK_ID's hand-back alone: its Status, its report's path, and its `Decisions needed` lines; none of the rest of the report.

    Read from the task's folder, where a task that has just ended is; a
    report that is not a hand-back is named, with why, after what it does hold.
    """
    folder = folder_of(task_id)
    if not folder.is_dir():
        fail(f'task {task_id} has no folder in temp, so there is no hand-back to read; `show --file {REPORT_NAME}` reads it from the branch')
    plan_status = read_plan(folder / PLAN_NAME).status
    lines = [f"Status: {read_report_status(folder) or '(none)'}", f'Report: {folder / REPORT_NAME}', *decisions_needed(folder)]
    problem = handback_problem(folder, plan_status)
    if problem:
        lines.append(f'Not a hand-back: {problem}')
    sys.stdout.write('\n'.join(lines) + '\n')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar git show-task-records`."""
    shower = verbs.add_parser(SHOW_COMMAND, help="print a task's plan and report, or files of it, from its folder or the records branch", description=f"Print the {PLAN_NAME} and the {REPORT_NAME} of the task TASK_ID, or the files named with\n--file, each under a line saying where it came from. A file is read from the\ntask's folder in the main repository's temp when it is there, and then from\nthe branch {RECORDS_BRANCH} of the project, where `archive-task-records` kept it. Use it for a task\nid a changelog, a handoff or a report cites: it needs no knowledge of which\nplace holds the task today. A file is named by its path from the\ntask's folder, like docs/note.md; --list prints the files the task has\ninstead. The project's branch is read, never the folder this runs in.\n\nA task that waits on another resumes when the owner says a task it waits for is done, or when\nevery task its Depends_on cites is Complete. It reads the hand-back alone (--hand-back),\nand no more of the report unless a step names a part; a task not Complete, or one holding\ndecisions, has its decisions answered as `memar ai get-task-questions-answer-brief` says, and what that leaves goes to the owner, before the plan goes on. The decisions made are consumed, not\nargued again, unless the chat's own work meets a problem with one. A report is a claim: read the passages it cites, at the cited lines, before\nbuilding on it, and keep it in the task folder for the debrief.")
    TaskId.add_flag(shower, 'the task whose records to print', required=True)
    shower.add_argument('--file', action='append', default=[], metavar='PATH', help=f"a file of the task, by its path from the task's folder; may be repeated; without it, {PLAN_NAME} and {REPORT_NAME}")
    shower.add_argument('--list', action='store_true', help='print the names of the files the task has, one a line, instead of their text')
    shower.add_argument('--hand-back', action='store_true', help="print only the task's hand-back: the report's Status, its path and its Decisions needed lines, and why it is not one when it is not")
    add_project_flags(shower, 'the project the task belongs to', required=True)
    return run

def run(args: argparse.Namespace) -> None:
    project = project_from_args(args)
    if project is None:
        fail(PROJECT_REQUIRED)
    if args.hand_back:
        hand_back(args.task_id)
        return
    if args.list:
        for name in listing(args.task_id, project):
            sys.stdout.write(f'{name}\n')
        return
    show(args.task_id, project, args.file)
