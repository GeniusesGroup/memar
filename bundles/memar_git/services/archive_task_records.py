#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
RECORDS_RELATIVE = _m_memar_location.RECORDS_RELATIVE
scratch_root = _m_memar_location.scratch_root
import argparse
import os
import tempfile
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, NamedTuple
from machine.console import fail, note
from . import branch as task_branch
from modules.computer.software.edges.manifest.services.preferences import RECORDS_KEY, Records, preferences_path, read_preferences, records_preference
from modules.computer.software.services.project_registry import read_entries
from modules.computer.software.services.project_find import project_by_name
from .branch import RecordRefused, folder_on_branch, reference
_m_folder = import_module('modules-plugable.management.task.services.folder')
Task = _m_folder.Task
folder_of = _m_folder.folder_of
read_task = _m_folder.read_task
task_folders = _m_folder.task_folders
from .keep import KEEP_LIMIT_BYTES, Left, Selection, select
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
same_path = _m_task_location.same_path
from .log import record
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
TASK_FACTS_NAME = _m_task_files.TASK_FACTS_NAME
facts_named_project = _m_task_files.facts_named_project
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_temp = import_module('modules-plugable.management.task.services.temp')
TEMP_FOLDER = _m_temp.TEMP_FOLDER
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
ARCHIVE_COMMAND = 'archive-task-records'

class Outcome(Enum):
    KEPT = 'kept'
    NOT_OWED = 'not owed'
    REFUSED = 'refused'

class Kept(NamedTuple):
    outcome: Outcome
    reference: str | None
    why: str = ''
    files: tuple[str, ...] = ()
    commit: str | None = None

class State(Enum):
    ARCHIVED = 'archived'
    WAITING = 'not archived'
    NOT_OWED = 'not owed'
    REFUSED = 'refused'

class Standing(NamedTuple):
    state: State
    why: str = ''

class Owed(NamedTuple):
    folder: Path
    project: Path
    name: str
    selection: Selection

def _project_of(task: Task) -> str:
    return (task.front or {}).get(PlanKey.PROJECT.key, '').strip()

def project_name(project: Path) -> str | None:
    entry = next((each for each in read_entries() if same_path(each.path, project)), None)
    return entry.names[0] if entry is not None and entry.names else None

def _named_plan(data: bytes, name: str) -> bytes:
    lines = data.decode('utf-8-sig').splitlines(keepends=True)
    key = f'{PlanKey.PROJECT.written}:'
    if lines and lines[0].strip() == '---':
        for index in range(1, len(lines)):
            line = lines[index]
            if line.strip() == '---':
                break
            if line.startswith(key):
                ending = line[len(line.rstrip('\r\n')):]
                lines[index] = f'{key} {name}{ending}'
                break
    return ''.join(lines).encode('utf-8')

def owed(folder: Path) -> Owed | Kept:
    task = read_task(folder)
    if not task.has_plan:
        return Kept(Outcome.NOT_OWED, None, 'it has no plan')
    if not task.readable or task.front is None:
        return Kept(Outcome.REFUSED, None, 'its task facts cannot be read, so its project is not known')
    named = _project_of(task)
    if not named:
        return Kept(Outcome.NOT_OWED, None, 'its task facts name no project to keep its records in')
    project = Path(named)
    if not project.is_dir():
        try:
            project = Path(project_by_name(named))
        except SystemExit:
            return Kept(Outcome.REFUSED, None, f'its project {named} is not a folder on this computer')
    if not project.is_dir():
        return Kept(Outcome.REFUSED, None, f'its project {named} is not a folder on this computer')
    preference = records_preference(project)
    if preference is None:
        return Kept(Outcome.REFUSED, None, f"`{RECORDS_KEY}: {read_preferences(project).get(RECORDS_KEY, '')}` in {preferences_path(project)} is none of {Records.listing()}, or empty")
    if preference is Records.OFF:
        return Kept(Outcome.NOT_OWED, None, f"its project's preferences say `{RECORDS_KEY}: {Records.OFF.value}`")
    name = project_name(project)
    if name is None:
        return Kept(Outcome.REFUSED, None, f'its project {project} has no registered name to write in the kept plan; give it one with `memar software add`')
    if not task_branch.is_repository(project):
        return Kept(Outcome.REFUSED, None, f"its project {project} is not the top folder of a git repository, and its records are kept on the branch {RECORDS_BRANCH} of the project's own repository")
    if task_branch.is_checked_out(project):
        return Kept(Outcome.REFUSED, None, f'the branch {RECORDS_BRANCH} is the branch checked out in {project}; the records branch is never worked on, so check out another')
    return Owed(folder, project, name, select(folder))

def _entries(owing: Owed, workdir: Path) -> dict[str, Path]:
    sid = owing.folder.name
    entries: dict[str, Path] = {}
    for relative in owing.selection.kept:
        source = owing.folder / relative
        if relative == TASK_FACTS_NAME:
            named = workdir / sid / TASK_FACTS_NAME
            named.parent.mkdir(parents=True, exist_ok=True)
            named.write_bytes(facts_named_project(source.read_bytes(), owing.name))
            source = named
        entries[f'{folder_on_branch(sid)}/{relative}'] = source
    return entries

