#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/plan/services/plan.py — a task's plan.md: what a plan is and how it is read, for the services that read and write it.

One format, imported by every service that touches a plan: `task_new` writes
one, `task_find` reads one to list a task, `task_gc` reads one to
decide a sweep. A format known to several files but written in none would be
several parsers for one shape, and a plan listed one way and swept another is
the drift the shared `task_id` exists to avoid for ids.

Why plan.md. A task that stops mid-work leaves a folder, and whoever comes
next — another agent, or the same person tomorrow — needs what was asked and
what comes next without the first task's context. plan.md is that record.
The title is asked for when the plan is first written because an id says only
when a task opened, not what it is about.

One task is one task. When work is finished is disputed for a conversation —
the person may come back, a sub-agent that has reported may be handed more —
but whether one task met its acceptance check is not, so the status sits on the
one task a task holds, and a further task is a task of its own. A plan
used to give each request its own `##` section with its own status; that made
one folder carry several states and the sweep read the task's state off all
of them. Tasks are linked instead: the plan records the task it came from
(`parent`) and the first task of its conversation (`conversation`), written
once, with the plan.

A task can wait for someone to work it: `queued` is a plan written but owned
by no one, which `task_claim` makes one agent's (`active`). It is a status
like the others rather than a mark beside them, so `list --status queued`
finds the waiting tasks and the sweep, which keeps whatever is not complete, keeps
them. The status line is rewritten (`set_status`) when a task is queued or
claimed, and nothing else in the plan is touched. Several writers reach one
plan — a claim, a priority, a person editing — so a rewrite is never a read
followed blindly by a write that would put back what another changed
meanwhile: it is checked against the plan as it is just before it lands, and
lands whole (`task_plan_rewrite`).

Which waiting task goes first is the plan's `priority` (`modules/knowledge/documentation/plan/primitive/priority.py`
declares what it is). It is the plan's own because it is a fact about the task,
read wherever the plan is read — `list`, `claims`, `digest` — and changed by
anyone (`task_priority`), so it is one key rewritten in place
(`set_priority`) like the status line, not a queue kept somewhere else that
could disagree with the plans.

What a waiting task is about, and what act it is, are the plan's `labels`
(`modules/knowledge/documentation/primitive/label.py` declares what a label is;
`modules/knowledge/documentation/plan/labels/topic.py` and `modules/knowledge/documentation/plan/labels/task_kind.py` declare the kinds the plan
carries): as many as the task needs, one `- Kind: word` line each in a block
under the key, so that `claims` can give one agent the tasks of one topic and
keep its context on it. A label is added or removed by one line
(`task_plan_labels`), like the priority is rewritten in place.

One Status vocabulary serves every Memar document (modules/knowledge/documentation/documentation.md,
section Status), declared once in `modules/knowledge/documentation/primitive/status.py`; the Statuses a plan may
take are those of `PLAN.statuses` (`modules/knowledge/documentation/record.py`), and its
Status is written in the front matter beside PascalCase keys. Only that
shape is read. A plan written before in another (a lower-case key, a `Status:`
line in the body, the words `open` and `done`, the sectioned form) is not read
as a plan, and is not rewritten by any writer here: `plan_shape_problem`
names it, and says that only today's shape is read and where it is shown.
It names no conversion: a one-time migration lives in the task that does
the change, never here (the task that does the change, in its `services/` folder), so the core does not point
at one that is gone once its work is done, and a plan left in an earlier shape
is rewritten by whoever keeps it.

plan.md is scratch, not a document, and is reaped with its folder: a topic's
lasting open state belongs in that topic's handoff, and closing by type moves
it there, so a plan that outlived its folder would be a second handoff nobody
maintains.

A plan is changed one front-matter field at a time, each field in a file of its own beside this one:
`task_plan_status`, `task_plan_priority` and `task_plan_labels`, each
with its field's words and checks, over `task_plan_rewrite`, the one way a plan's lines are
replaced. This file holds what they and every reader share: the shape, the front matter, and the
reading.
"""
from __future__ import annotations
import time
from pathlib import Path
from typing import NamedTuple
from machine.console import fail
from modules.knowledge.documentation.record import PLAN, REPORT
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.label import Labels
from modules.knowledge.documentation.primitive.status import Status
PLAN_NAME = PLAN.file_name
EARLIER_SHAPE_REMEDY = "only today's shape is read, which `memar task ensure --help` shows; rewrite it in that shape"
EARLIER_STATUS_WORDS = ('open', 'done')
EARLIER_LABEL_KEYS = ('topic', 'kind')
STATUS_PREFIX = f'{PlanKey.STATUS.written}:'
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
        if '\n' in title or '\r' in title:
            fail('a title is one line; this one holds a line break')
        title = title.strip() or None
    if title is None and required:
        fail(f"--title is required: say in one line what the task is, for the folder's {PLAN_NAME}")
    return title

def status_word(word: str) -> str:
    """WORD as a status is compared: stripped and lower case; any word, the old ones too, as written."""
    return word.strip().lower()
WRITTEN = {key.key: key.written for key in (*PLAN.keys, *REPORT.keys)}

def front_key(key: str) -> str:
    """KEY as the front matter writes it: the written form a record's key declares (`ID`, `Start Date`), else PascalCase, a capital for a one-word key."""
    return WRITTEN.get(key.lower(), key.capitalize())

