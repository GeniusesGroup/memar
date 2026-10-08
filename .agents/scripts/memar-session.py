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

Why plan.md. A session that stops mid-work leaves a folder, and whoever comes
next — another agent, or the same person tomorrow — needs what was asked and
what comes next without the first session's context. plan.md is that record,
and `list` reads it to find the folder again; the title is asked for when the
plan is first written because an id says only when a session opened, not what
it is about. The plan is divided by request rather than given one status for the
whole file: when a session is done is disputed — the person may come back, a
sub-agent that has reported may be handed more — but whether one request was met
is not, so the status sits on each request's section and the session's state is
read off them. plan.md is scratch, not a document, and is reaped with its
folder: a topic's lasting open state belongs in that topic's handoff, and closing
by type moves it there, so a plan that outlived its folder would be a second
handoff nobody maintains.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import NamedTuple


from memar_console import fail, note, use_utf8_stdio
from machine.fs_memar import scratch_root, session_dir
from machine.fs_trash import soft_delete
from memar_session import is_dated_session_id, is_session_id, new_session_id

NEW_COMMAND = "new"
LIST_COMMAND = "list"
CLOSE_COMMAND = "close"
PLAN_NAME = "plan.md"
STATUSES = ("open", "blocked", "done")
STATUS_PREFIX = "Status:"
NO_PLAN = f"(no {PLAN_NAME})"
NO_FRONT_MATTER = f"({PLAN_NAME} has no front matter)"
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


def checked_title(title: str | None, *, required: bool) -> str | None:
    """TITLE stripped, or None when it is blank; refused when REQUIRED and absent.

    A title is one line, because it is a front-matter value and a heading.
    """
    if title is not None:
        if "\n" in title or "\r" in title:
            fail("a title is one line; this one holds a line break")
        title = title.strip() or None
    if title is None and required:
        fail(f"--title is required: say in one line what the work is, for the folder's {PLAN_NAME}")
    return title


def project_root() -> Path:
    """The git top-level of the current directory, else the current directory."""
    try:
        found = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return Path.cwd()
    top = found.stdout.strip()
    return Path(top).resolve() if found.returncode == 0 and top else Path.cwd()


def plan_skeleton(title: str, opened: str, project: Path) -> str:
    """A new plan.md: front matter, the title, and one open section named for it."""
    return (
        "---\n"
        f"title: {title}\n"
        f"opened: {opened}\n"
        f"project: {project}\n"
        "---\n"
        f"# {title}\n"
        "\n"
        f"## {title}\n"
        f"{STATUS_PREFIX} open\n"
        "\n"
        "### Request\n"
        "\n"
        "### Steps\n"
        "\n"
        "### Next\n"
    )


def write_plan(folder: Path, title: str) -> None:
    """Create FOLDER's plan.md unless one is there; an existing plan is never touched."""
    opened = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    try:
        with (folder / PLAN_NAME).open("x", encoding="utf-8", newline="\n") as plan:
            plan.write(plan_skeleton(title, opened, project_root()))
    except FileExistsError:
        pass


def ensure_session(session_id: str | None = None, title: str | None = None) -> tuple[str, Path]:
    """Ensure <temp>/<session-id>/ and its plan.md exist and return its id and path.

    TITLE is required when the folder has no plan.md yet, and unused when it
    has one. A rerun with the same id is idempotent: the folder and its plan are
    kept as they are and the same id and path are reported again. The first
    call of a day also reaps the session folders that have been idle past the
    limit, other than this one.
    """
    sid = new_session_id() if session_id is None else session_id
    existed = session_dir(sid).is_dir()
    has_plan = (session_dir(sid) / PLAN_NAME).is_file()
    title = checked_title(title, required=not has_plan)
    path = session_dir(sid, create=True)
    if not existed:
        record("opened", sid)
    if not has_plan:
        write_plan(path, title)
    reap_idle_sessions(keep=sid)
    return sid, path


class Session(NamedTuple):
    path: Path
    has_plan: bool
    front: dict[str, str] | None
    sections: list[tuple[str, str]]


def read_plan(path: Path) -> tuple[dict[str, str] | None, list[tuple[str, str]]]:
    """PATH's front matter, None when absent, and each `##` section's heading and status.

    Front matter is the `key: value` lines between two `---` lines, each split
    at its first `: `: four keys do not need a YAML library installed.
    """
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    front: dict[str, str] | None = None
    body = lines
    if lines and lines[0].strip() == "---":
        for end in range(1, len(lines)):
            if lines[end].strip() == "---":
                pairs = (line.split(": ", 1) for line in lines[1:end] if ": " in line)
                front = {key.strip(): value.strip() for key, value in pairs} or None
                body = lines[end + 1:]
                break
    sections: list[tuple[str, str]] = []
    for line in body:
        if line.startswith("## "):
            sections.append((line[3:].strip(), ""))
        elif sections and not sections[-1][1] and line.startswith(STATUS_PREFIX):
            sections[-1] = (sections[-1][0], line[len(STATUS_PREFIX):].strip().lower())
    return front, sections


