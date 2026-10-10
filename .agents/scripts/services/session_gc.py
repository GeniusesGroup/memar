#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_gc.py — the sweep: idle finished session folders moved to the trash.

No session has to ask for its own close. No agent knows at a reliable moment
that the work is finished — the person may come back tomorrow, and a sub-agent
that has reported may be handed more — and a message spent asking is paid by
every session there is. So the sweep reaps instead: every session folder in
which nothing has changed for the idle limit and whose status is done — a
folder holding no plan has nothing unfinished — is moved to the OS trash, where
it can be recovered, and the reap is recorded in the session log. Idle is not
the same as finished, so a session whose status is not done is never swept:
carrying that task to the next session is what the folder is there for, and it
goes only when its status is done or a person closes it. The test is done
rather than not open: a status is a vocabulary this file does not own — today
open, blocked, done, and another can be added tomorrow — and a status it does
not know, or none, is not done, so such a folder is kept; so is one whose plan
cannot be read, since its status is not known either. What counts as done is
`session_plan.is_done`, which also reads the free-text finished statuses
earlier plans wrote. The limit is
SESSION_IDLE_DAYS below, a number in this file rather than a per-machine
setting: changing it is an edit reviewed like any other. Only folders named in
the form `session_id` mints are reaped, and never the one being opened or
continued.

The sweep runs once a day, at the first `new` of the day. A person opens dozens
of sessions a day, and walking hundreds of folders on each of them is load for
nothing, since a folder idle for a week does not become more idle by the hour.
Whether today's sweep happened is read from a one-line marker holding its date,
not from the log: the log grows with every session, and reading it on each
`new` would bring back the cost the daily sweep removes. The guard is
`machine/fs_lock.claim_today`, which the daily update asks too. The same sweep keeps
the log from growing without end: lines older than LOG_KEEP_DAYS, four idle
limits, are moved into a dated file that goes to the trash, so an old record
leaves the log without being deleted for good. The caller of `new` is not told
what was reaped: it was not their session, and the log is where a person looks
for a folder that is gone.

`gc` is the same sweep asked for by a person, not a second one: the daily guard
is a separate step in front of it, so `new` keeps its once-a-day cost and `gc`
sweeps whenever it is run, by the same rules, and logs the same way. Unlike
`new` it prints what it moved, because its caller asked, and it lists the idle
folders it kept for unfinished work with their age, because those are the ones
only a person can let go. It may be given a shorter limit, never one under
GC_MIN_IDLE_DAYS: at zero, a folder opened a moment ago would be judged by a
plan its session has not begun to keep.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import sys
import time
from datetime import datetime, timedelta, timezone
from typing import Callable, NamedTuple

from machine.console import fail, note
from machine.fs_memar import sessions_root
from services.session_folder import DAY_SECONDS, Session, last_change, read_session, session_folders
from services.session_log import SESSION_LOG_NAME, log_path, record
from services.session_plan import PLAN_NAME, is_done

GC_COMMAND = "gc"
SESSION_IDLE_DAYS = 7
GC_MIN_IDLE_DAYS = 1
LOG_KEEP_DAYS = 4 * SESSION_IDLE_DAYS
SWEPT_MARKER_NAME = "sessions.swept"
CLOSE_HINT = "memar session close --session-id ID"


class Sweep(NamedTuple):
    """What one sweep did with the folders idle past its limit, each with its idle days."""

    reaped: list[tuple[str, float]]
    kept: list[tuple[str, float, str]]
    stuck: list[tuple[str, float]]


def unfinished(session: Session) -> str | None:
    """Why SESSION's task is not known to be finished, or None when it is."""
    if not session.has_plan:
        return None
    if not session.readable:
        return f"its {PLAN_NAME} cannot be read"
    if not is_done(session.status):
        return f"its status is {session.status}" if session.status else "it has no status"
    return None


def claim_todays_sweep() -> bool:
    """Whether this call is the first today, recording today's date if it is."""
    from machine.fs_lock import claim_today

    return claim_today(sessions_root() / SWEPT_MARKER_NAME)


def trim_log() -> None:
    """Move log lines older than LOG_KEEP_DAYS into a file sent to the trash.

    A line whose time cannot be read is kept: it is not known to be old.
    """
    from machine.fs_trash import soft_delete

    log = log_path()
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


