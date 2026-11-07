#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/memar_git/services/show.py — a task's plan and report from the records branch.

Tasks live on `RECORDS_BRANCH`. Materialization under temp/task-store is
ephemeral; this verb reads the branch (hydrating when a Path reader needs it).
A file is named by its path from the task's folder; the project is told by
`--project` or `--project-path`, never the folder this runs in.
"""
from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
import argparse
import sys
from pathlib import Path, PurePosixPath
from typing import Callable
from machine.console import fail
from . import branch as task_branch
from modules.computer.software.services.project_find import add_project_flags, project_from_args
from .branch import folder_on_branch, reference
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
Reader = _m_dependency.Reader
_m_depends = import_module('modules-plugable.management.task.services.depends')
concerns_for = _m_depends.concerns_for
home_of = _m_depends.home_of
notes_for = _m_depends.notes_for
_m_list = import_module('modules-plugable.management.task.services.list')
find_tasks = _m_list.find_tasks
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
read_task = _m_folder.read_task
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
has_task = _m_task_files.has_task
plan_path = _m_task_files.plan_path
report_path = _m_task_files.report_path
read_plan = _m_plan_file.read_plan
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
decisions_needed = _m_report_file.decisions_needed
handback_problem = _m_report_file.handback_problem
from modules.computer.software.primitive.project_name import ProjectName
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
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
    """The files the task has on the records branch."""
    found = sorted(task_branch.held(project_path, task_id))
    if found:
        return found
    fail(f'no task {task_id}: {RECORDS_BRANCH} of {project_path} holds nothing for it')
    return []

def _kind_label(name: str) -> str | None:
    """NAME as a content kind word: plan or report (legacy filename spellings still accepted)."""
    lower = name.strip().lower()
    if lower in ('plan', PLAN_NAME, 'plan.md'):
        return 'plan'
    if lower in ('report', REPORT_NAME, 'report.md'):
        return 'report'
    return None

def _content_number(name: str) -> str | None:
    stem = Path(name).stem
    if stem.startswith('content.'):
        digits = stem[len('content.'):]
        if digits.isdigit():
            return str(int(digits))
    return None

def _read_kind(folder: Path, task_id: str, project_path: Path, kind: str) -> tuple[str, bytes] | None:
    """Latest content of KIND as (agent-facing label, bytes); label is the kind word, content number optional."""
    path = plan_path(folder) if kind == 'plan' else report_path(folder)
    name = Path(getattr(path, 'name', path)).name
    held = _read_blob(folder, task_id, project_path, name)
    if held is None and name not in (PLAN_NAME, REPORT_NAME):
        held = _read_blob(folder, task_id, project_path, PLAN_NAME if kind == 'plan' else REPORT_NAME)
    if held is None:
        return None
    _source, data = held
    number = _content_number(name)
    label = f'{kind} (content {number})' if number is not None else kind
    return (label, data)

def _read_blob(folder: Path, task_id: str, project_path: Path, name: str) -> tuple[str, bytes] | None:
    local = folder / name
    if folder.is_dir() and local.is_file():
        return (str(local), local.read_bytes())
    data = task_branch.read(project_path, task_id, name)
    if data is not None:
        return (f'{reference(task_id)}{name}', data)
    return None

def show(task_id: str, project_path: Path, files: list[str]) -> None:
    """Print the latest plan and report by kind when FILES is empty, else each named file or kind word."""
    folder = folder_of(task_id)
    if not files:
        printed = 0
        for kind in ('plan', 'report'):
            held = _read_kind(folder, task_id, project_path, kind)
            if held is None:
                continue
            label, data = held
            try:
                text = data.decode('utf-8-sig')
            except UnicodeDecodeError:
                fail(f'{label} of task {task_id} is not text, so it is not printed')
            sys.stdout.write(f'=== {label} ===\n{text}')
            if not text.endswith('\n'):
                sys.stdout.write('\n')
            sys.stdout.write('\n')
            printed += 1
        if printed == 0:
            fail(f'no plan or report content for task {task_id} on {RECORDS_BRANCH} of {project_path}; `show --list` names what it has')
        if has_task(folder) or has_task(task_id):
            dependency_lines(read_task(task_id), project_path)
        return
    for raw in files:
        kind = _kind_label(raw)
        if kind is not None:
            held = _read_kind(folder, task_id, project_path, kind)
            if held is None:
                fail(f'no {kind} content for task {task_id} on {RECORDS_BRANCH} of {project_path}; `show --list` names what it has')
            label, data = held
            header = f'=== {label} ==='
        else:
            name = _relative(raw)
            blob = _read_blob(folder, task_id, project_path, name)
            if blob is None:
                where = f'in {folder}, and ' if folder.is_dir() else ''
                fail(f'{name} of task {task_id} is not {where}on the branch {RECORDS_BRANCH} of {project_path} ({folder_on_branch(task_id)}/{name}); `show --list` names the files it has')
            source, data = blob
            header = f'=== {name} ({source})'
        try:
            text = data.decode('utf-8-sig')
        except UnicodeDecodeError:
            fail(f'{raw} of task {task_id} is not text, so it is not printed')
        sys.stdout.write(f'{header}\n{text}')
        if not text.endswith('\n'):
            sys.stdout.write('\n')
        sys.stdout.write('\n')

def dependency_lines(task, project_path: Path) -> None:
    """Print, under the plan, where each of TASK's dependencies stands and which tasks depend on it (derived, from Memar's tasks and the project's); nothing when neither."""
    reader = Reader(home_of(task) or project_path)
    everyone = {each.id: each for each in [*find_tasks(), *find_tasks(project=project_path)]}
    lines = [*notes_for(task, reader, everyone.values()), *(f'concerns: {each}' for each in concerns_for(task, reader))]
    if lines:
        sys.stdout.write('=== dependencies\n' + '\n'.join(lines) + '\n\n')