def read_session(folder: Path) -> Session:
    plan = folder / PLAN_NAME
    if not plan.is_file():
        return Session(folder, False, None, [])
    try:
        front, sections = read_plan(plan)
    except (OSError, UnicodeDecodeError):
        front, sections = None, []
    return Session(folder, True, front, sections)


def matches(session: Session, text: str) -> bool:
    """Whether TEXT is in the session's title, project, or a section heading, in any case."""
    front = session.front or {}
    fields = (front.get("title", ""), front.get("project", ""), *(heading for heading, _ in session.sections))
    needle = text.casefold()
    return any(needle in field.casefold() for field in fields)


def find_sessions(text: str | None = None) -> list[Session]:
    """Every session folder under the scratch root, newest first, filtered by TEXT."""
    folders = [
        entry
        for entry in scratch_root().iterdir()
        if is_session_id(entry.name) and entry.is_dir() and not entry.is_symlink()
    ]
    folders.sort(key=lambda entry: (is_dated_session_id(entry.name), entry.name), reverse=True)
    sessions = [read_session(folder) for folder in folders]
    return [session for session in sessions if not text or matches(session, text)]


def count_statuses(sections: list[tuple[str, str]]) -> str:
    """How many sections are in each status, e.g. `2 open, 1 done`."""
    counts = Counter(status or "no status" for _, status in sections)
    order = (*STATUSES, *sorted(set(counts) - set(STATUSES)))
    return ", ".join(f"{counts[status]} {status}" for status in order if counts[status]) or "no sections"


def print_session(session: Session) -> None:
    if not session.has_plan:
        print(f"{session.path.name}  {NO_PLAN}")
    elif session.front is None:
        print(f"{session.path.name}  {NO_FRONT_MATTER}")
    else:
        print(f"{session.path.name}  {session.front.get('title', '')}")
        note(f"project: {session.front.get('project', '')}")
    if session.has_plan:
        note(f"sections: {count_statuses(session.sections)}")
    note(f"path: {session.path}")


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

    memar session new --title TITLE   open a folder and print its id and path
    memar session list [TEXT]         find session folders, newest first
    memar session close               move one to the OS recycle bin / Trash

`new` prints an id and a path; pass that id back as `--session-id` to continue
the same session later. The path is absolute and lies in Memar's own checkout,
also when you work in another project: use it as printed, and never make a
folder of the same name in your project instead. If your file tool cannot reach
it, write there through `memar content write`.

A new session needs `--title`, one line saying what the work is, and so does a
folder that has no {PLAN_NAME} yet. `new` then writes the folder's {PLAN_NAME}, and
never overwrites one that is there:

    ---
    title: TITLE
    opened: the UTC time it was written, e.g. 2026-10-08T13:20:34Z
    project: the git top-level of where you ran `new`, else that folder
    ---
    # TITLE

    ## one thing the person asked
    Status: open

    ### Request
    ### Steps
    ### Next

Keep {PLAN_NAME} as you work, so another session can continue from it. Give each
distinct thing the person asks its own `##` section, added as requests arrive;
the first message may already hold several. The first section is named for the
title; rename it when the request says it better. Each section carries its own
`Status:`, open, blocked, or done, and three parts: Request, what was asked, in
the person's words; Steps, each marked local or delegated, with its state; Next,
what the next session does first. The plan has no status of its own: the work
is finished when its sections are.

To continue a piece of work another session left:

    memar session list TEXT             find it by title, project, or section
    memar session new --session-id ID   take that folder up as your session
    then read its {PLAN_NAME} and start from each open section's Next.

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
    opener.add_argument(
        "--title",
        default=None,
        help=f"one line saying what the work is; required unless the folder has a {PLAN_NAME}",
    )
    lister = verbs.add_parser(
        LIST_COMMAND,
        help="list session folders, newest first",
        description=(
            "List every session folder, newest first: its id, title, project, how\n"
            "many of its sections are open, blocked, and done, and its path. A folder\n"
            f"with no {PLAN_NAME}, or one without front matter, is listed and marked so."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    lister.add_argument(
        "text",
        nargs="?",
        metavar="TEXT",
        help="show only sessions whose title, project, or a section heading holds TEXT, in any case",
    )
    closer = verbs.add_parser(CLOSE_COMMAND, help="move a finished session folder to the OS recycle bin / Trash")
    closer.add_argument("--session-id", required=True, help="the session id to close")
    args = parser.parse_args(argv)
    if args.verb == NEW_COMMAND:
        sid, path = ensure_session(args.session_id, args.title)
        note(f"session_id: {sid}")
        note(f"path: {path}")
        note(f"plan: {path / PLAN_NAME}")
    elif args.verb == LIST_COMMAND:
        sessions = find_sessions(args.text)
        for session in sessions:
            print_session(session)
        if not sessions:
            note("no session folder matches" if args.text else "no session folder")
    else:
        sid, path, removed = close_session(args.session_id)
        note(f"{'closed' if removed else 'already closed'}: {sid}")
        note(f"path: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
