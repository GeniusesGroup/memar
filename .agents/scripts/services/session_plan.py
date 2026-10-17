#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan.py — a session's plan.md: what a plan is and how it is read, for the services that read and write it.

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
by no one, which `session_claim` makes one agent's (`active`). It is a status
like the others rather than a mark beside them, so `list --status queued`
finds the waiting tasks and the sweep, which keeps whatever is not complete, keeps
them. The status line is rewritten (`set_status`) when a session is queued or
claimed, and nothing else in the plan is touched. Several writers reach one
plan — a claim, a priority, a person editing — so a rewrite is never a read
followed blindly by a write that would put back what another changed
meanwhile: it is checked against the plan as it is just before it lands, and
lands whole (`session_plan_rewrite`).

Which waiting task goes first is the plan's `priority` (`services/priority.py`
declares what it is). It is the plan's own because it is a fact about the task,
read wherever the plan is read — `list`, `claims`, `digest` — and changed by
anyone (`session_priority`), so it is one key rewritten in place
(`set_priority`) like the status line, not a queue kept somewhere else that
could disagree with the plans.

What a waiting task is about is the plan's `topic` (`services/topic.py`
declares what it is), one subject in its front matter, so that `claims` can
give one agent the tasks of one subject and keep its context on it. It is one
key rewritten in place (`set_topic`), like the priority.

One Status vocabulary serves every Memar document (modules/content/documentation/documentation.md,
section Status), declared once in `services/status.py`; the Statuses a plan may
take are those of `PLAN.statuses` (`services/session_record.py`), and its
Status is written in the front matter beside PascalCase keys. Only that
shape is read. A plan written before in another (a lower-case key, a `Status:`
line in the body, the words `open` and `done`, the sectioned form) is not read
as a plan, and is not rewritten by any writer here: `plan_shape_problem`
names it, and says that only today's shape is read and where it is shown.
It names no conversion: a one-time migration lives in the session that does
the change, never here (.agents/scripts/README.md), so the core does not point
at one that is gone once its work is done, and a plan left in an earlier shape
is rewritten by whoever keeps it.

plan.md is scratch, not a document, and is reaped with its folder: a topic's
lasting open state belongs in that topic's handoff, and closing by type moves
it there, so a plan that outlived its folder would be a second handoff nobody
maintains.

A plan is changed one front-matter field at a time, each field in a file of its own beside this one:
`session_plan_status`, `session_plan_priority`, `session_plan_topic` and `session_plan_kind`, each
with its field's words and checks, over `session_plan_rewrite`, the one way a plan's lines are
replaced. This file holds what they and every reader share: the shape, the front matter, and the
reading.
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import NamedTuple

from machine.console import fail
from services.session_record import PLAN, PlanKey
from services.status import Status

# The plan's shape and the Status vocabulary it draws on are declared once, in
# `session_record` and `status`; the name is derived from them, not repeated.
PLAN_NAME = PLAN.file_name
# What the message for a plan or a report in an earlier shape says to do: the
# shape is not converted here, and `memar session new --help` shows today's.
EARLIER_SHAPE_REMEDY = "only today's shape is read, which `memar session new --help` shows; rewrite it in that shape"
# What marks an earlier shape, so it can be named: the words a status was
# written in, and the body line that held it.
EARLIER_STATUS_WORDS = ("open", "done")
STATUS_PREFIX = f"{PlanKey.STATUS.written}:"
# A read that finds the plan refused for the moment tries again this many times, pausing this
# long (`session_plan_rewrite` uses the same for its replace).
REWRITE_ATTEMPTS = 5
REWRITE_PAUSE_SECONDS = 0.05


class Plan(NamedTuple):
    """What a plan says: its front matter and its status."""

    front: dict[str, str] | None
    status: str


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


def status_word(word: str) -> str:
    """WORD as a status is compared: stripped and lower case; any word, the old ones too, as written."""
    return word.strip().lower()


def front_key(key: str) -> str:
    """KEY as the front matter writes it: PascalCase, which for the one-word keys of a plan is a capital."""
    return key.capitalize()


