#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/sweep_idle_task_folders.py — daily verify of the records branch.

Tasks live on `RECORDS_BRANCH` only; there is no task folder to trash or flush.
The daily ensure verifies the tip and trims the task log.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
scratch_root = _m_fs_memar.scratch_root
_m_fs_lock = import_module('modules-plugable.computer.memory.filesystem.services.fs_lock')
claim_today = _m_fs_lock.claim_today
_m_fs_trash = import_module('modules-plugable.computer.memory.filesystem.services.fs_trash')
import argparse
import contextlib
import io
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Callable, NamedTuple
from machine.console import note
_m_task_store = import_module('modules-plugable.computer.git.services.task_store')
_m_branch = import_module('modules-plugable.computer.git.services.branch')
RecordRefused = _m_branch.RecordRefused
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
prune_registry = _m_task_location.prune_registry
registered_locations = _m_task_location.registered_locations
from .log import TASK_LOG_NAME, log_path, record
_m_task_id = import_module('modules-plugable.management.task.primitive.task_id')
TaskId = _m_task_id.TaskId
GC_COMMAND = 'sweep-idle-task-folders'
LOG_KEEP_DAYS = 28
SWEPT_MARKER_NAME = 'tasks.swept'
NOT_SWEPT = "not swept, a project's own task location, which is the project's to keep or delete"
FORGOTTEN = 'no longer recorded, a project task location that is gone'

class Sweep(NamedTuple):
    flushed: list[str]
    refused: list[tuple[str, str]]
    tip: str | None

def claim_todays_sweep() -> bool:
    marker = scratch_root() / SWEPT_MARKER_NAME
    return claim_today(marker)

def trim_log() -> None:
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

def flush_records(keep: str | None=None, by: str='') -> Sweep:
    """Verify the records branch tip; drop any leftover retired task-store folder."""
    del keep
    record('flushed', '', f"daily records{by and f', by {by}'}")
    _m_task_store.drop_legacy_task_store()
    tip: str | None
    refused: list[tuple[str, str]] = []
    try:
        tip = _m_task_store.verify_tip()
    except RecordRefused as error:
        tip = None
        refused.append(('*', str(error)))
    return Sweep([], refused, tip)

def reap_idle_tasks(keep: str | None, limit: float | None=None, by: str='') -> Sweep:
    del limit
    return flush_records(keep, by=by)

def reap_once_a_day(keep: str) -> None:
    if not claim_todays_sweep():
        return
    trim_log()
    flush_records(keep)

def print_sweep(swept: Sweep) -> None:
    for sid, why in swept.refused:
        note(f'refused, {why}: {sid}')
    if swept.tip:
        note(f'tip: {swept.tip}')
    else:
        note(f'no tip for {RECORDS_BRANCH}')

def collect(keep: str | None, idle_days: float | None) -> None:
    del idle_days
    print_sweep(flush_records(keep, by='gc'))
    for location in prune_registry():
        note(f'{FORGOTTEN}: {location}')
    for location in registered_locations():
        note(f'{NOT_SWEPT}: {location}')

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    collector = verbs.add_parser(GC_COMMAND, help='verify the records branch tip', description=f"Verify the tip of {RECORDS_BRANCH} (tasks at {RECORDS_RELATIVE.as_posix()}/<id>/).\nThere is no task folder to sweep: tasks live on the branch. The daily `ensure`\nruns this once a day. --idle-days is ignored.")
    TaskId.add_flag(collector, 'ignored; kept for compatibility')
    collector.add_argument('--idle-days', type=float, default=None, metavar='DAYS', help='ignored; kept so older callers do not break')
    return run

def run(args: argparse.Namespace) -> None:
    collect(args.task_id, args.idle_days)
