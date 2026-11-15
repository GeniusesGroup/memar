#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
RECORDS_RELATIVE = _m_memar_location.RECORDS_RELATIVE
_m_fs_trash = import_module('bundles.memar_adaptor.fs.services.fs_trash')
from pathlib import Path
from typing import NamedTuple
from machine.console import fail, note
from modules.computer.software.edges.manifest.services.preferences import TASKS_KEY
from .archive_task_records import ARCHIVE_COMMAND, Kept, Outcome, State, standing
from .branch import reference
_m_folder = import_module('modules-plugable.management.task.services.folder')
folder_of = _m_folder.folder_of
foreign_project_entry = _m_folder.foreign_project_entry
queued_why = _m_folder.queued_why
read_task = _m_folder.read_task
from .sweep_idle_task_folders import GC_COMMAND
from .log import record
CLOSE_COMMAND = 'trash-task-folder'
DISCARD_RECORDS_FLAG = '--discard-records'

class Closed(NamedTuple):
    id: str
    path: Path
    removed: bool
    kept: Kept | None = None

def close_task(task_id: str, *, discard_records: bool=False) -> Closed:
    path = folder_of(task_id)
    if not path.exists() and (not path.is_symlink()):
        foreign = foreign_project_entry(task_id)
        if foreign is not None:
            fail(f"{foreign} is not a task folder; `close` closes only a task's folder")
        return Closed(task_id, path, False)
    task = read_task(path)
    _m_things = import_module('modules-plugable.management.task.services.task_thing_services')
    queued = queued_why(task, _m_things.read_status_key(task.id, _m_things.project_for(task)))
    if queued is not None:
        fail(f'{task_id} was not closed: {queued}; a task waiting to be taken up is not closed')
    held = standing(path)
    if held.state is State.WAITING:
        fail(f'{task_id} was not closed: its records are owed and it is not archived on the branch {RECORDS_BRANCH}; run `memar git_{ARCHIVE_COMMAND.replace("-", "_")} --task-id {task_id}`, then close it')
    if held.state is State.REFUSED and (not discard_records):
        fail(f'{task_id} was not closed: its records cannot be kept, {held.why}; settle that, or close it and discard them with {DISCARD_RECORDS_FLAG}')
    if held.state is State.ARCHIVED:
        kept = Kept(Outcome.KEPT, reference(task_id))
    else:
        kept = Kept(Outcome.NOT_OWED if held.state is State.NOT_OWED else Outcome.REFUSED, None, held.why)
    _m_fs_trash.soft_delete(path)
    record('closed', task_id, folder=path)
    return Closed(task_id, path, True, kept)

def close(task_id: str, discard_records: bool=False) -> None:
    closed = close_task(task_id, discard_records=discard_records)
    note(f"{('closed' if closed.removed else 'already closed')}: {closed.id}")
    note(f'path: {closed.path}')
    if closed.kept is None:
        return
    if closed.kept.outcome is Outcome.KEPT:
        note(f'records: {closed.kept.reference}')
    else:
        note(f'records not kept, {closed.kept.why}')

def trash_task_folder(*, task_id: str, discard_records: bool = False) -> None:
    close(task_id, discard_records)

declare = import_module('modules.process.service.primitive.declaration').declare
DECLARATIONS = (
    declare(trash_task_folder, name=CLOSE_COMMAND, summary='move a finished, archived task folder to the OS recycle bin / Trash',
            description=f'Move the task folder TASK_ID to the OS recycle bin / Trash, so a\nmistake costs one trip there; a folder already gone is already trashed.\nIt keeps nothing itself: a folder whose records are owed is trashed only\nwhen `memar git_{ARCHIVE_COMMAND.replace("-", "_")} --task-id ID` has put them, as the folder holds\nthem now, on the branch {RECORDS_BRANCH} of its project ({RECORDS_RELATIVE.as_posix()}/<id>/ there);\na folder not archived is not trashed, and {DISCARD_RECORDS_FLAG} does not change that.\nA folder whose plan or report Status is Queued is never trashed. A folder\nwhose records cannot be kept at all (its project is gone) is not trashed\nunless {DISCARD_RECORDS_FLAG} is given, which drops them.\nRun it only when the person who started the task has already said the\nwork is finished; never ask them to, and never trash a task you did not\nopen. You do not have to trash a task: once a day `ensure` sweeps the idle\nfolders whose status is complete (`{GC_COMMAND}` runs that sweep at once), and a\nproject that keeps its finished tasks (its preferences set `{TASKS_KEY}`)\ntrashes none.',
            help={'task_id': 'the task id to trash', 'discard_records': "close it even though its records cannot be kept at all, which loses them; only on its starter's word"}),
)
