#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/gc.py — the sweep: idle finished task folders moved to the trash.

No task has to ask for its own close. No agent knows at a reliable moment
that the work is finished — the person may come back tomorrow, and a sub-agent
that has reported may be handed more — and a message spent asking is paid by
every task there is. So the sweep reaps instead: every task folder in
which nothing has changed for the idle limit and whose status is complete — a
folder holding no plan has nothing unfinished — is moved to the OS trash, where
it can be recovered, and the reap is recorded in the task log. Idle is not
the same as finished, so a task whose status is not complete is never swept:
carrying that task to the next task is what the folder is there for, and it
goes only when its status is complete or a person closes it. The test is complete,
not merely not active: a status is a vocabulary this file does not own — today
queued, active, blocked, complete, and another can be added tomorrow — and a status it does
not know, or none, is not complete, so such a folder is kept; so is one whose plan
cannot be read, since its status is not known either. What counts as complete is
`task_plan.is_complete`: the word complete and no other, so a plan in an
earlier shape is kept and named, with where today's shape is shown. The limit is
TASK_IDLE_DAYS below, a number in this file rather than a per-machine
setting: changing it is an edit reviewed like any other. Only folders named in
the form `task_id` mints are reaped, and never the one being opened or
continued. The limit is one day because a finished folder owes nothing to the
clock once its records are on the records branch, where they stay recoverable:
waiting a week only crowded the list of folders a person reads.

The sweep runs once a day, at the first `ensure` of the day. A person opens dozens
of tasks a day, and walking hundreds of folders on each of them is load for
nothing, since a folder idle for a week does not become more idle by the hour.
Whether today's sweep happened is read from a one-line marker holding its date,
not from the log: the log grows with every task, and reading it on each
`ensure` would bring back the cost the daily sweep removes. The guard is
`s_lock.claim_today`, which the daily update asks too. The same sweep keeps
the log from growing without end: lines older than LOG_KEEP_DAYS, four weeks, are moved into a dated file that goes to the trash, so an old record
leaves the log without being deleted for good. The caller of `ensure` is not told
what was reaped: it was not their task, and the log is where a person looks
for a folder that is gone.

Before a finished folder is moved, whatever of its records the project's
records branch does not hold is added (`task_archive`), so a task id a
commit cites still names something once the folder is gone. The sweep is the
one act that adds records on its own: `close` acts only
on a task `archive` has kept, but the clock has no one to run `archive`
first. All the folders one sweep moves are added in one commit for each
project. A folder whose records cannot be kept is not moved: the clock never
drops a record, and `gc` lists the folder with why. A task whose plan or
report Status is Queued is waiting to be taken up and is never swept.

A kept folder that looks finished or abandoned is flagged beside it
(`task_concerns`), and only flagged: the sweep deletes nothing it did not
before, because a plan can say it is finished and be wrong.

`gc` is the same sweep asked for by a person, not a second one: the daily guard
is a separate step in front of it, so `ensure` keeps its once-a-day cost and `gc`
sweeps whenever it is run, by the same rules, and logs the same way. Unlike
`ensure` it prints what it moved, because its caller asked, and it lists the idle
folders it kept for unfinished work with their age, because those are the ones
only a person can let go. It may be given a shorter limit, never one under
GC_MIN_IDLE_DAYS: at zero, a folder opened a moment ago would be judged by a
plan its task has not begun to keep.

The sweep reaches Memar's own scratch only. A task folder a project's
preferences placed in the project (`task_location`) is the project's to
keep, commit, or delete, so neither sweep is given it; `gc` names each such
location it passed over, so the person who asked knows the sweep did not
cover it. Its log, in that location, is the project's too, so only Memar's
own log is trimmed. `gc` also removes from Memar's record each location
whose folder is gone, and names it: a person running it is there to read
that, which the daily sweep's caller is not, so the daily sweep leaves the
record as it is.

