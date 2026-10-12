#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan.py — a session's plan.md: what a plan is, for the services that read and write it.

One format, imported by every service that touches a plan: `session_new` writes
one, `session_find` reads one to list a session, `session_gc` reads one to
decide a sweep. A format known to several files but written in none would be
several parsers for one shape, and a plan listed one way and swept another is
the drift the shared `session_id` exists to avoid for ids.

Why plan.md. A session that stops mid-work leaves a folder, and whoever comes
next — another agent, or the same person tomorrow — needs what was asked and
what comes next without the first session's context. plan.md is that record.
The title is asked for when the plan is first written because an id says only
when a session opened, not what it is about.

One session is one task. When work is finished is disputed for a conversation —
the person may come back, a sub-agent that has reported may be handed more —
but whether one task met its acceptance check is not, so the status sits on the
one task a session holds, and a further task is a session of its own. A plan
used to give each request its own `##` section with its own status; that made
one folder carry several states and the sweep read the session's state off all
of them. Sessions are linked instead: the plan records the session it came from
(`parent`) and the first session of its conversation (`conversation`), written
once, with the plan.

A task can wait for someone to work it: `queued` is a plan written but owned
by no one, which `session_claim` makes one agent's (`open`). It is a status
like the others rather than a mark beside them, so `list --status queued`
finds the waiting tasks and the sweep, which keeps whatever is not done, keeps
them. The status line is rewritten (`set_status`) when a session is queued or
claimed, and nothing else in the plan is touched. Several writers reach one
plan — a claim, a priority, a person editing — so a rewrite is never a read
followed blindly by a write that would put back what another changed
meanwhile: it is checked against the plan as it is just before it lands, and
lands whole (`_rewrite`).

Which waiting task goes first is the plan's `priority`, a whole number from 1
to 10 in its front matter, the higher sooner. It is the plan's own because it
is a fact about the task, read wherever the plan is read — `list`, `claims`,
`digest` — and changed by anyone (`session_priority`), so it is one key
rewritten in place (`set_priority`) like the status line, not a queue kept
somewhere else that could disagree with the plans. A plan that writes none has
the middle value, 5, so every plan written before priorities existed waits as
an ordinary task; a value that is not such a number reads as 5 too, since a
plan is scratch a person edits by hand and one typo must not stop the line.

A plan written in the sectioned form is still read, because folders in that
form still hold unfinished work: a section's status is the `Status:` line under
its heading, before its first part, where that form wrote it, and the plan's is
open when any section is open, else blocked when any is blocked, else the first
status that is not done, and done only when every section is. A plan with no
status there or above its first section has none, and none is not done, so its
folder is kept. Those plans also wrote a status in free text, so a status that
starts with done or complete reads as finished (`is_done`), and any other as
not. That reading lives here and nowhere else, so the folders it covers go
through the sweep like any other and the form can be dropped once none is left.

plan.md is scratch, not a document, and is reaped with its folder: a topic's
lasting open state belongs in that topic's handoff, and closing by type moves
it there, so a plan that outlived its folder would be a second handoff nobody
maintains.
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Callable, NamedTuple

from machine.console import fail

PLAN_NAME = "plan.md"
# queued: planned and owned by no one, waiting to be claimed;
# open: someone is working it; blocked: waiting on someone; done.
STATUSES = ("queued", "open", "blocked", "done")
QUEUED_STATUS = "queued"
OPEN_STATUS = "open"
BLOCKED_STATUS = "blocked"
DONE_STATUS = "done"
# Plans written before the sweep read a status said finished in their own
# words, such as `complete (2026-10-09)`.
FINISHED_PREFIXES = (DONE_STATUS, "complete")
STATUS_PREFIX = "Status:"
PARENT_KEY = "parent"
CONVERSATION_KEY = "conversation"
# Which waiting task goes first: 1 to 10, the higher sooner, 5 when absent.
PRIORITY_KEY = "priority"
LOWEST_PRIORITY = 1
HIGHEST_PRIORITY = 10
DEFAULT_PRIORITY = 5
# The parts every plan carries, in order, under the task's status.
PARTS = ("Request", "Why", "Steps", "Next")
# A rewrite that finds the plan changed under it starts over this many times
# before it gives up, pausing this long when the system refused the replace.
REWRITE_ATTEMPTS = 5
REWRITE_PAUSE_SECONDS = 0.05


class Plan(NamedTuple):
    """What a plan says: its front matter, its status, and the tasks of the earlier sectioned form."""

    front: dict[str, str] | None
    status: str
    tasks: list[tuple[str, str]]