def reap_idle_sessions(keep: str | None, limit: float | None = None, by: str = "") -> Sweep:
    """Move every folder idle past LIMIT days, else SESSION_IDLE_DAYS, to the trash, except KEEP and unfinished work.

    BY names who asked, for the log.
    """
    from machine.fs_trash import soft_delete

    limit = SESSION_IDLE_DAYS if limit is None else limit
    record("swept", "", f"limit {limit:g} days{by and f', by {by}'}")
    swept = Sweep([], [], [])
    now = time.time()
    for entry in sorted(session_folders()):
        if entry.name == keep:
            continue
        try:
            idle_days = (now - last_change(entry)) / DAY_SECONDS
        except OSError:
            continue
        if idle_days <= limit:
            continue
        why = unfinished(read_session(entry))
        if why is not None:
            # Not finished, only quiet: the folder is what carries its task to
            # the next session, so it is reaped once its status is done or when
            # a person closes it, never by the clock.
            swept.kept.append((entry.name, idle_days, why))
            continue
        try:
            # The trash reports what it moved on stderr, and whoever asked is
            # told by the caller, which knows whether that is anyone's business.
            with contextlib.redirect_stderr(io.StringIO()):
                soft_delete(entry)
        except (OSError, SystemExit):
            # soft_delete reports a failure by exiting. A folder that will not
            # go is retried by the next sweep; it is no reason to refuse the
            # session being opened.
            swept.stuck.append((entry.name, idle_days))
            continue
        record("reaped", entry.name, f"idle {idle_days:.1f} days")
        swept.reaped.append((entry.name, idle_days))
    return swept


def reap_once_a_day(keep: str) -> None:
    """Sweep, and trim the log, at the first call of the day; every later call stops at the marker."""
    if not claim_todays_sweep():
        return
    trim_log()
    reap_idle_sessions(keep)


def print_sweep(swept: Sweep, limit: float) -> None:
    """What `gc` moved, what it kept for unfinished work, and what would not go."""
    for sid, idle in swept.reaped:
        note(f"moved to the recycle bin: {sid}  idle {idle:.1f} days")
    for sid, idle, why in swept.kept:
        note(f"kept, {why}: {sid}  idle {idle:.1f} days")
    for sid, idle in swept.stuck:
        note(f"not moved, the recycle bin refused it: {sid}  idle {idle:.1f} days")
    if not (swept.reaped or swept.kept or swept.stuck):
        note(f"no session folder has been idle more than {limit:g} days")
    if swept.kept:
        note(f"a kept folder goes once its status is done, or by `{CLOSE_HINT}` once its starter says the work is finished")


def collect(keep: str | None, idle_days: float | None) -> None:
    """Sweep now, as `gc` asks, and say what was moved and kept."""
    limit = SESSION_IDLE_DAYS if idle_days is None else idle_days
    if not limit >= GC_MIN_IDLE_DAYS:
        fail(
            f"--idle-days is at least {GC_MIN_IDLE_DAYS}: a folder opened a moment ago "
            "would be judged by a plan its session has not begun to keep"
        )
    print_sweep(reap_idle_sessions(keep, limit, by="gc"), limit)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session gc`."""
    collector = verbs.add_parser(
        GC_COMMAND,
        help="sweep idle finished session folders now, and say what was moved and kept",
        description=(
            "Move to the OS recycle bin / Trash every session folder in which nothing\n"
            f"has changed for more than DAYS days ({SESSION_IDLE_DAYS} unless given) and whose status\n"
            "is done: the sweep `new` runs once a day, run now. A folder whose status\n"
            f"is not done, or whose {PLAN_NAME} cannot be read, is kept however idle it is,\n"
            "and listed with how long it has been idle, so a person can see which ones\n"
            "only they can let go. Your own session is never swept."
        ),
    )
    collector.add_argument(
        "--session-id",
        default=None,
        help="your own session, which is never swept, however idle",
    )
    collector.add_argument(
        "--idle-days",
        type=float,
        default=None,
        metavar="DAYS",
        help=f"sweep folders idle more than DAYS days (default {SESSION_IDLE_DAYS}, at least {GC_MIN_IDLE_DAYS})",
    )
    return run


def run(args: argparse.Namespace) -> None:
    collect(args.session_id, args.idle_days)