**What the help leaves out.** A recorded project task location whose folder is gone is no
longer recorded, and each one is named; `ensure` records it again when it makes a task there.
The flags are the same `concerns` marks `list` prints (`task_concerns`).
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
tasks_root = _m_fs_memar.tasks_root
_m_fs_lock = import_module('modules-plugable.computer.memory.filesystem.services.fs_lock')
claim_today = _m_fs_lock.claim_today
_m_fs_trash = import_module('modules-plugable.computer.memory.filesystem.services.fs_trash')
import argparse
import contextlib
import io
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Callable, NamedTuple
from machine.console import fail, note
from .archive_task_records import Outcome, keep_records
_m_concerns = import_module('modules-plugable.management.task.services.concerns')
concerns = _m_concerns.concerns
_m_folder = import_module('modules-plugable.management.task.services.folder')
DAY_SECONDS = _m_folder.DAY_SECONDS
Task = _m_folder.Task
last_change = _m_folder.last_change
queued_why = _m_folder.queued_why
read_task = _m_folder.read_task
task_folders = _m_folder.task_folders
from modules.process.project.services.task_location import prune_registry, registered_locations
from .log import TASK_LOG_NAME, log_path, record
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
is_complete = _m_plan_file.is_complete
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
GC_COMMAND = 'sweep-idle-task-folders'
TASK_IDLE_DAYS = 1
GC_MIN_IDLE_DAYS = 1
LOG_KEEP_DAYS = 28
SWEPT_MARKER_NAME = 'tasks.swept'
CLOSE_HINT = 'memar git trash-task-folder --task-id ID'
NOT_SWEPT = "not swept, a project's own task location, which is the project's to keep or delete"
FORGOTTEN = 'no longer recorded, a project task location that is gone'
RECORDS_NOT_KEPT = 'its records cannot be kept'

class Sweep(NamedTuple):
    """What one sweep did with the folders idle past its limit, each with its idle days."""
    reaped: list[tuple[str, float]]
    kept: list[tuple[str, float, str]]
    stuck: list[tuple[str, float]]
    flagged: list[tuple[str, str]]

def unfinished(task: Task) -> str | None:
    """Why TASK's task is not known to be finished, or None when it is."""
    if not task.has_plan:
        return None
    if not task.readable:
        return f'its {PLAN_NAME} cannot be read'
    if task.shape:
        return task.shape
    if not is_complete(task.status):
        return f'its status is {task.status}' if task.status else 'it has no status'
    return queued_why(task)

def claim_todays_sweep() -> bool:
    """Whether this call is the first today, recording today's date if it is."""
    return claim_today(tasks_root() / SWEPT_MARKER_NAME)

def trim_log() -> None:
    """Move log lines older than LOG_KEEP_DAYS into a file sent to the trash.

    A line whose time cannot be read is kept: it is not known to be old.
    """
    log = log_path()
    try:
        lines = log.read_text(encoding='utf-8').splitlines(keepends=True)
    except OSError:
        return
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=LOG_KEEP_DAYS)
    kept: list[str] = []
    old: list[str] = []
    for line in lines:
        try:
            stamp = datetime.fromisoformat(line.split('\t', 1)[0])
        except ValueError:
            kept.append(line)
            continue
        (old if stamp < cutoff else kept).append(line)
    if not old:
        return
    aside = log.with_name(f'{TASK_LOG_NAME}.{now.date().isoformat()}')
    rewritten = log.with_name(f'{TASK_LOG_NAME}.new')
    try:
        aside.write_text(''.join(old), encoding='utf-8', newline='\n')
        rewritten.write_text(''.join(kept), encoding='utf-8', newline='\n')
        os.replace(rewritten, log)
    except OSError as error:
        print(f'warning: the task log could not be trimmed ({error})', file=sys.stderr)
        return
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            _m_fs_trash.soft_delete(aside)
    except (OSError, SystemExit):
        pass