def checked_title(title: str | None, *, required: bool) -> str | None:
    """TITLE stripped, or None when it is blank; refused when REQUIRED and absent.

    A title is one line, because it is a front-matter value and a heading.
    """
    if title is not None:
        if "\n" in title or "\r" in title:
            fail("a title is one line; this one holds a line break")
        title = title.strip() or None
    if title is None and required:
        fail(f"--title is required: say in one line what the task is, for the folder's {PLAN_NAME}")
    return title


def plan_skeleton(
    title: str,
    opened: str,
    project: Path,
    *,
    parent: str | None = None,
    conversation: str | None = None,
    status: str = OPEN_STATUS,
    priority: int | None = None,
) -> str:
    """A new plan.md: front matter, the title as its heading, its status (open unless queued), and the parts.

    PARENT and CONVERSATION are written only for a session opened from another
    one; a session without them is the first of its own conversation. PRIORITY
    is written only when given; absent, the plan reads as `DEFAULT_PRIORITY`.
    """
    front = ["---", f"title: {title}", f"opened: {opened}", f"project: {project}"]
    if parent:
        front.append(f"{PARENT_KEY}: {parent}")
    if conversation:
        front.append(f"{CONVERSATION_KEY}: {conversation}")
    if priority is not None:
        front.append(f"{PRIORITY_KEY}: {priority}")
    body = [f"# {title}", f"{STATUS_PREFIX} {status}"]
    for part in PARTS:
        body += ["", f"## {part}"]
    return "\n".join([*front, "---", *body]) + "\n"


def front_matter(lines: list[str]) -> tuple[dict[str, str] | None, int]:
    """The `key: value` lines between two leading `---` lines, and where the body starts.

    Each line is split at its first `: `; a handful of keys does not need a
    YAML library installed. A key with no value, `key:` alone, is left out.
    A project's preferences file is read by this too (`project_preferences`),
    so the two front matters cannot be read two ways.
    """
    if lines and lines[0].strip() == "---":
        for end in range(1, len(lines)):
            if lines[end].strip() == "---":
                pairs = (line.split(": ", 1) for line in lines[1:end] if ": " in line)
                return {key.strip(): value.strip() for key, value in pairs} or None, end + 1
    return None, 0


def _own_status(body: list[str]) -> str | None:
    """The status line above the first `##` heading, or None when the plan has none there."""
    for line in body:
        if line.startswith("## "):
            return None
        if line.startswith(STATUS_PREFIX):
            return line[len(STATUS_PREFIX):].strip().lower()
    return None


def _sections(body: list[str]) -> list[tuple[str, str]]:
    """Each `##` section of the earlier sectioned form, one task each, with its status as written.

    The status is the first `Status:` line under the heading, before the
    section's first `###` part; a section with no such line has no status,
    which is not open.
    """
    tasks: list[tuple[str, str]] = []
    under_heading = False
    for line in body:
        if line.startswith("## "):
            tasks.append((line[3:].strip(), ""))
            under_heading = True
        elif line.startswith("###"):
            under_heading = False
        elif under_heading and not tasks[-1][1] and line.startswith(STATUS_PREFIX):
            tasks[-1] = (tasks[-1][0], line[len(STATUS_PREFIX):].strip().lower())
    return tasks


def is_done(status: str) -> bool:
    """Whether STATUS says the task is finished: it starts with done or complete, in any case.

    Anything else — open, blocked, a word this file does not know, or none —
    is not finished.
    """
    return status.strip().lower().startswith(FINISHED_PREFIXES)


def sectioned_status(tasks: list[tuple[str, str]]) -> str:
    """The one status a plan of the earlier sectioned form has, read off its tasks; none when it has no task."""
    statuses = [status for _, status in tasks]
    for status in (OPEN_STATUS, BLOCKED_STATUS):
        if status in statuses:
            return status
    if not statuses:
        return ""
    return next((status for status in statuses if not is_done(status)), DONE_STATUS)


def _read_bytes(path: Path) -> bytes:
    """PATH's bytes, trying again when Windows refuses the read for the moment another process replaces the plan."""
    for _ in range(REWRITE_ATTEMPTS):
        try:
            return path.read_bytes()
        except PermissionError:
            time.sleep(REWRITE_PAUSE_SECONDS)
    return path.read_bytes()


def read_plan(path: Path) -> Plan:
    """PATH's front matter, None when absent, its status, and any tasks of the sectioned form.

    A plan's own status is the `Status:` line above its first `##` heading. A
    plan without one is read in the earlier sectioned form, and its status is
    read off its tasks by `sectioned_status`. A status is lowercased as it is
    read, and one outside `STATUSES` is returned as written — the reader reports
    what the file says rather than renaming it; an empty one means the plan has
    none.
    """
    lines = _read_bytes(path).decode("utf-8-sig").splitlines()
    front, start = front_matter(lines)
    body = lines[start:]
    own = _own_status(body)
    if own is not None:
        return Plan(front, own, [])
    tasks = _sections(body)
    return Plan(front, sectioned_status(tasks), tasks)


