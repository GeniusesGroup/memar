#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/log.py — the session log: one line per thing done to a session folder.

Opening, closing, reaping, moving, and each sweep are recorded here, one
tab-separated line each — time, event, id, detail — beside the folders, because
the log is where a person looks for a folder that is no longer there.

Each location keeps its own log, in its root: a session in a project's own
session location (`session_location`) is recorded in that location's log, so
the project that keeps, commits, or deletes the folders keeps their record with
them, and Memar's own log holds Memar's own sessions and its sweeps. A session
an earlier Memar left directly in temp/ is Memar's, so it is recorded in
Memar's log, not beside it. Keeping Memar's log from growing without end is the
daily sweep's, in `session_gc`; a project's log is the project's.
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

from machine.fs_memar import sessions_root
from modules.process.session.services.location import in_project_location

SESSION_LOG_NAME = "sessions.log"


def log_path(folder: Path | None = None) -> Path:
    """The log FOLDER, a session folder, is recorded in: its project location's, else Memar's own."""
    if folder is not None and in_project_location(folder):
        return folder.parent / SESSION_LOG_NAME
    return sessions_root() / SESSION_LOG_NAME


def record(event: str, session_id: str, detail: str = "", folder: Path | None = None) -> None:
    """Append one line to the log of FOLDER's location, else to Memar's own: time, event, id, detail."""
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = "\t".join((stamp, event, session_id, detail)) + "\n"
    try:
        with log_path(folder).open("a", encoding="utf-8", newline="\n") as log:
            log.write(line)
    except OSError as error:
        print(f"warning: the session log could not be written ({error})", file=sys.stderr)
