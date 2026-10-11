#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_close.py — one session's folder moved to the OS trash, on its starter's word.

The sweep in `session_gc` is how folders normally go; `close` remains for the
case where the person who started the session has already said the work is
finished. The folder goes to the trash rather than being deleted, so a session
closed by mistake costs one trip to the trash, and a trash that fails leaves
the folder where it was: a failed recovery is not a successful close.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from machine.console import fail, note
from services.session_folder import folder_of, foreign_project_entry
from services.session_log import record

CLOSE_COMMAND = "close"


def close_session(session_id: str) -> tuple[str, Path, bool]:
    """Trash one session's folder. Idempotent: a missing folder is already closed.

    Returns the id, its path, and whether anything was moved to recoverable
    storage. The target is confined to the session folder by construction:
    session_dir refuses anything shaped like a path. A session an earlier
    Memar left in temp/, not moved yet, is closed where it is, and so is one
    in a project's own session location, on the same word of its starter; a
    folder of that name there that is not a session's is refused.
    """
    from machine.fs_trash import soft_delete

    path = folder_of(session_id)
    if not path.exists() and not path.is_symlink():
        foreign = foreign_project_entry(session_id)
        if foreign is not None:
            fail(f"{foreign} is not a session folder; `close` closes only a session's folder")
        return session_id, path, False
    soft_delete(path)
    record("closed", session_id)
    return session_id, path, True


def close(session_id: str) -> None:
    """`close`: trash the folder and say whether anything was there."""
    sid, path, removed = close_session(session_id)
    note(f"{'closed' if removed else 'already closed'}: {sid}")
    note(f"path: {path}")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session close`."""
    closer = verbs.add_parser(CLOSE_COMMAND, help="move a finished session folder to the OS recycle bin / Trash")
    closer.add_argument("--session-id", required=True, help="the session id to close")
    return run


def run(args: argparse.Namespace) -> None:
    close(args.session_id)