def plan_skeleton(
    session: str,
    title: str,
    opened: str,
    project: Path,
    *,
    parent: str | None = None,
    conversation: str | None = None,
    status: str = Status.ACTIVE.key,
    priority: int | None = None,
    topic: str | None = None,
    kind: str | None = None,
    depends_on: str | None = None,
) -> str:
    """A new plan.md: front matter naming its session and carrying its status (active unless queued), the title as its heading, and the parts.

    SESSION is the id of the session the plan belongs to, written into the
    record so that a reader finds it inside the document rather than by
    reading the name of the folder the record sits in
    ([Documentation — Plan](../../../modules/content/documentation/plan/plan.md)).
    PARENT and CONVERSATION are written only for a session opened from another
    one; a session without them is the first of its own conversation. PRIORITY
    is written only when given; absent, the plan reads as `Priority.DEFAULT`.
    TOPIC is written only when it is not empty, as given: the caller has
    checked it (`Topic.checked`). KIND is written only when given, checked
    (`checked_kind`). DEPENDS_ON is written only when given, as the text of
    the type that checked it (`services/depends_on.py`).
    """
    given = {
        PlanKey.SESSION: session,
        PlanKey.TITLE: title,
        PlanKey.STATUS: status_word(status).capitalize(),
        PlanKey.OPENED: opened,
        PlanKey.PROJECT: project,
        PlanKey.PARENT: parent,
        PlanKey.CONVERSATION: conversation,
        PlanKey.PRIORITY: priority,
        PlanKey.TOPIC: topic,
        PlanKey.KIND: kind,
        PlanKey.DEPENDS_ON: depends_on,
    }
    # Keys in the record's order; an optional key with no value is not written.
    front = ["---", *(f"{key.written}: {given[key]}" for key in PLAN.keys if given[key] not in (None, ""))]
    body = [f"# {title}"]
    for part in PLAN.parts:
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


def is_complete(status: str) -> bool:
    """Whether STATUS says the task is finished: the word complete, in any case, and no other."""
    return Status.read(status) is Status.COMPLETE


def read_bytes(path: Path) -> bytes:
    """PATH's bytes, trying again when Windows refuses the read for the moment another process replaces the plan."""
    for _ in range(REWRITE_ATTEMPTS):
        try:
            return path.read_bytes()
        except PermissionError:
            time.sleep(REWRITE_PAUSE_SECONDS)
    return path.read_bytes()


def read_plan(path: Path) -> Plan:
    """PATH's front matter, None when absent, and its status; an empty status means the plan has none.

    Only today's shape is read. The front matter's keys are those written in
    PascalCase (`Title`), lowercased as they are read so callers ask for
    `title`; a key written otherwise is not read. A plan's status is the front
    matter's `Status`, lowercased, and one no session plan may take is returned as
    written; nothing else gives a plan a status. A plan in an earlier shape
    reads as one with no status, and `plan_shape_problem` says why.
    """
    lines = read_bytes(path).decode("utf-8-sig").splitlines()
    front, _ = front_matter(lines)
    if front is not None:
        front = {key.lower(): value for key, value in front.items() if key == front_key(key)}
    return Plan(front, status_word((front or {}).get(PlanKey.STATUS.key, "")))


def plan_shape_problem(lines: list[str]) -> str | None:
    """Why the plan LINES are in an earlier shape, with where today's is shown; None when they are not, or have no front matter.

    An earlier shape has a key in lower case, a status written as `open` or
    `done`, or its status in a body `Status:` line above the first `##`
    heading with none in the front matter.
    """
    front, start = front_matter(lines)
    if front is None:
        return None
    found = []
    if any(key != front_key(key) and key.lower() in {plan_key.key for plan_key in PLAN.keys} for key in front):
        found.append("keys in lower case")
    status = front.get(PlanKey.STATUS.written, "")
    if status_word(status) in EARLIER_STATUS_WORDS:
        found.append(f"the status word {status_word(status)}")
    if not status:
        for line in lines[start:]:
            if line.startswith("## "):
                break
            if line.startswith(STATUS_PREFIX):
                found.append("its status in a body `Status:` line")
                break
    if not found:
        return None
    return f"its plan is in an earlier shape ({'; '.join(found)}); {EARLIER_SHAPE_REMEDY}"


def plan_file_problem(path: Path) -> str | None:
    """`plan_shape_problem` of the plan at PATH; None when it is not in an earlier shape or cannot be read."""
    try:
        return plan_shape_problem(read_bytes(path).decode("utf-8-sig").splitlines())
    except (OSError, UnicodeDecodeError):
        return None


def part_text(path: Path, part: str) -> str:
    """What PATH says under its `## PART` heading, up to the next `##`, stripped; empty when it has none."""
    lines = read_bytes(path).decode("utf-8-sig").splitlines()
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
