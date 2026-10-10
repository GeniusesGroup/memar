#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_log.py — the session log: one line per thing done to a session folder.

Opening, closing, reaping, moving, and each sweep are recorded here, one
tab-separated line each — time, event, id, detail — beside the folders, because
the log is where a person looks for a folder that is no longer there. Keeping
it from growing without end is the daily sweep's, in `session_gc`.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from machine.fs_memar import sessions_root

SESSION_LOG_NAME = "sessions.log"


def log_path() -> Path:
    return sessions_root() / SESSION_LOG_NAME


def record(event: str, session_id: str, detail: str = "") -> None:
    """Append one line to the session log: time, event, id, detail."""
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = "\t".join((stamp, event, session_id, detail)) + "\n"
    try:
        with log_path().open("a", encoding="utf-8", newline="\n") as log:
            log.write(line)
    except OSError as error:
        print(f"warning: the session log could not be written ({error})", file=sys.stderr)
