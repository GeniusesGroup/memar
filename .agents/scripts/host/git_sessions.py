#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_sessions.py — the sessions a commit carries out, named in its message (owner, 2026-10-16).

A commit that cites no session cannot be traced to the decisions that produced it, so `commit`
refuses one unless the caller says it carries out none. The form is one git trailer a session,
`Session: <id>`, with the bare id: `git log --format=%(trailers:key=Session,valueonly)` reads it
back one id a line, a fold of several commits keeps the union of their lines, and `memar session
show` resolves the id to the session's folder or its records wherever they are today, so no
branch name is written into history.

The caller names each session with `--session-id` and the verb writes the trailer itself, through
`git interpret-trailers`, into the message's own trailer block, so a `Co-Authored-By:` stays a
trailer. A `Session:` the message already holds is refused: an id reaches history only by the one
route that checks it.

The check is `memar session show --list` run as a process, the same lookup a reader of the commit
will use, with the repository committed to as its project. This shelf imports nothing from
`services/`: the two meet at the command line, which is the interface `services/` offers anyone,
so the lookup has one implementation and this file holds none of its knowledge (where a session
folder is, which branch keeps records).
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from host.git_run import plumb

TRAILER = "Session"
NO_SESSION_FLAG = "--no-session"
SESSION_FLAG = "--session-id"
ROUTER = Path(__file__).resolve().parent.parent / "memar"


def cited_by_hand(message: str, root: Path) -> list[str]:
    """The `Session:` trailers MESSAGE already holds."""
    parsed = plumb(["interpret-trailers", "--parse", "--no-divider"], root, data=message.encode("utf-8"))
    return [
        value.strip()
        for key, _, value in (line.partition(":") for line in parsed.splitlines())
        if key.strip().lower() == TRAILER.lower()
    ]


def carried(parent: str, head: str, root: Path) -> list[str]:
    """The sessions the commits after PARENT up to HEAD cite, oldest first, each once: what a fold of them keeps."""
    if parent == head:
        return []
    listed = plumb(["log", "--reverse", f"--format=%(trailers:key={TRAILER},valueonly)", f"{parent}..{head}"], root)
    return list(dict.fromkeys(line.strip() for line in listed.splitlines() if line.strip()))


def not_found(session_ids: list[str], root: Path) -> list[str]:
    """For each of SESSION_IDS that `memar session show` cannot find in ROOT's project, what it said."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    said: list[str] = []
    for session_id in session_ids:
        shown = subprocess.run(
            [sys.executable, str(ROUTER), "session", "show", "--session-id", session_id, "--list", "--project-path", str(root)],
            capture_output=True, text=True, encoding="utf-8", errors="replace", env=env,
        )
        if shown.returncode != 0:
            said.append((shown.stderr.strip() or shown.stdout.strip() or f"no session {session_id}").removeprefix("error: "))
    return said


def checked(message: str, given: list[str], no_session: bool, parent: str, head: str, root: Path) -> list[str]:
    """The sessions the commit cites, in order: those the commits it folds cite, then GIVEN; refused, naming the form, when there are none and NO_SESSION is not said."""
    if no_session and given:
        sys.exit(f"error: {NO_SESSION_FLAG} says the commit carries out no session, and {SESSION_FLAG} names one; give one of the two. Nothing was committed.")
    by_hand = cited_by_hand(message, root)
    if by_hand:
        sys.exit(
            f"error: the message names {', '.join(by_hand)} in a `{TRAILER}:` trailer of its own; take it out and "
            f"pass {SESSION_FLAG} ID instead, so the id is checked and the trailer written. Nothing was committed."
        )
    missing = not_found(list(dict.fromkeys(given)), root)
    if missing:
        sys.exit(
            "error: a session cited is not one Memar knows, in its folder or on the project's records branch: "
            + "; ".join(missing)
            + f". Check the id with `memar session show --session-id ID --project-path {root}`. Nothing was committed."
        )
    sessions = list(dict.fromkeys([*carried(parent, head, root), *given]))
    if not sessions and not no_session:
        sys.exit(
            f"error: a commit names the sessions it carries out. Pass {SESSION_FLAG} ID once for each, and a "
            f"`{TRAILER}: ID` trailer is written for each into the message; a commit that carries out no session "
            f"(a task that opened none: committing, staging, a rename, one edit) says so with {NO_SESSION_FLAG}. "
            "Nothing was committed."
        )
    return sessions


def with_trailers(message: str, sessions: list[str], root: Path) -> str:
    """MESSAGE with one `Session:` trailer for each of SESSIONS, in its own trailer block."""
    if not sessions:
        return message
    trailers = [argument for session_id in sessions for argument in ("--trailer", f"{TRAILER}: {session_id}")]
    return plumb(
        ["interpret-trailers", "--where", "end", "--if-exists", "addIfDifferent", "--if-missing", "add", *trailers],
        root,
        data=(message + "\n").encode("utf-8"),
    )
