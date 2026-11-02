#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from modules.identity.thing.labels.Label_Queued import Label_Queued
from importlib import import_module
import argparse
import re
from datetime import date
from pathlib import Path
from typing import Callable
from machine.console import note
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
REPORT = _m_record.REPORT
from modules.knowledge.label.services.status_words import statuses, statuses_for, status_keys, status_listing, read_status, status_definitions, STATUS_LABEL, STATUS_WORDS
_m_content_questions = import_module('modules-plugable.knowledge.documentation.services.content_questions')
BLOCKING_MARK = _m_content_questions.BLOCKING_MARK
open_questions = _m_content_questions.open_questions
_m_contents = import_module('modules-plugable.knowledge.documentation.services.contents_of_tasks')
contents_of_tasks = _m_contents.contents_of_tasks
from modules.knowledge.content.services.reference import content_root
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
Reader = _m_dependency.Reader
_m_concerns = import_module('modules-plugable.management.task.services.concerns')
concerns = _m_concerns.concerns
_m_depends = import_module('modules-plugable.management.task.services.depends')
concerns_for = _m_depends.concerns_for
reconcile_all = _m_depends.reconcile_all
_m_day = import_module('modules-plugable.management.task.services.day')
DAY_NAMES = _m_day.DAY_NAMES
day_of = _m_day.day_of
parse_day = _m_day.parse_day
from modules.computer.software.services.project_find import add_project_flags, project_from_args
_m_list = import_module('modules-plugable.management.task.services.list')
find_tasks = _m_list.find_tasks
project_of = _m_list.project_of
_m_folder = import_module('modules-plugable.management.task.services.folder')
Task = _m_folder.Task
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
_m_task_files = import_module('modules-plugable.management.task.services.task_memory')
report_path = _m_task_files.report_path
decisions_needed = _m_report_file.decisions_needed
handback_problem = _m_report_file.handback_problem
_m_report_summary = import_module('modules-plugable.management.task.services.report_summary')
summary_lines = _m_report_summary.summary_lines
from modules.computer.software.primitive.project_name import ProjectName
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
OPEN_HEADING = 'Open questions'
DECISION_KIND = 'decision'
DIGEST_COMMAND = 'get-decisions-digest'
_POINTER = re.compile(r'\b(\d{8}-?T\d{6}Z[\w-]*)#(\d+)')
_FIELD = re.compile(r'^\s*-\s+\*{0,2}(Decided|Confidence|Reason)\*{0,2}\s*:\s*(.*)$', re.I)
CLOSE_LINE = 'close, once the owner confirms it is finished: memar git trash-task-folder --task-id'

def decision_lines(content) -> list[str]:
    found = {}
    for line in content.body.splitlines():
        match = _FIELD.match(line)
        if match:
            found.setdefault(match.group(1).lower(), match.group(2).strip())
    return [('decision' if name == 'decided' else name) + f': {found[name]}' for name in ('decided', 'confidence', 'reason') if name in found]

def decisions_by_task(contents: list) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for task_id, content in contents:
        if content.header.get('kind') == DECISION_KIND:
            found.setdefault(task_id, []).extend(decision_lines(content))
    return found

def pointer_problem(lines: list[str], open_keys: set[str]) -> str | None:
    for line in lines:
        for match in _POINTER.finditer(line):
            key = f'{match.group(1)}#{match.group(2)}'
            if key not in open_keys:
                return f'{REPORT.hand_back_part} points to {key}, which holds no open question'
    return None

def points_to(lines: list[str], task_id: str, number: int) -> bool:
    key = f'{task_id}#{number}'
    return any((key in text for text in lines))

def print_open_questions(entries: list, decisions: list[str], wanted: date | None) -> int:
    shown_entries = [entry for entry in entries if (wanted is None or entry[4] == wanted.isoformat()) and (not points_to(decisions, entry[0], entry[1]))]
    if not shown_entries:
        return 0
    print()
    print(f"{OPEN_HEADING} — {len(shown_entries)} {('entry' if len(shown_entries) == 1 else 'entries')}")
    for task_id, number, heading, blocking, _ in shown_entries:
        note(f'{task_id}#{number}: {heading}' + (f' {BLOCKING_MARK}' if blocking else ''))
    return len(shown_entries)

def print_task(task: Task, entries: list[str], problem: str | None, flags: list[str], recorded: list[str], *, review: bool) -> None:
    print()
    print(f"{task.id}  {(task.front or {}).get('title', '')}")
    note(f"status: {task.status or 'none'}")
    note(f'priority: {Priority.of(task.front)}')
    if problem:
        note(f'failed hand-back: {problem}')
    for flag in flags:
        note(f'concerns: {flag}')
    note(f'report: {report_path(task.path)}')
    if review:
        for line in summary_lines(task.path):
            note(line)
    for entry in entries:
        note(entry)
    if review:
        for line in recorded:
            note(line)
        note(f'{CLOSE_LINE} {task.id}')

