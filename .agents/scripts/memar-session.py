#!/usr/bin/env python3
"""memar-session.py — one session's scratch folder under temp/, opened and closed.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `memar session --help` prints: it is addressed to whoever is about
to open a session and says what to run and when its starter may close it.
Everything from here down is addressed to whoever opens this file. A person
opening a scratch folder does not need to know which module resolves the temp
root, and help output that told them would be a second, worse copy of this.

Why one folder per session, under ONE root. Parallel agent sessions edit one
shared working tree with no coordination, and concurrent writes to one file
collide silently — shared-tree collisions. The per-file advisory locks in
`machine/fs_lock.py` answer that, and the write verbs of `memar-content.py` take one,
but advisory locks are honored by skill rule and not by the filesystem:
file-write tools bypass them, and only intent notes saying who plans what
against which base let a waiter that takes over a stale lock read what the dead
session meant. Intent notes and locks are scratch, and scratch needs a home that
survives the session: session folders give every session its own folder, and
every session works inside its own folder so nothing lands in git by accident.
That home is <memar-root>/temp/, the ONE root the root .gitignore already
ignores — OS temp dirs are forbidden, because they are wiped by other apps
while sessions last days (the OS-temp wiped risk). The temp root resolves as the
recorded location else the checkout the tool runs inside; when neither resolves
this fails closed and guesses nothing.

Lifecycle. No session has to ask for its own close. No agent knows at a reliable
moment that the work is finished — the person may come back tomorrow, and a
sub-agent that has reported may be handed more — and a message spent asking is
paid by every session there is. So `new` reaps instead: every session folder in
which nothing has changed for the idle limit is moved to the OS trash, where it
can be recovered, and the reap is recorded in the session log beside the
folders. Idle is the latest change anywhere inside, because on Windows a
folder's own time does not move when a nested file is edited. The limit is
SESSION_IDLE_DAYS below, a number in this file rather than a per-machine
setting: changing it is an edit reviewed like any other. Only folders named in
the form `memar_session.py` mints are reaped, and never the one being opened or
continued. The caller of `new` is not told what was reaped: it was not their
session, and the log is where a person looks for a folder that is gone. `close`
remains for the case where the starter has already said the work is finished.

The sweep runs once a day, at the first `new` of the day. A person opens dozens
of sessions a day, and walking hundreds of folders on each of them is load for
nothing, since a folder idle for a week does not become more idle by the hour.
Whether today's sweep happened is read from a one-line marker holding its date,
not from the log: the log grows with every session, and reading it on each
`new` would bring back the cost the daily sweep removes. The same sweep keeps
the log from growing without end: lines older than LOG_KEEP_DAYS, four idle
limits, are moved into a dated file that goes to the trash, so an old record
leaves the log without being deleted for good.

A session writes only inside its own folder: --session-id reuses an id only to
continue the same logical session, and two sessions writing one folder
reintroduce the unattributed mixing this tool exists to remove. Reading another
session's folder is fine. Reading changes no modification time, though, so a
folder that is only read is still reaped once idle; a session that needs
something from an old folder copies it into its own.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


from memar_console import note, use_utf8_stdio
from machine.fs_memar import scratch_root, session_dir
from machine.fs_trash import soft_delete
from memar_session import is_session_id, new_session_id

NEW_COMMAND = "new"
CLOSE_COMMAND = "close"
SESSION_IDLE_DAYS = 7
LOG_KEEP_DAYS = 4 * SESSION_IDLE_DAYS
SESSION_LOG_NAME = "sessions.log"
SWEPT_MARKER_NAME = "sessions.swept"
DAY_SECONDS = 24 * 60 * 60


def last_change(path: Path) -> float:
    """The latest modification time of PATH or of anything inside it."""
    latest = path.stat().st_mtime
    for root, folders, files in os.walk(path):
        for name in (*folders, *files):
            try:
                changed = os.stat(os.path.join(root, name), follow_symlinks=False).st_mtime
            except OSError:
                continue
            latest = max(latest, changed)
    return latest


def record(event: str, session_id: str, detail: str = "") -> None:
    """Append one line to the session log: time, event, id, detail."""
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    line = "\t".join((stamp, event, session_id, detail)) + "\n"
    try:
        with (scratch_root() / SESSION_LOG_NAME).open("a", encoding="utf-8", newline="\n") as log:
            log.write(line)
    except OSError as error:
        print(f"warning: the session log could not be written ({error})", file=sys.stderr)


def claim_todays_sweep() -> bool:
    """Whether this call is the first today, recording today's date if it is."""
    marker = scratch_root() / SWEPT_MARKER_NAME
    today = date.today().isoformat()
    try:
        if marker.read_text(encoding="utf-8").strip() == today:
            return False
    except OSError:
        pass
    try:
        marker.write_text(today + "\n", encoding="utf-8", newline="\n")
    except OSError as error:
        print(f"warning: the sweep marker could not be written ({error})", file=sys.stderr)
    return True


