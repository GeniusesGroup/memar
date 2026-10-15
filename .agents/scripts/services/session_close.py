#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_close.py — one session's folder moved to the OS trash, on its starter's word.

The sweep in `session_gc` is how folders normally go; `close` remains for the
case where the person who started the session has already said the work is
finished. The folder goes to the trash rather than being deleted, so a session
closed by mistake costs one trip to the trash, and a trash that fails leaves
the folder where it was: a failed recovery is not a successful close.

Before the folder goes, its records are kept in its project
(`session_archive`), as the sweep keeps them. A folder whose records cannot be
kept is not closed, because closing it would drop them without a word; the
person may still close it without them, by saying so (`--without-records`),
for a project that is gone for good.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable, NamedTuple

from machine.console import fail, note
from machine.fs_memar import RECORDS_RELATIVE
from services.session_archive import Kept, Outcome, keep_records
from services.session_folder import folder_of, foreign_project_entry
from services.project_preferences import SESSIONS_KEY
from services.session_gc import GC_COMMAND
from services.session_log import record

CLOSE_COMMAND = "close"
WITHOUT_RECORDS_FLAG = "--without-records"


class Closed(NamedTuple):
    """One close: the id, its folder, whether anything was moved to recoverable storage, and how its records were kept."""

    id: str
    path: Path
    removed: bool
    kept: Kept | None = None


def close_session(session_id: str, *, without_records: bool = False) -> Closed:
    """Keep one session's records, then trash its folder. Idempotent: a missing folder is already closed.

    The target is confined to the session folder by construction:
    session_dir refuses anything shaped like a path. A session an earlier
    Memar left in temp/, not moved yet, is closed where it is, and so is one
    in a project's own session location, on the same word of its starter; a
    folder of that name there that is not a session's is refused. A folder
    whose records cannot be kept is refused, unless WITHOUT_RECORDS.
    """
    from machine.fs_trash import soft_delete

    path = folder_of(session_id)
    if not path.exists() and not path.is_symlink():
        foreign = foreign_project_entry(session_id)
        if foreign is not None:
            fail(f"{foreign} is not a session folder; `close` closes only a session's folder")
        return Closed(session_id, path, False)
    kept = keep_records(path)
    if kept.outcome is Outcome.REFUSED and not without_records:
        fail(
            f"{session_id} was not closed: its records cannot be kept, {kept.why}; "
            f"settle that, or close it without them with {WITHOUT_RECORDS_FLAG}"
        )
    if kept.outcome is Outcome.KEPT:
        record("recorded", session_id, str(kept.folder), folder=path)
    soft_delete(path)
    record("closed", session_id, folder=path)
    return Closed(session_id, path, True, kept)


def close(session_id: str, without_records: bool = False) -> None:
    """`close`: keep the records, trash the folder, and say what was done."""
    closed = close_session(session_id, without_records=without_records)
    note(f"{'closed' if closed.removed else 'already closed'}: {closed.id}")
    note(f"path: {closed.path}")
    if closed.kept is None:
        return
    if closed.kept.outcome is Outcome.KEPT:
        note(f"records: {closed.kept.folder}")
    else:
        note(f"records not kept, {closed.kept.why}")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session close`."""
    closer = verbs.add_parser(
        CLOSE_COMMAND,
        help="move a finished session folder to the OS recycle bin / Trash",
        description=(
            "Move the session folder SESSION_ID to the OS recycle bin / Trash, so a\n"
            "mistake costs one trip there; a folder already gone is already closed.\n"
            "First its records — its plan, its report, and the files the report links\n"
            f"to — are copied into {RECORDS_RELATIVE.as_posix()}/ in the project its plan names, and\n"
            "the folder holding them is printed; a folder whose records cannot be kept\n"
            f"is not closed, unless {WITHOUT_RECORDS_FLAG} is given.\n"
            "Run it only when the person who started the session has already said the\n"
            "work is finished; never ask them to, and never close a session you did not\n"
            "open. You do not have to close a session: once a day `new` sweeps the idle\n"
            f"folders whose status is complete (`{GC_COMMAND}` runs that sweep at once), and a\n"
            f"project that keeps its finished sessions (its preferences set `{SESSIONS_KEY}`)\n"
            "closes none."
        ),
    )
    closer.add_argument("--session-id", required=True, help="the session id to close")
    closer.add_argument(
        WITHOUT_RECORDS_FLAG,
        action="store_true",
        help="close it even though its records cannot be kept, which loses them; only on its starter's word",
    )
    return run


def run(args: argparse.Namespace) -> None:
    close(args.session_id, args.without_records)