def reap_idle_tasks(keep: str | None, limit: float | None=None, by: str='') -> Sweep:
    """Move every folder idle past LIMIT days, else TASK_IDLE_DAYS, to the trash, except KEEP and unfinished work.

    BY names who asked, for the log.
    """
    limit = TASK_IDLE_DAYS if limit is None else limit
    record('swept', '', f"limit {limit:g} days{by and f', by {by}'}")
    swept = Sweep([], [], [], [])
    now = time.time()
    finished: list[tuple[Path, float]] = []
    for entry in sorted(task_folders()):
        if entry.name == keep:
            continue
        try:
            idle_days = (now - last_change(entry)) / DAY_SECONDS
        except OSError:
            continue
        if idle_days <= limit:
            continue
        why = unfinished(read_task(entry))
        if why is not None:
            swept.kept.append((entry.name, idle_days, why))
            swept.flagged.extend(((entry.name, flag) for flag in concerns(read_task(entry)) if flag != why))
            continue
        finished.append((entry, idle_days))
    for (entry, idle_days), kept in zip(finished, keep_records([each for each, _ in finished])):
        if kept.outcome is Outcome.REFUSED:
            swept.kept.append((entry.name, idle_days, f'{RECORDS_NOT_KEPT}: {kept.why}'))
            continue
        try:
            with contextlib.redirect_stderr(io.StringIO()):
                _m_fs_trash.soft_delete(entry)
        except (OSError, SystemExit):
            swept.stuck.append((entry.name, idle_days))
            continue
        record('reaped', entry.name, f'idle {idle_days:.1f} days')
        swept.reaped.append((entry.name, idle_days))
    return swept

def reap_once_a_day(keep: str) -> None:
    """Sweep, and trim the log, at the first call of the day; every later call stops at the marker."""
    if not claim_todays_sweep():
        return
    trim_log()
    reap_idle_tasks(keep)

def print_sweep(swept: Sweep, limit: float) -> None:
    """What `gc` moved, what it kept for unfinished work, and what would not go."""
    for sid, idle in swept.reaped:
        note(f'moved to the recycle bin: {sid}  idle {idle:.1f} days')
    for sid, idle, why in swept.kept:
        note(f'kept, {why}: {sid}  idle {idle:.1f} days')
    for sid, flag in swept.flagged:
        note(f'flagged, {flag}: {sid}')
    for sid, idle in swept.stuck:
        note(f'not moved, the recycle bin refused it: {sid}  idle {idle:.1f} days')
    if not (swept.reaped or swept.kept or swept.stuck):
        note(f'no task folder has been idle more than {limit:g} days')
    if swept.kept:
        note(f'a kept folder goes once its status is complete, or by `{CLOSE_HINT}` once its starter says the work is finished')

def collect(keep: str | None, idle_days: float | None) -> None:
    """Sweep now, as `gc` asks, and say what was moved and kept."""
    limit = TASK_IDLE_DAYS if idle_days is None else idle_days
    if not limit >= GC_MIN_IDLE_DAYS:
        fail(f'--idle-days is at least {GC_MIN_IDLE_DAYS}: a folder opened a moment ago would be judged by a plan its task has not begun to keep')
    print_sweep(reap_idle_tasks(keep, limit, by='gc'), limit)
    for location in prune_registry():
        note(f'{FORGOTTEN}: {location}')
    for location in registered_locations():
        note(f'{NOT_SWEPT}: {location}')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar git sweep-idle-task-folders`."""
    collector = verbs.add_parser(GC_COMMAND, help='sweep idle finished task folders now, and say what was moved and kept', description=f"Move to the OS recycle bin / Trash every task folder in which nothing\nhas changed for more than DAYS days ({TASK_IDLE_DAYS} unless given) and whose status\nis complete: the sweep `ensure` runs once a day, run now. Before a folder is\nmoved, whatever of its records the project's records branch does not hold\nis added ({RECORDS_BRANCH}, at {RECORDS_RELATIVE.as_posix()}/<id>/), all the folders moved in one\ncommit for each project: this sweep is the one act that adds records on its\nown. A folder whose plan or report Status is Queued is never moved.\nA folder whose status is not complete, whose {PLAN_NAME} cannot be read, or whose\nrecords cannot be kept, is kept however idle, and listed with why and how long it has\nbeen idle; one that looks finished or abandoned is also flagged, which moves nothing.\nYour own task is never swept. Only Memar's own .agents/tasks/ is swept: a project's\nown task location is named as not swept.")
    TaskId.add_flag(collector, 'your own task, which is never swept, however idle')
    collector.add_argument('--idle-days', type=float, default=None, metavar='DAYS', help=f'sweep folders idle more than DAYS days (default {TASK_IDLE_DAYS}, at least {GC_MIN_IDLE_DAYS})')
    return run

def run(args: argparse.Namespace) -> None:
    collect(args.task_id, args.idle_days)