def trim_log() -> None:
    """Move log lines older than LOG_KEEP_DAYS into a file sent to the trash.

    A line whose time cannot be read is kept: it is not known to be old.
    """
    log = scratch_root() / SESSION_LOG_NAME
    try:
        lines = log.read_text(encoding="utf-8").splitlines(keepends=True)
    except OSError:
        return
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=LOG_KEEP_DAYS)
    kept: list[str] = []
    old: list[str] = []
    for line in lines:
        try:
            stamp = datetime.fromisoformat(line.split("\t", 1)[0])
        except ValueError:
            kept.append(line)
            continue
        (old if stamp < cutoff else kept).append(line)
    if not old:
        return
    aside = log.with_name(f"{SESSION_LOG_NAME}.{now.date().isoformat()}")
    rewritten = log.with_name(f"{SESSION_LOG_NAME}.new")
    try:
        aside.write_text("".join(old), encoding="utf-8", newline="\n")
        rewritten.write_text("".join(kept), encoding="utf-8", newline="\n")
        # A line another `new` appends between the read above and this replace
        # is lost; the window is one daily rewrite of a short file.
        os.replace(rewritten, log)
    except OSError as error:
        print(f"warning: the session log could not be trimmed ({error})", file=sys.stderr)
        return
    try:
        with contextlib.redirect_stderr(io.StringIO()):
            soft_delete(aside)
    except (OSError, SystemExit):
        # The old lines stay beside the log, still readable, until a sweep can
        # move them.
        pass


def reap_idle_sessions(keep: str) -> None:
    """Move every session folder idle past the limit to the trash, except KEEP."""
    if not claim_todays_sweep():
        return
    trim_log()
    record("swept", "", f"limit {SESSION_IDLE_DAYS} days")
    now = time.time()
    for entry in sorted(scratch_root().iterdir()):
        if entry.name == keep or not is_session_id(entry.name):
            continue
        if entry.is_symlink() or not entry.is_dir():
            continue
        try:
            idle_days = (now - last_change(entry)) / DAY_SECONDS
        except OSError:
            continue
        if idle_days <= SESSION_IDLE_DAYS:
            continue
        try:
            # The trash reports what it moved on stderr, and this caller was not
            # the session that folder belonged to.
            with contextlib.redirect_stderr(io.StringIO()):
                soft_delete(entry)
        except (OSError, SystemExit):
            # soft_delete reports a failure by exiting. A folder that will not
            # go is retried by the next day's sweep; it is no reason to refuse
            # the session being opened.
            continue
        record("reaped", entry.name, f"idle {idle_days:.1f} days")


def ensure_session(session_id: str | None = None) -> tuple[str, Path]:
    """Ensure <temp>/<session-id>/ exists and return its id and path.

    A rerun with the same id is idempotent: the folder is kept as is and the
    same id and path are reported again. The first call of a day also reaps
    the session folders that have been idle past the limit, other than this one.
    """
    sid = new_session_id() if session_id is None else session_id
    existed = session_dir(sid).is_dir()
    path = session_dir(sid, create=True)
    if not existed:
        record("opened", sid)
    reap_idle_sessions(keep=sid)
    return sid, path


def close_session(session_id: str) -> tuple[str, Path, bool]:
    """Trash one session's folder. Idempotent: a missing folder is already closed.

    Returns the id, its path, and whether anything was moved to recoverable
    storage. The target is confined to the session folder by construction:
    session_dir refuses anything shaped like a path.
    """
    path = session_dir(session_id)
    if not path.exists() and not path.is_symlink():
        return session_id, path, False
    soft_delete(path)
    record("closed", session_id)
    return session_id, path, True


DESCRIPTION = f"""memar session — one folder for the work you are about to do

Work inside this folder, not in the checkout: the files you write while working
belong to your session, not to the repository.

    memar session new      open a folder and print its id and path
    memar session close    move it to the OS recycle bin / Trash

`new` prints an id and a path; pass that id back as `--session-id` to continue
the same session later.

Write only inside your own folder; reading another session's folder is fine.

You do not have to close a session. Once a day, the first `new` moves to the
recycle bin every session folder in which nothing has changed for
{SESSION_IDLE_DAYS} days. Run `close` only when the person who started the
session has already said the work is finished; never ask them to, and never
close a session you did not open.
"""


def main(argv: list[str] | None = None) -> int:
    use_utf8_stdio()
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    verbs = parser.add_subparsers(dest="verb", required=True)
    opener = verbs.add_parser(NEW_COMMAND, help="ensure one session folder and print its id and path")
    opener.add_argument(
        "--session-id",
        default=None,
        help="reuse this session id instead of minting one (rerun is idempotent)",
    )
    closer = verbs.add_parser(CLOSE_COMMAND, help="move a finished session folder to the OS recycle bin / Trash")
    closer.add_argument("--session-id", required=True, help="the session id to close")
    args = parser.parse_args(argv)
    if args.verb == NEW_COMMAND:
        sid, path = ensure_session(args.session_id)
        note(f"session_id: {sid}")
        note(f"path: {path}")
    else:
        sid, path, removed = close_session(args.session_id)
        note(f"{'closed' if removed else 'already closed'}: {sid}")
        note(f"path: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
