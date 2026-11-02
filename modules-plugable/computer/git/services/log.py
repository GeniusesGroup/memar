#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/log.py — the task log: one line per thing done to a task.

Opening, closing, reaping, moving, and each sweep are recorded here, one
tab-separated line each — time, event, id, detail — under the Memar scratch
root (`temp/tasks.log`), because the log is where a person looks for a task
that is no longer listed and must not sit beside durable records or in the
checkout root.

Tasks themselves live on `RECORDS_BRANCH`, not as folders. The optional
`folder` argument is kept only so callers that still pass a path keep compiling;
it does not choose the log path. Keeping the log from growing without end is
the daily sweep's, in `task_gc`.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
scratch_root = _m_fs_memar.scratch_root
import sys
from datetime import datetime, timezone
from pathlib import Path
TASK_LOG_NAME = 'tasks.log'

def log_path(folder: Path | None=None) -> Path:
    """The one task log: `<memar-root>/temp/tasks.log`. FOLDER is ignored."""
    del folder
    return scratch_root() / TASK_LOG_NAME

def record(event: str, task_id: str, detail: str='', folder: Path | None=None) -> None:
    """Append one line to temp/tasks.log: time, event, id, detail."""
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    line = '\t'.join((stamp, event, task_id, detail)) + '\n'
    path = log_path(folder)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8', newline='\n') as log:
            log.write(line)
    except OSError as error:
        print(f'warning: the task log could not be written ({error})', file=sys.stderr)