def _rewrite(path: Path, change: Callable[[list[str]], list[str]]) -> None:
    """Rewrite PATH as CHANGE makes its lines, starting over when another writer changed it meanwhile.

    Each line keeps its newline, so CHANGE keeps every line it does not touch
    as written. The new text is written to a temporary file beside the plan
    and put in its place by `os.replace`, so a reader never sees half a plan;
    just before that, the plan is read again, and when it is no longer what
    CHANGE was given — a claim, a priority, a person's edit landed meanwhile —
    the rewrite starts over from what is there now, so that change is kept
    rather than written over. What is left is the moment between that second
    read and the replace.
    """
    for _ in range(REWRITE_ATTEMPTS):
        # Bytes decoded, not read_text: that would turn CRLF into LF on the way in.
        data = _read_bytes(path)
        text = "".join(change(data.decode("utf-8-sig").splitlines(keepends=True)))
        temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        try:
            with temporary.open("w", encoding="utf-8", newline="") as written:
                written.write(text)
            if _read_bytes(path) == data:
                os.replace(temporary, path)
                return
        except PermissionError:
            # Windows refuses the replace while another process has the plan open.
            time.sleep(REWRITE_PAUSE_SECONDS)
        finally:
            temporary.unlink(missing_ok=True)
    fail(f"{path} kept changing while it was being rewritten, so nothing was written; try again")


def set_status(path: Path, status: str, expected: tuple[str, ...] | None = None) -> None:
    """Rewrite PATH's own `Status:` line to STATUS, keeping every other line and its newlines as written.

    Only a plan with its own status line — above its first `##` heading — has
    one to rewrite; a plan of the earlier sectioned form is refused, since its
    status is read off several sections and no one line says it. With
    EXPECTED, the status is set only while it is still one of those, checked on
    the plan as it is when written (`_rewrite`); otherwise the plan is left as
    it is and the caller refused.
    """

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        for index in range(start, len(lines)):
            line = lines[index]
            if line.startswith("## "):
                break
            if line.startswith(STATUS_PREFIX):
                found = line[len(STATUS_PREFIX):].strip().lower()
                if expected is not None and found not in expected:
                    fail(f"{path} is {found or 'without a status'} now, no longer {' or '.join(expected)}, so it is not set to {status}")
                ending = line[len(line.rstrip("\r\n")):] or "\n"
                return [*lines[:index], f"{STATUS_PREFIX} {status}{ending}", *lines[index + 1:]]
        fail(f"{path} has no Status line above its first part, so its status cannot be set to {status}")

    _rewrite(path, change)


def _whole_priority(value: str) -> int | None:
    """VALUE as a priority, or None when it is not a whole number from 1 to 10."""
    value = value.strip()
    if not value.isdigit():
        return None
    number = int(value)
    return number if LOWEST_PRIORITY <= number <= HIGHEST_PRIORITY else None


def priority_of(front: dict[str, str] | None) -> int:
    """The priority FRONT matter gives its plan: its `priority`, or `DEFAULT_PRIORITY` when absent or not 1 to 10."""
    found = _whole_priority((front or {}).get(PRIORITY_KEY, ""))
    return DEFAULT_PRIORITY if found is None else found


def checked_priority(value: str | int) -> int:
    """VALUE as a priority; refused when it is not a whole number from 1 to 10."""
    found = _whole_priority(str(value))
    if found is None:
        fail(
            f"a priority is a whole number from {LOWEST_PRIORITY} to {HIGHEST_PRIORITY}, the higher sooner; "
            f"{value!r} is not one"
        )
    return found


def set_priority(path: Path, priority: int) -> None:
    """Write PRIORITY as PATH's `priority`, replacing the key or adding it last in the front matter; every other line is kept.

    A plan without front matter has no place for it and is refused.
    """
    priority = checked_priority(priority)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its priority cannot be set")
        ending = lines[0][len(lines[0].rstrip("\r\n")):] or "\n"
        written = f"{PRIORITY_KEY}: {priority}{ending}"
        for index in range(1, start - 1):
            if lines[index].split(":", 1)[0].strip() == PRIORITY_KEY:
                return [*lines[:index], written, *lines[index + 1:]]
        return [*lines[:start - 1], written, *lines[start - 1:]]

    _rewrite(path, change)


def part_text(path: Path, part: str) -> str:
    """What PATH says under its `## PART` heading, up to the next `##`, stripped; empty when it has none."""
    lines = _read_bytes(path).decode("utf-8-sig").splitlines()
    found: list[str] | None = None
    for line in lines:
        if line.startswith("## "):
            if found is not None:
                break
            if line[3:].strip() == part:
                found = []
        elif found is not None:
            found.append(line)
    return "\n".join(found or []).strip()
