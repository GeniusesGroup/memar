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

from pathlib import Path
from typing import NamedTuple

from machine.console import fail

PLAN_NAME = "plan.md"
STATUSES = ("open", "blocked", "done")
OPEN_STATUS = "open"
BLOCKED_STATUS = "blocked"
DONE_STATUS = "done"
# Plans written before the sweep read a status said finished in their own
# words, such as `complete (2026-10-09)`.
FINISHED_PREFIXES = (DONE_STATUS, "complete")
STATUS_PREFIX = "Status:"
PARENT_KEY = "parent"
CONVERSATION_KEY = "conversation"
# The parts every plan carries, in order, under the task's status.
PARTS = ("Request", "Steps", "Next")


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
) -> str:
    """A new plan.md: front matter, the title as its heading, an open status, and the three parts.

    PARENT and CONVERSATION are written only for a session opened from another
    one; a session without them is the first of its own conversation.
    """
    front = ["---", f"title: {title}", f"opened: {opened}", f"project: {project}"]
    if parent:
        front.append(f"{PARENT_KEY}: {parent}")
    if conversation:
        front.append(f"{CONVERSATION_KEY}: {conversation}")
    body = [f"# {title}", f"{STATUS_PREFIX} {OPEN_STATUS}"]
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


def read_plan(path: Path) -> Plan:
    """PATH's front matter, None when absent, its status, and any tasks of the sectioned form.

    A plan's own status is the `Status:` line above its first `##` heading. A
    plan without one is read in the earlier sectioned form, and its status is
    read off its tasks by `sectioned_status`. A status is lowercased as it is
    read, and one outside `STATUSES` is returned as written — the reader reports
    what the file says rather than renaming it; an empty one means the plan has
    none.
    """
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    front, start = front_matter(lines)
    body = lines[start:]
    own = _own_status(body)
    if own is not None:
        return Plan(front, own, [])
    tasks = _sections(body)
    return Plan(front, sectioned_status(tasks), tasks)
