#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_migrate.py — session folders an earlier Memar left in temp/, moved into temp/sessions/.

Session folders used to sit directly in temp/, beside the locks, the test
scratch, and whatever else scratch holds; they now have a folder of their own.
A person who updates Memar runs no command for the purpose, so the session
commands after the update move the folders an earlier version left, say what
they moved, and record once nothing is left that the move is done, so later
commands do not look again.

Which folder is a session an earlier Memar left is `session_folder`'s answer,
because until it moves it is still that session's folder. Nothing else in
temp/ is touched: not the lock folder, not the test scratch, not the sessions
folder itself. The session log and the daily sweep's marker move too, before
the folders, since they describe them; one that cannot move stays readable
where it is and holds nothing up.

The update arrives in the background, while sessions are at work, and an
agent at work keeps writing to the path it was given, which would make the
folder again behind the move. So a folder in which anything changed within
MIGRATE_IDLE_DAYS, measured as the sweep measures idle, is left for a later
command, and the marker waits for it. A session continued by its id before
then is moved by `take_up` as it is continued, because its agent is the one
asking and is given the new path; where the system will not move it, the
session goes on in temp/, and nothing is made beside it.

A move is a rename within one filesystem, never a copy and a delete, so a
folder is whole either where it was or where it goes. A name already taken in
temp/sessions/ is never merged or overwritten: the folder from temp/ is set
beside it, its name ending in SET_ASIDE_SUFFIX, which no session id has, and
that is reported once. A folder the system will not move — one held open on
Windows — is left, reported, and tried again by the next command.

What moved is printed on stderr, and also left through
`services/update_daily.py`'s once-shown notice, the line the next `memar`
command prints: the command that moved the folders may be another agent's, and
the person whose session moved has to hear of it somewhere they look.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import NamedTuple

from machine.fs_memar import scratch_root, sessions_root
from services.session_folder import is_left_session, measured_idle
from services.session_gc import SWEPT_MARKER_NAME
from services.session_log import SESSION_LOG_NAME, record
from services.update_daily import leave_notice, state_dir

MIGRATED_MARKER_NAME = "sessions.migrated"
MOVED_FILES = (SESSION_LOG_NAME, SWEPT_MARKER_NAME)
MIGRATE_IDLE_DAYS = 1
SET_ASIDE_SUFFIX = ".from-temp"
NOTICE_SUBJECT = "sessions"
LIST_HINT = "memar session list"


class Migration(NamedTuple):
    """What one pass did: moved, set beside a taken name, left with why, and waiting while at work."""

    moved: list[tuple[Path, Path]]
    set_aside: list[tuple[Path, Path]]
    left: list[tuple[Path, str]]
    waiting: list[Path]


def _move(source: Path, target: Path) -> str | None:
    """Rename SOURCE to TARGET; why it was not moved, or None when it was.

    An empty reason is a folder another command moved first.
    """
    if target.exists() or target.is_symlink():
        return f"{target} is already there"
    try:
        os.rename(source, target)
    except FileNotFoundError:
        return "" if not source.exists() else "it could not be found to move"
    except OSError as error:
        return error.strerror or str(error)
    return None


def _any_left(temp: Path) -> bool:
    try:
        return any(is_left_session(entry) for entry in temp.iterdir())
    except OSError:
        return True


def migrate_left_sessions() -> Migration:
    """Move every quiet session folder directly in temp/ into temp/sessions/, unless that was done before."""
    sessions = sessions_root()
    marker = sessions / MIGRATED_MARKER_NAME
    done = Migration([], [], [], [])
    if marker.is_file():
        return done
    temp = scratch_root()
    for name in MOVED_FILES:
        source = temp / name
        if source.is_file() and not source.is_symlink():
            _move(source, sessions / name)
    for entry in sorted(temp.iterdir()):
        if not is_left_session(entry):
            continue
        idle = measured_idle(entry)
        if idle is None or idle < MIGRATE_IDLE_DAYS:
            done.waiting.append(entry)
            continue
        target = sessions / entry.name
        taken = target.exists() or target.is_symlink()
        if taken:
            target = sessions / f"{entry.name}{SET_ASIDE_SUFFIX}"
        why = _move(entry, target)
        if why is None:
            (done.set_aside if taken else done.moved).append((entry, target))
            record("moved", entry.name, f"from {entry.parent}" + (f", set beside {entry.name} as {target.name}" if taken else ""))
        elif why:
            done.left.append((entry, why))
    if not _any_left(temp):
        stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
        try:
            marker.write_text(
                f"{stamp}\tmoved {len(done.moved) + len(done.set_aside)}\n", encoding="utf-8", newline="\n"
            )
        except OSError as error:
            print(f"warning: the move marker could not be written ({error})", file=sys.stderr)
    return done


def take_up(session_id: str) -> Path | None:
    """Move SESSION_ID's folder from temp/ into temp/sessions/ as its session continues it.

    Where the session's folder is now: moved, or still in temp/ when the system
    would not move it, so the session goes on there; None when no such folder
    is in temp/ and nothing is under temp/sessions/ either. The caller checks
    the id, and calls this only when temp/sessions/ holds no folder of it.
    """
    left = scratch_root() / session_id
    if not is_left_session(left):
        return None
    target = sessions_root() / session_id
    why = _move(left, target)
    if why is None:
        record("moved", session_id, f"from {left.parent}, as it was continued")
        print(f"memar session: moved from temp/, as it was continued: {left}  ->  {target}", file=sys.stderr)
        return target
    if not why:
        return target if target.is_dir() else None
    print(f"memar session: {left} could not be moved into {target.parent} ({why}); the session goes on in it", file=sys.stderr)
    return left


def notice_lines(done: Migration) -> list[str]:
    """What a person needs to hear of DONE, one line per thing to say."""
    lines = []
    if done.moved:
        lines.append(
            f"{len(done.moved)} session folder(s) an earlier Memar left in temp/ were moved into "
            f"{done.moved[0][1].parent}; each keeps its id, and `{LIST_HINT}` finds it"
        )
    for source, aside in done.set_aside:
        lines.append(
            f"{source} was moved to {aside}, because {aside.parent / source.name} was already there; "
            "nothing was merged, so compare the two by hand"
        )
    return lines


def migrate() -> None:
    """Move the folders an earlier Memar left, and say on stderr, and once to the next command, what moved."""
    done = migrate_left_sessions()
    if done.moved:
        print("memar session: session folders moved from temp/ into temp/sessions/:", file=sys.stderr)
        for source, target in done.moved:
            print(f"    {source.name}  ->  {target}", file=sys.stderr)
    for source, aside in done.set_aside:
        print(f"memar session: set beside a folder of the same id, not merged: {source}  ->  {aside}", file=sys.stderr)
    for source, why in done.left:
        print(f"memar session: left in temp/, tried again next time: {source} ({why})", file=sys.stderr)
    lines = notice_lines(done)
    if lines:
        try:
            leave_notice(state_dir(), "\n".join(lines), subject=NOTICE_SUBJECT, add=True)
        except OSError as error:
            print(f"warning: the notice of the move could not be left ({error})", file=sys.stderr)
