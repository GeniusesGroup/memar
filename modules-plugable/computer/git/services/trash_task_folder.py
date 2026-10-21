#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/close.py — one session's folder moved to the OS trash, on its starter's word.

The sweep in `session_gc` is how folders normally go; `close` remains for the
case where the person who started the session has already said the work is
finished. The folder goes to the trash rather than being deleted, so a session
closed by mistake costs one trip to the trash, and a trash that fails leaves
the folder where it was: a failed recovery is not a successful close.

`close` keeps nothing itself. A folder whose records are
owed is closed only when they are already on its project's records branch as
the folder holds them now (`session_archive.standing`): the person who closes
has run `archive` for the task, and its commit is cited, so a close that
quietly wrote another one would be a record nobody saw made. A folder not yet
archived is not closed, and `--discard-records` does not change that. The flag
is for the folder whose records cannot be kept at all, a project that is gone
for good; closing it drops them, which only its starter may say. A project
that keeps no records, and a folder with no plan or no project, owe none.

A session waiting to be taken up is not closed either: while its plan's or its
report's Status is Queued its folder is the task itself.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
_m_fs_trash = import_module('modules-plugable.computer.filesystem.services.fs_trash')
soft_delete = _m_fs_trash.soft_delete
import argparse
from pathlib import Path
from typing import Callable, NamedTuple
from machine.console import fail, note
from modules.process.project.services.preferences import SESSIONS_KEY
from .archive_task_records import ARCHIVE_COMMAND, Kept, Outcome, State, standing
from .branch import reference
from modules.management.task.services.folder import folder_of, foreign_project_entry, queued_why, read_session
from .sweep_idle_task_folders import GC_COMMAND
from .log import record
CLOSE_COMMAND = 'trash-task-folder'
DISCARD_RECORDS_FLAG = '--discard-records'

class Closed(NamedTuple):
    """One close: the id, its folder, whether anything was moved to recoverable storage, and how its records stand."""
    id: str
    path: Path
    removed: bool
    kept: Kept | None = None

def close_session(task_id: str, *, discard_records: bool=False) -> Closed:
    """Trash one session's folder once its records are archived or not owed. Idempotent: a missing folder is already closed.

    The target is confined to the session folder by construction:
    task_dir refuses anything shaped like a path. A session an earlier
    Memar left in temp/ is closed where it is, and so is one
    in a project's own session location, on the same word of its starter; a
    folder of that name there that is not a session's is refused. A folder
    whose plan or report is Queued, or whose records are owed and not on the
    branch, is refused; one whose records cannot be kept is refused unless
    DISCARD_RECORDS.
    """
    path = folder_of(task_id)
    if not path.exists() and (not path.is_symlink()):
        foreign = foreign_project_entry(task_id)
        if foreign is not None:
            fail(f"{foreign} is not a session folder; `close` closes only a session's folder")
        return Closed(task_id, path, False)
    queued = queued_why(read_session(path))
    if queued is not None:
        fail(f'{task_id} was not closed: {queued}; a session waiting to be taken up is not closed')
    held = standing(path)
    if held.state is State.WAITING:
        fail(f'{task_id} was not closed: its records are owed and it is not archived on the branch {RECORDS_BRANCH}; run `memar git {ARCHIVE_COMMAND} --task-id {task_id}`, then close it')
    if held.state is State.REFUSED and (not discard_records):
        fail(f'{task_id} was not closed: its records cannot be kept, {held.why}; settle that, or close it and discard them with {DISCARD_RECORDS_FLAG}')
    if held.state is State.ARCHIVED:
        kept = Kept(Outcome.KEPT, reference(task_id))
    else:
        kept = Kept(Outcome.NOT_OWED if held.state is State.NOT_OWED else Outcome.REFUSED, None, held.why)
    soft_delete(path)
    record('closed', task_id, folder=path)
    return Closed(task_id, path, True, kept)

def close(task_id: str, discard_records: bool=False) -> None:
    """`close`: trash the folder once its records are archived, and say what was done."""
    closed = close_session(task_id, discard_records=discard_records)
    note(f"{('closed' if closed.removed else 'already closed')}: {closed.id}")
    note(f'path: {closed.path}')
    if closed.kept is None:
        return
    if closed.kept.outcome is Outcome.KEPT:
        note(f'records: {closed.kept.reference}')
    else:
        note(f'records not kept, {closed.kept.why}')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar git trash-task-folder`."""
    closer = verbs.add_parser(CLOSE_COMMAND, help='move a finished, archived task folder to the OS recycle bin / Trash', description=f'Move the task folder TASK_ID to the OS recycle bin / Trash, so a\nmistake costs one trip there; a folder already gone is already trashed.\nIt keeps nothing itself: a folder whose records are owed is trashed only\nwhen `memar git {ARCHIVE_COMMAND} --task-id ID` has put them, as the folder holds\nthem now, on the branch {RECORDS_BRANCH} of its project ({RECORDS_RELATIVE.as_posix()}/<id>/ there);\na folder not archived is not trashed, and {DISCARD_RECORDS_FLAG} does not change that.\nA folder whose plan or report Status is Queued is never trashed. A folder\nwhose records cannot be kept at all (its project is gone) is not trashed\nunless {DISCARD_RECORDS_FLAG} is given, which drops them.\nRun it only when the person who started the task has already said the\nwork is finished; never ask them to, and never trash a task you did not\nopen. You do not have to trash a task: once a day `new` sweeps the idle\nfolders whose status is complete (`{GC_COMMAND}` runs that sweep at once), and a\nproject that keeps its finished tasks (its preferences set `{SESSIONS_KEY}`)\ntrashes none.')
    closer.add_argument('--task-id', required=True, help='the task id to trash')
    closer.add_argument(DISCARD_RECORDS_FLAG, action='store_true', help="close it even though its records cannot be kept at all, which loses them; only on its starter's word")
    return run

def run(args: argparse.Namespace) -> None:
    close(args.task_id, args.discard_records)