def hand_back(task_id: str) -> None:
    """Print TASK_ID's hand-back: Status, timeline place, and Decisions needed — never a content filename."""
    folder = folder_of(task_id)
    task = read_task(folder) if folder.is_dir() else read_task(task_id)
    if not task.has_plan:
        fail(f'no task {task_id} on {RECORDS_BRANCH}')
    lines = [f"Status: {task.status or '(none)'}", f'Report: {RECORDS_BRANCH}:{folder_on_branch(task_id)}/ (timeline)']
    problem = handback_problem(folder, task.status)
    if problem:
        lines.append(f'Not a hand-back: {problem}')
    else:
        lines.extend(decisions_needed(folder))
    sys.stdout.write('\n'.join(lines) + '\n')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar git show-task-records`."""
    shower = verbs.add_parser(SHOW_COMMAND, help="print a task's latest plan and report by kind, or named files, from the records branch", description=f"Print the latest **plan** and **report** contents of TASK_ID (found by kind on its\ntimeline, not by a filename), or the files named with --file, each under a line\nsaying where it came from. Prefer no --file: agents read plan and report as kinds.\n`--file plan` or `--file report` select by kind; a rare blob may still be named as a\npath under the task's tree. Material is read from the branch {RECORDS_BRANCH} of the\nproject (required). --list prints the raw tree names for debugging, not for ordinary\nagent work.\n\nA task that waits on another resumes when the owner says a task it waits for is done, or when\nevery task its Depends_on cites is Complete. It reads the hand-back alone (--hand-back),\nand no more of the report unless a step names a part; a task not Complete, or one holding\ndecisions, has its decisions answered as `memar ai get-task-questions-answer-brief` says, and what that leaves goes to the owner, before the plan goes on. The decisions made are consumed, not\nargued again, unless the chat's own work meets a problem with one. A report is a claim: read the passages it cites, at the cited lines, before\nbuilding on it.")
    TaskId.add_flag(shower, 'the task whose records to print', required=True)
    shower.add_argument('--file', action='append', default=[], metavar='PATH', help='optional: `plan` or `report` (by kind), or a rare path under the task tree; without it, latest plan and report')
    shower.add_argument('--list', action='store_true', help='print the names of the files the task has, one a line, instead of their text')
    shower.add_argument('--hand-back', action='store_true', help="print only the task's hand-back: Status, timeline place, and Decisions needed lines — never a content filename")
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
