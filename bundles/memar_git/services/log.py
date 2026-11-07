#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
scratch_root = _m_memar_location.scratch_root
import sys
from datetime import datetime, timezone
from pathlib import Path
TASK_LOG_NAME = 'tasks.log'

def log_path(folder: Path | None=None) -> Path:
    del folder
    return scratch_root() / TASK_LOG_NAME

def record(event: str, task_id: str, detail: str='', folder: Path | None=None) -> None:
    stamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    line = '\t'.join((stamp, event, task_id, detail)) + '\n'
    path = log_path(folder)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('a', encoding='utf-8', newline='\n') as log:
            log.write(line)
    except OSError as error:
        print(f'warning: the task log could not be written ({error})', file=sys.stderr)