def get_decisions_digest(conversation: str | None=None, project: str | None=None, day: str | None=None) -> None:
    wanted = parse_day(day) if day is not None else None
    root = project_of(project)
    base = root if root is not None else content_root()
    contents = list(contents_of_tasks(base))
    questions = open_questions(contents)
    open_keys = {f'{task_id}#{number}' for task_id, number, _, _, _ in questions}
    recorded = decisions_by_task(contents)
    gathered = []
    decisions: list[str] = []
    reconcile_all(find_tasks(conversation=conversation, project=project_of(project)))
    reader = Reader(None)
    for task in find_tasks(conversation=conversation, project=project_of(project)):
        if task.status == Label_Queued.key:
            continue
        if wanted is not None and day_of(task.path) != wanted:
            continue
        entries = decisions_needed(task.path)
        problem = handback_problem(task.path, task.status)
        decisions.extend(entries)
        lying = pointer_problem(entries, open_keys)
        if lying:
            problem = f'{problem}; {lying}' if problem else lying
        flags = [*concerns(task), *concerns_for(task, reader)]
        if wanted is not None or entries or problem or flags:
            gathered.append((task, entries, problem, flags))
    listed = 0 if conversation is not None else None
    if not gathered:
        if listed is None:
            listed = print_open_questions(questions, decisions, wanted)
        if not listed:
            note(f'no task changed on {wanted.isoformat()}' if wanted else 'no decisions needed, and no failed hand-back')
        return
    count = sum((len(entries) for _, entries, _, _ in gathered))
    if wanted is not None:
        print(f'Review of {wanted.isoformat()} — {len(gathered)} tasks, {count} {REPORT.hand_back_part} entries')
    else:
        print(f'{REPORT.hand_back_part} — {len(gathered)} tasks, {count} entries')
    for task, entries, problem, flags in gathered:
        print_task(task, entries, problem, flags, recorded.get(task.id, []), review=wanted is not None)
    if listed is None:
        print_open_questions(questions, decisions, wanted)

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    digester = verbs.add_parser(DIGEST_COMMAND, help="gather every task's decisions needed into one digest, or review a day's tasks", description=f"""Without --day: one digest of every entry under `{REPORT.hand_back_part}` in the tasks'\n{REPORT_NAME}s: each task with entries, its title, status, priority, report status, and\nentries as written. A report that is not a short hand-back is in it too, marked `failed\nhand-back` with why, and so is a task not complete that looks finished or abandoned,\nmarked `concerns`; so is a task Blocked by its `{PlanKey.DEPENDS_ON.written}`, with what it waits for, and a\ndependency that cannot be found or makes a cycle. Queued tasks are left out; a complete task is in only when it has\nentries or a failed hand-back. A short hand-back is a {REPORT_NAME} whose Status equals its\nplan's and, only when it needs a decision, at most {REPORT.hand_back_max_lines} lines under `## {REPORT.hand_back_part}`,\neach the question, its options, and the one it recommends.\n\nWith --day: the review, for when the owner asks to "review today's tasks with me and\nclose the ones I confirm". Every task not queued that changed on that day, one by one,\nwith the command that closes it. Read each with the owner; run that\n`memar git trash-task-folder --task-id ID` only for those the owner confirms finished, and for\nnone of a project that keeps its tasks (its preferences set `tasks`). The review closes\nnothing itself.\n\nAfter the tasks it lists the open questions (contents of kind question that no later content
refers to), as `memar content questions` does: blocking first, then by task and number; with
--day only those asked that day; none with --conversation. A `{REPORT.hand_back_part}` line
naming `task#number` shows that question there and not again; one naming a question that is
not open is a failed hand-back. With --day each task also shows its decision contents: the
Decided, Confidence and Reason fields.

Without a project flag it reads Memar's own tasks; {ProjectName.FLAG} reads a project's wherever\nthey lie; --conversation one conversation's, by the id of a task in it.""")
    add_project_flags(digester, 'read the tasks of the project')
    digester.add_argument('--day', default=None, metavar='DAY', help=f'review the tasks that changed on DAY: {DAY_NAMES}')
    digester.add_argument('--conversation', default=None, metavar='ID', help='gather only the tasks of the conversation the task ID belongs to')
    return run

def run(args: argparse.Namespace) -> None:
    get_decisions_digest(args.conversation, project_from_args(args), args.day)
