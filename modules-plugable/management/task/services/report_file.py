#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/report_file.py — a task's report.md: what a report is, and when it disagrees with the plan.

plan.md says what a task is and where it stands while it is worked; report.md
says how the work on it ended — the Status it reached, what ran, the check
and its result, what is left open. `task_new` writes the skeleton beside
the plan and never overwrites one, and `task_find` reads its Status to mark
a task whose report and plan disagree. One file owns the name, the
skeleton, and the Statuses a report may state, so the task that writes a report and the list that checks it
read it one way.

A report states a Status of the one vocabulary
[Status](../../../modules-plugable/knowledge/documentation/documentation.md#status) defines, held in
`modules/knowledge/status/primitive/status.py`, and no second field for how the run ended: each Status a
report may state says in the type how a run that stated it ended
(`Status.report_ending`). A report whose Status is empty says nothing yet and is not checked; a Status the
table does not give a report cannot be checked either, and is marked as such
rather than guessed.

Only today's shape is read: the Status in the front matter, in PascalCase. A
report written before in another (an `Outcome` key beside the Status, the
outcome in a `Stop:` line under the heading and no front matter, a lower-case
key, the words `open` and `done`) says no Status, and `report_shape_problem`
names it, with the same remedy a plan's gets (`task_plan`): only today's
shape is read, and where it is shown; no conversion is named.

A report is also the hand-back of a task another agent handed out: its
Status, its path, and at most ten lines under `Decisions needed` are all the
delegating side reads, and `task_digest` gathers those lines across
tasks and marks a report that is not such a hand-back. A task with nothing to ask writes no such part, so the skeleton
does not carry one.

A report is scratch, like the plan, and goes with its folder: what lasts of it
is routed by closing by type.
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path
files = import_module('modules-plugable.management.task.services.task_memory')
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
EARLIER_SHAPE_REMEDY = _m_plan_file.EARLIER_SHAPE_REMEDY
EARLIER_STATUS_WORDS = _m_plan_file.EARLIER_STATUS_WORDS
front_key = _m_plan_file.front_key
front_matter = _m_plan_file.front_matter
status_word = _m_plan_file.status_word
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN = _m_record.PLAN
REPORT = _m_record.REPORT
_m_report_key = import_module('modules-plugable.knowledge.documentation.report.primitive.report_key')
ReportKey = _m_report_key.ReportKey
from modules.knowledge.label.services.status_words import statuses, statuses_for, status_keys, status_listing, read_status, status_definitions, STATUS_LABEL, STATUS_WORDS
REPORT_NAME = REPORT.file_name
EARLIER_OUTCOME_KEY = 'Outcome'
EARLIER_STOP_PREFIX = 'Stop:'

def report_skeleton(task: str, title: str | None=None) -> str:
    """A new report.md: front matter naming its task (and the TITLE, when known), its heading, and the four parts.

    TASK is the id of the task the report belongs to, written into the
    record so that a reader finds it inside the document rather than by
    reading the name of the folder the record sits in
    ([Documentation — Report](../../../modules-plugable/knowledge/documentation/report/report.md)).
    The task holds its Status; the report does not repeat it.
    """
    front = ['---', f'{ReportKey.ID.written}: {task}', *([f'{ReportKey.TITLE.written}: {title}'] if title else []), '---']
    return '\n'.join([*front, f'# {REPORT.heading}', '', *(f'## {part}' for part in REPORT.parts)]) + '\n'

def _lines(folder: Path) -> list[str]:
    return files.report_lines(folder)

def _front(lines: list[str]) -> dict[str, str]:
    """The report's front matter, the keys written in PascalCase lowercased so callers ask for `status`; empty without one."""
    front, _ = front_matter(lines)
    return REPORT.current({key.lower(): value for key, value in (front or {}).items() if key == front_key(key)})

def read_report_status(folder: Path) -> str:
    """Status still written in an old-shape report.md front matter, if any; empty for a new-shape report and when none.

    A task's lifecycle Status is the task's fact, not the report's. This
    reader remains only so old-shape records and shape checks can see a
    Status line left in an earlier report.md; Complete and Depends_on do
    not use it.
    """
    return status_word(_front(_lines(folder)).get('status', ''))

def report_shape_problem(folder: Path) -> str | None:
    """Why FOLDER's report is in an earlier shape, with where today's is shown; None when it is not, or there is none."""
    lines = _lines(folder)
    front, start = front_matter(lines)
    found = []
    if any((line.startswith(EARLIER_STOP_PREFIX) for line in lines[start:])):
        found.append('a `Stop:` line')
    if front is not None:
        if EARLIER_OUTCOME_KEY in front or EARLIER_OUTCOME_KEY.lower() in front:
            found.append('an `Outcome` key')
        if any((key != front_key(key) and key.lower() in {report_key.key for report_key in REPORT.keys} for key in front)):
            found.append('keys in lower case')
        if status_word(front.get('Status', '')) in EARLIER_STATUS_WORDS:
            found.append(f'the status word {status_word(front["Status"])}')
    if not found:
        return None
    return f"{REPORT_NAME} is in an earlier shape ({'; '.join(found)}); {EARLIER_SHAPE_REMEDY}"

def disagreement(status: str, report_status: str='') -> str | None:
    """Why STATUS, the task's, is not a Status a task may take; None when it is fine or empty.

    A report does not carry Status; REPORT_STATUS is ignored. An empty status
    checks nothing.
    """
    status = status_word(status)
    if status and status not in status_keys(PLAN.kind):
        return f"status {status} is not one of {', '.join(status_keys(PLAN.kind))}"
    return None

def report_part(folder: Path, heading: str) -> list[str]:
    """The non-blank lines under FOLDER's report's `## HEADING` heading, as written; none without one."""
    found: list[str] | None = None
    for line in _lines(folder):
        if line.startswith('#'):
            if found is not None:
                break
            if line.lstrip('#').strip().lower() == heading.lower():
                found = []
        elif found is not None and line.strip():
            found.append(line.rstrip())
    return found or []

def decisions_needed(folder: Path) -> list[str]:
    """The non-blank lines under FOLDER's report's `## Decisions needed` heading, as written; none without one."""
    return report_part(folder, REPORT.hand_back_part)

def handback_problem(folder: Path, status: str) -> str | None:
    """Why FOLDER's report is not a hand-back; None when it is one.

    A hand-back is a report whose shape is today's, with at most
    `REPORT.hand_back_max_lines` lines under its hand-back part: what the
    delegating side reads is the task's Status, the report's path, and those
    lines, so a longer one would carry the task's context back into the
    reader's. STATUS is the task's Status and is not compared to a report field.
    """
    shape = report_shape_problem(folder)
    if shape:
        return shape
    if not _lines(folder):
        return f'{files.report_path(folder).name} is missing'
    count = len(decisions_needed(folder))
    if count > REPORT.hand_back_max_lines:
        return f'{count} lines under {REPORT.hand_back_part}, more than {REPORT.hand_back_max_lines}'
    return None