def plan_skeleton(task: str, title: str, opened: str, project: Path, *, parent: str | None=None, conversation: str | None=None, status: str=Status.ACTIVE.key, priority: int | None=None, labels: Labels | None=None, depends_on: str | None=None) -> str:
    """A new plan.md: front matter naming its task and carrying its status (active unless queued), the title as its heading, and the parts.

    TASK is the id of the task the plan belongs to, written into the
    record as its `ID` so that a reader finds it inside the document rather
    than by reading the name of the folder the record sits in
    ([Documentation — Plan](../../../modules/knowledge/documentation/plan/plan.md)).
    PARENT and CONVERSATION are written only for a task opened from another
    one; a task without them is the first of its own conversation. PRIORITY
    is written only when given; absent, the plan reads as `Priority.DEFAULT`.
    LABELS is written as a block only when it holds a label: the caller has
    checked each against its kind (`task_plan_labels`). DEPENDS_ON is written only when given, as the text of
    the type that checked it (`modules/management/task/services/dependency.py`).
    """
    given = {PlanKey.ID: task, PlanKey.TITLE: title, PlanKey.STATUS: status_word(status).capitalize(), PlanKey.START_DATE: opened, PlanKey.PROJECT: project, PlanKey.PARENT: parent, PlanKey.CONVERSATION: conversation, PlanKey.PRIORITY: priority, PlanKey.LABELS: labels, PlanKey.DEPENDS_ON: depends_on}
    front = ['---']
    for key in PLAN.keys:
        if key is PlanKey.LABELS:
            if given[key]:
                front += [f'{key.written}:', *given[key].lines()]
        elif given[key] not in (None, ''):
            front.append(f'{key.written}: {given[key]}')
    body = [f'# {title}']
    for part in PLAN.parts:
        body += ['', f'## {part}']
    return '\n'.join([*front, '---', *body]) + '\n'

def front_matter(lines: list[str]) -> tuple[dict[str, str] | None, int]:
    """The `key: value` lines between two leading `---` lines, and where the body starts.

    Each line is split at its first `: `; a handful of keys does not need a
    YAML library installed. A key with no value, `key:` alone, is left out,
    unless indented lines follow it: those are its block (`Labels:`, then one
    `  - Kind: word` line a label), and its value is their text, one per line,
    each without its `- `.
    """
    if lines and lines[0].strip() == '---':
        for end in range(1, len(lines)):
            if lines[end].strip() == '---':
                return (_front_pairs(lines[1:end]) or None, end + 1)
    return (None, 0)

def _front_pairs(lines: list[str]) -> dict[str, str]:
    """The `key: value` pairs of the front matter LINES, an indented line joining the block of the key above it."""
    found: dict[str, str] = {}
    current: str | None = None
    for line in lines:
        if line[:1] in (' ', '\t') and current is not None:
            child = line.strip()
            child = child[2:] if child.startswith('- ') else child
            if child:
                found[current] = f'{found[current]}\n{child}' if found[current] else child
        elif ': ' in line:
            key, value = line.split(': ', 1)
            current = key.strip()
            found[current] = value.strip()
        elif line.rstrip().endswith(':') and line.strip() != ':':
            current = line.rstrip()[:-1].strip()
            found[current] = ''
        else:
            current = None
    return {key: value for key, value in found.items() if value}

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
    `title`; a key written otherwise is not read. A key an earlier name still
    carries (`Opened` for `Start Date`, `Task` for `ID`) is read as the key. A plan's status is the front
    matter's `Status`, lowercased, and one no task plan may take is returned as
    written; nothing else gives a plan a status. A plan in an earlier shape
    reads as one with no status, and `plan_shape_problem` says why.
    """
    lines = read_bytes(path).decode('utf-8-sig').splitlines()
    front, _ = front_matter(lines)
    if front is not None:
        front = PLAN.current({key.lower(): value for key, value in front.items() if key == front_key(key)})
    return Plan(front, status_word((front or {}).get(PlanKey.STATUS.key, '')))

def plan_shape_problem(lines: list[str]) -> str | None:
    """Why the plan LINES are in an earlier shape, with where today's is shown; None when they are not, or have no front matter.

    An earlier shape has a key in lower case, a status written as `open` or
    `done`, a `Topic` or `Kind` key (both are labels now, under `Labels`), or
    its status in a body `Status:` line above the first `##` heading with none
    in the front matter.
    """
    front, start = front_matter(lines)
    if front is None:
        return None
    found = []
    if any((key != front_key(key) and key.lower() in {plan_key.key for plan_key in PLAN.keys} for key in front)):
        found.append('keys in lower case')
    if any((key.lower() in EARLIER_LABEL_KEYS for key in front)):
        found.append(f"the keys {' and '.join((key.capitalize() for key in EARLIER_LABEL_KEYS))}, which are labels now")
    status = front.get(PlanKey.STATUS.written, '')
    if status_word(status) in EARLIER_STATUS_WORDS:
        found.append(f'the status word {status_word(status)}')
    if not status:
        for line in lines[start:]:
            if line.startswith('## '):
                break
            if line.startswith(STATUS_PREFIX):
                found.append('its status in a body `Status:` line')
                break
    if not found:
        return None
    return f"its plan is in an earlier shape ({'; '.join(found)}); {EARLIER_SHAPE_REMEDY}"

def plan_file_problem(path: Path) -> str | None:
    """`plan_shape_problem` of the plan at PATH; None when it is not in an earlier shape or cannot be read."""
    try:
        return plan_shape_problem(read_bytes(path).decode('utf-8-sig').splitlines())
    except (OSError, UnicodeDecodeError):
        return None

def part_text(path: Path, part: str) -> str:
    """What PATH says under its `## PART` heading, up to the next `##`, stripped; empty when it has none."""
    lines = read_bytes(path).decode('utf-8-sig').splitlines()
    found: list[str] | None = None
    for line in lines:
        if line.startswith('## '):
            if found is not None:
                break
            if line[3:].strip() == part:
                found = []
        elif found is not None:
            found.append(line)
    return '\n'.join(found or []).strip()