def standing(folder: Path) -> Standing:
    judged = owed(folder)
    if isinstance(judged, Kept):
        return Standing(State.NOT_OWED if judged.outcome is Outcome.NOT_OWED else State.REFUSED, judged.why)
    with tempfile.TemporaryDirectory(dir=scratch_root(), prefix='archive-') as workdir:
        entries = _entries(judged, Path(workdir))
        sources = list(entries.values())
        ids = task_branch.blob_ids(judged.project, sources)
        have = task_branch.held(judged.project, folder.name)
        prefix = folder_on_branch(folder.name) + '/'
        same = all((have.get(target.removeprefix(prefix)) == blob for target, blob in zip(entries, ids)))
    return Standing(State.ARCHIVED if same else State.WAITING)

def _size(size: int) -> str:
    return f'{size} bytes'

def _left_line(left: Left) -> str:
    held = f'{left.files} files, ' if left.files != 1 else ''
    return f'  {left.path} ({held}{_size(left.size)}): {left.reason.sentence}'

def _message(group: list[Owed]) -> str:
    ids = ', '.join((each.folder.name for each in group))
    lines = [f"Record {('task' if len(group) == 1 else 'tasks')} {ids}", '']
    for each in group:
        if each.selection.left:
            lines.append(f'Left out of {each.folder.name}:')
            lines.extend((_left_line(left) for left in each.selection.left))
            lines.append('')
    lines.append(f'Kept whole except what is listed: files over {KEEP_LIMIT_BYTES // 1024} KB are left out unless they are documents.')
    return '\n'.join(lines) + '\n'

def keep_records(folders: Iterable[Path], *, write: bool=True) -> list[Kept]:
    folders = list(folders)
    outcomes: list[Kept | None] = [None] * len(folders)
    groups: dict[str, list[tuple[int, Owed]]] = {}
    for index, folder in enumerate(folders):
        judged = owed(folder)
        if isinstance(judged, Kept):
            outcomes[index] = judged
        else:
            groups.setdefault(os.path.normcase(str(judged.project.resolve())), []).append((index, judged))
    with tempfile.TemporaryDirectory(dir=scratch_root(), prefix='archive-') as workdir:
        for number, members in enumerate(groups.values()):
            project = members[0][1].project
            group = [owing for _, owing in members]
            if not write:
                for index, owing in members:
                    outcomes[index] = Kept(Outcome.KEPT, reference(owing.folder.name), files=owing.selection.kept)
                continue
            scratch = Path(workdir) / str(number)
            scratch.mkdir()
            entries: dict[str, Path] = {}
            for owing in group:
                entries.update(_entries(owing, scratch))
            try:
                tip = task_branch.record(project, entries, [folder_on_branch(owing.folder.name) for owing in group], _message(group), scratch)
            except RecordRefused as error:
                for index, owing in members:
                    outcomes[index] = Kept(Outcome.REFUSED, None, f'its records could not be written to {RECORDS_BRANCH} of {project} ({error})')
                continue
            for index, owing in members:
                outcomes[index] = Kept(Outcome.KEPT, reference(owing.folder.name), files=owing.selection.kept, commit=tip)
                record('recorded', owing.folder.name, reference(owing.folder.name), folder=owing.folder)
    return [each for each in outcomes if each is not None]

def related_tasks(folder: Path) -> list[Path]:
    children: dict[str, list[Path]] = {}
    store = import_module('bundles.memar_git.services.task_store')
    store.scan((TASK_FACTS_NAME,))
    try:
        for entry in task_folders(projects=True):
            parent = read_task(entry).parent
            if parent:
                children.setdefault(parent, []).append(entry)
    finally:
        store.forget_scan()
    found = [folder]
    for each in found:
        for child in children.get(each.name, []):
            if all((child.resolve() != known.resolve() for known in found)):
                found.append(child)
    return found

def archive(task_id: str) -> None:
    _m_task_store = import_module('bundles.memar_git.services.task_store')
    if not _m_task_store.on_branch(task_id):
        fail(f'no task {task_id} on {RECORDS_BRANCH}')
    note(f'on branch: {task_id}')
    note(f'records: {reference(task_id)}')
    note(f'commit: {_m_task_store.verify_tip()}')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    parser = verbs.add_parser(ARCHIVE_COMMAND, help="confirm a task is on its project's records branch", description=f'Confirm the task TASK_ID is on {RECORDS_BRANCH} at {RECORDS_RELATIVE.as_posix()}/<id>/.\nTasks are written to the branch by ensure and conversation post; this verb does not copy from a folder.')
    TaskId.add_flag(parser, 'the task whose work is being committed', required=True)
    return run

def run(args: argparse.Namespace) -> None:
    archive(args.task_id)
