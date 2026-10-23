#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/log.py — the task log: one line per thing done to a task folder.

Opening, closing, reaping, moving, and each sweep are recorded here, one
tab-separated line each — time, event, id, detail — beside the folders, because
the log is where a person looks for a folder that is no longer there.

Each location keeps its own log, in its root: a task in a project's own
task location (`task_location`) is recorded in that location's log, so
the project that keeps, commits, or deletes the folders keeps their record with
them, and Memar's own log holds Memar's own tasks and its sweeps. A task
an earlier Memar left directly in temp/ is Memar's, so it is recorded in
Memar's log, not beside it. Keeping Memar's log from growing without end is the
daily sweep's, in `task_gc`; a project's log is the project's.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
tasks_root = _m_fs_memar.tasks_root
import sys
from datetime import datetime, timezone
from pathlib import Path
from modules.process.project.services.task_location import in_project_location
TASK_LOG_NAME = 'tasks.log'

def log_path(folder: Path | None=None) -> Path:
    """The log FOLDER, a task folder, is recorded in: its project location's, else Memar's own."""
    if folder is not None and in_project_location(folder):
        return folder.parent / TASK_LOG_NAME
    return tasks_root() / TASK_LOG_NAME

def record(event: str, task_id: str, detail: str='', folder: Path | None=None) -> None:
    """Append one line to the log of FOLDER's location, else to Memar's own: time, event, id, detail."""
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    line = '\t'.join((stamp, event, task_id, detail)) + '\n'
    try:
        with log_path(folder).open('a', encoding='utf-8', newline='\n') as log:
            log.write(line)
    except OSError as error:
        print(f'warning: the task log could not be written ({error})', file=sys.stderr)
