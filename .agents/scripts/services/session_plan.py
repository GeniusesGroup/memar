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
by no one, which `session_claim` makes one agent's (`active`). It is a status
like the others rather than a mark beside them, so `list --status queued`
finds the waiting tasks and the sweep, which keeps whatever is not complete, keeps
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

What a waiting task is about is the plan's `topic`, one subject in its front
matter, so that `claims` can give one agent the tasks of one subject and keep
its context on it. One value, not several: a task with two subjects is two
tasks, and one value keeps "the same topic" a plain equality. It is free text
normalized when written (`normalized_topic`: lower case, runs of white space as
one hyphen), not a list the project keeps, because a kept list is a second
thing to maintain and would stop a new subject at the moment it appears; a typo
that splits one subject in two is met by showing the topics in use and by
warning of a near match (`session_topic`). A plan without one has none, and
none is not a topic of its own. It is one key rewritten in place
(`set_topic`), like the priority.

One Status vocabulary serves every Memar document (docs/documentation.md,
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
"""
from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Callable, NamedTuple

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
STATUS_PREFIX = "Status:"
# Which waiting task goes first: 1 to 10, the higher sooner, 5 when absent.
LOWEST_PRIORITY = 1
HIGHEST_PRIORITY = 10
DEFAULT_PRIORITY = 5
# What kind of task a plan holds, which says how strong a model it needs: the
# kinds whose work is judgment run on the strongest model the runtime offers
# (the Memar skill, section Session and plan), the others on a cheaper one.
STRONG_KINDS = ("ideation", "plan", "modeling", "design", "critique")
CHEAPER_KINDS = ("mechanical",)
KINDS = (*STRONG_KINDS, *CHEAPER_KINDS)
# A rewrite that finds the plan changed under it starts over this many times
# before it gives up, pausing this long when the system refused the replace.
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
) -> str:
    """A new plan.md: front matter with its status (active unless queued), the title as its heading, and the parts.

    PARENT and CONVERSATION are written only for a session opened from another
    one; a session without them is the first of its own conversation. PRIORITY
    is written only when given; absent, the plan reads as `DEFAULT_PRIORITY`.
    TOPIC is written only when it is not empty, as given: the caller has
    checked it (`checked_topic`). KIND is written only when given, checked
    (`checked_kind`).
    """
    given = {
        PlanKey.TITLE: title,
        PlanKey.STATUS: status_word(status).capitalize(),
        PlanKey.OPENED: opened,
        PlanKey.PROJECT: project,
        PlanKey.PARENT: parent,
        PlanKey.CONVERSATION: conversation,
        PlanKey.PRIORITY: priority,
        PlanKey.TOPIC: topic,
        PlanKey.KIND: kind,
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


def _read_bytes(path: Path) -> bytes:
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
    lines = _read_bytes(path).decode("utf-8-sig").splitlines()
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
        return plan_shape_problem(_read_bytes(path).decode("utf-8-sig").splitlines())
    except (OSError, UnicodeDecodeError):
        return None


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
        lines = data.decode("utf-8-sig").splitlines(keepends=True)
        problem = plan_shape_problem([line.rstrip("\r\n") for line in lines])
        if problem:
            fail(f"{path}: {problem}; nothing was written")
        text = "".join(change(lines))
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


def _key_of(line: str) -> str:
    """The key a front-matter LINE sets, as written; empty when the line sets none."""
    key, colon, _ = line.partition(":")
    return key.strip() if colon else ""


def _end(line: str) -> str:
    """LINE's line ending, a newline when it has none."""
    return line[len(line.rstrip("\r\n")):] or "\n"


def set_status(path: Path, status: str, expected: tuple[str, ...] | None = None) -> None:
    """Set PATH's front matter Status to STATUS, keeping every other line and its newlines as written.

    A plan in an earlier shape is refused (`_rewrite`), and so is one with no
    front matter, which has nowhere to keep a status. A plan with front matter
    and no Status is given one, last. With EXPECTED, the status is set only
    while it is still one of those, checked on the plan as it is when written
    (`_rewrite`); otherwise the plan is left as it is and the caller refused.
    STATUS and EXPECTED are statuses a session plan may take (`PLAN.statuses`); any other word is refused.
    """
    status = status_word(status)
    wanted = None if expected is None else tuple(status_word(word) for word in expected)
    for word in (status, *(wanted or ())):
        if word not in Status.keys(PLAN.kind):
            fail(f"{word!r} is not a status; the statuses are {', '.join(Status.keys(PLAN.kind))}")

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its status cannot be set to {status}")
        written = f"{PlanKey.STATUS.written}: {status.capitalize()}"
        for index in range(1, start - 1):
            if _key_of(lines[index]) == PlanKey.STATUS.written:
                found = status_word(lines[index].partition(":")[2])
                if wanted is not None and found not in wanted:
                    fail(f"{path} is {found or 'without a status'} now, no longer {' or '.join(expected)}, so it is not set to {status}")
                return [*lines[:index], written + _end(lines[index]), *lines[index + 1:]]
        if wanted is not None:
            fail(f"{path} is without a status now, no longer {' or '.join(expected)}, so it is not set to {status}")
        return [*lines[:start - 1], written + _end(lines[0]), *lines[start - 1:]]

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
    found = _whole_priority((front or {}).get(PlanKey.PRIORITY.key, ""))
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
        written = f"{PlanKey.PRIORITY.written}: {priority}{_end(lines[0])}"
        for index in range(1, start - 1):
            if _key_of(lines[index]) == PlanKey.PRIORITY.written:
                return [*lines[:index], written, *lines[index + 1:]]
        return [*lines[:start - 1], written, *lines[start - 1:]]

    _rewrite(path, change)


def normalized_topic(text: str) -> str:
    """TEXT as a topic: stripped, lower case, each run of white space one hyphen; empty when nothing is left."""
    return "-".join(text.lower().split())


def checked_topic(text: str) -> str:
    """TEXT as a topic, normalized; refused when it holds a line break, since a topic is a one-line front-matter value."""
    if "\n" in text or "\r" in text:
        fail("a topic is one line; this one holds a line break")
    return normalized_topic(text)


def topic_of(front: dict[str, str] | None) -> str:
    """The topic FRONT matter gives its plan, normalized; empty when it has none."""
    return normalized_topic((front or {}).get(PlanKey.TOPIC.key, ""))


def set_topic(path: Path, topic: str) -> None:
    """Write TOPIC as PATH's `topic`, replacing the key or adding it last in the front matter; empty removes the key.

    Every other line is kept. A plan without front matter has no place for it
    and is refused. TOPIC is normalized here, so the plan never holds another
    form.
    """
    topic = checked_topic(topic)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its topic cannot be set")
        written = [f"{PlanKey.TOPIC.written}: {topic}{_end(lines[0])}"] if topic else []
        for index in range(1, start - 1):
            if _key_of(lines[index]) == PlanKey.TOPIC.written:
                return [*lines[:index], *written, *lines[index + 1:]]
        return [*lines[:start - 1], *written, *lines[start - 1:]]

    _rewrite(path, change)


def checked_kind(text: str) -> str:
    """TEXT as a kind, lower case; refused when it is not one of `KINDS`, so a misspelt kind never reads as a cheaper one."""
    kind = text.strip().lower()
    if kind not in KINDS:
        fail(f"a kind is one of {', '.join(KINDS)}; {text!r} is not one")
    return kind


def kind_of(front: dict[str, str] | None) -> str:
    """The kind FRONT matter gives its plan, lower case as written; empty when it has none. It is not checked: a plan is edited by hand."""
    return (front or {}).get(PlanKey.KIND.key, "").strip().lower()


def set_kind(path: Path, kind: str) -> None:
    """Write KIND as PATH's `kind`, replacing the key or adding it last in the front matter; every other line is kept."""
    kind = checked_kind(kind)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its kind cannot be set")
        written = f"{PlanKey.KIND.written}: {kind}{_end(lines[0])}"
        for index in range(1, start - 1):
            if _key_of(lines[index]) == PlanKey.KIND.written:
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
