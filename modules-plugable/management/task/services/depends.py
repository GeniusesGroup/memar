#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/depends.py — the verb `memar task depends-on`, and the Status a task's dependencies give it.

What a dependency is, when it is met, and how it is checked is the type's
(`modules-plugable/management/task/services/dependency.py`); writing the key is `task_plan_depends`. This file
decides what the key does to a task, and says it.

The Status of a task with dependencies. An unmet `Depends_on` makes the
task Blocked, the Status word that already means "cannot continue until a
dependency arrives; the record states what it waits for" (`memar task
--help`), and the record states it: the key holds the ids, and every verb that
shows the task prints each with where it stands. No Status word is added.

How the Status is kept truthful. A stored Status is a fact that goes stale
when the task it waits for ends, and the one that ends must not write
another task's folder. So the Status is set when the key is written and
brought up to date by every verb that reads tasks to decide or to show
(`claim`, `claims`, `list`, `digest`) through `reconcile`, which does two things
and nothing else:
- a Queued task with an unmet dependency becomes Blocked;
- a Blocked task whose every dependency is now met becomes Queued again,
  but only one that Memar itself blocked for its dependencies, which the
  task log says (`BLOCKED_EVENT`, `RELEASED_EVENT`); dropping the last
  dependency leaves none unmet, so it is released the same way. A task blocked by
  hand, or a delegating task's own plan blocked on the tasks it waits for, is
  never put back in line behind its agent's back: `list` and `digest` say that
  every dependency is Complete and it can resume.
An Active task is never changed: it is running, and its agent sets Blocked
when it cannot go on. Once released, a task is an ordinary queued one:
`claim` and `claims` take it, and it goes Active on the claim.

A task whose dependency is not met cannot be claimed or started
(`refusal`), whatever its Status, and the refusal names the unmet ids and how
each stands; one that no longer resolves keeps it unclaimable until the key is
dropped, and the refusal says so.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
from pathlib import Path
from typing import Iterable
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
ARROW = _m_dependency.ARROW
DEPENDS_FOR = _m_dependency.DEPENDS_FOR
DependsOn = _m_dependency.DependsOn
Reader = _m_dependency.Reader
dependents = _m_dependency.dependents
_m_folder = import_module('modules-plugable.management.task.services.folder')
Task = _m_folder.Task
read_task = _m_folder.read_task
_m_log = plugable_load('computer.git.services.log')
log_path = _m_log.log_path
record = _m_log.record
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
_m_plan_status = import_module('modules-plugable.management.task.services.plan_status')
set_status = _m_plan_status.set_status
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
from modules.knowledge.status.primitive.status import Status
DEPENDS_COMMAND = PlanKey.DEPENDS_ON.key.replace('_', '-')
BLOCKED_EVENT = 'blocked-by-dependency'
RELEASED_EVENT = 'released-by-dependency'

def home_of(task: Task) -> Path | None:
    """The project TASK's plan names, when it is a folder that is there; where its local references are looked for."""
    named = (task.front or {}).get(PlanKey.PROJECT.key, '').strip()
    return Path(named) if named and Path(named).is_dir() else None

def problems(task: Task, reader: Reader) -> list[str]:
    """Why TASK's dependencies are not met, one reason each, a cycle among them; none when it has none or all are met."""
    refs = DependsOn.of(task.front)
    if not refs:
        return []
    home = home_of(task)
    reasons = reader.unmet(refs, home)
    path = reader.cycle(task.id, refs, home)
    if path:
        reasons.append(f'a dependency cycle {ARROW.join(path)}')
    return reasons

def blocked_by_memar(folder: Path) -> bool:
    """Whether the task log's last word on FOLDER's task about its dependencies is that Memar blocked it."""
    try:
        lines = log_path(folder).read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeDecodeError):
        return False
    for line in reversed(lines):
        fields = line.split('\t')
        if len(fields) >= 3 and fields[2] == folder.name and (fields[1] in (BLOCKED_EVENT, RELEASED_EVENT)):
            return fields[1] == BLOCKED_EVENT
    return False

def reconcile(task: Task, reader: Reader) -> str:
    """Bring TASK's Status up to date with its dependencies, as the module says; the Status it has now."""
    if not (task.has_plan and task.readable):
        return task.status
    if task.status not in (Status.QUEUED.key, Status.BLOCKED.key):
        return task.status
    if not DependsOn.of(task.front) and (not (task.status == Status.BLOCKED.key and blocked_by_memar(task.path))):
        return task.status
    unmet = problems(task, reader)
    plan = task.path / PLAN_NAME
    try:
        if unmet and task.status == Status.QUEUED.key:
            set_status(plan, Status.BLOCKED.key, expected=(Status.QUEUED.key,))
            record(BLOCKED_EVENT, task.id, '; '.join(unmet), folder=task.path)
            return Status.BLOCKED.key
        if not unmet and task.status == Status.BLOCKED.key and blocked_by_memar(task.path):
            set_status(plan, Status.QUEUED.key, expected=(Status.BLOCKED.key,))
            record(RELEASED_EVENT, task.id, '', folder=task.path)
            return Status.QUEUED.key
    except SystemExit:
        return read_task(task.path).status
    return task.status

def reconcile_all(tasks: Iterable[Task], reader: Reader | None=None) -> None:
    """`reconcile` each of TASKS that has dependencies, with one reader so each cited task is read once; READER when the caller keeps reading with it."""
    reader = reader or Reader(None)
    for task in tasks:
        reconcile(task, reader)

def refusal(folder: Path, act: str) -> str | None:
    """Why the task at FOLDER cannot be ACT'ed (`claim`, `start`) for its dependencies, naming each; None when it can.

    The Status is brought up to date first, so the refusal and the Status agree.
    """
    task = read_task(folder)
    if not (task.has_plan and task.readable) or not DependsOn.of(task.front):
        return None
    reader = Reader(None)
    unmet = problems(task, reader)
    reconcile(task, reader)
    if not unmet:
        return None
    return f"task {task.id} depends on {', '.join(unmet)}, so it cannot be {act}ed until each is Complete; a dependency that cannot be found stays until it is dropped with `memar task {DEPENDS_COMMAND} {task.id} --drop REF`"

def labelled(refs: DependsOn, reader: Reader, home: Path | None) -> str:
    """REFS each with where it stands, `ref (state)`, as the plan's key is shown."""
    parts = []
    for ref in refs:
        found = reader.find(ref, home)
        state = found.split(':')[0] if isinstance(found, str) else 'complete' if found.met else found.state
        parts.append(f'{ref} ({state})')
    return ', '.join(parts)

def notes_for(task: Task, reader: Reader, everyone: Iterable[Task]) -> list[str]:
    """The lines `list` shows under TASK for its dependencies and for the tasks that depend on it; none when it has neither."""
    refs = DependsOn.of(task.front)
    lines = []
    if refs:
        lines.append(f'{PlanKey.DEPENDS_ON.written}: {labelled(refs, reader, home_of(task))}')
    cited_by = dependents(task.id, everyone)
    if cited_by:
        lines.append(f"{DEPENDS_FOR}: {', '.join(cited_by)}")
    return lines

def concerns_for(task: Task, reader: Reader) -> list[str]:
    """What TASK's dependencies say that its reader should know: a cycle, a dependency that cannot be found, and a blocked task that can resume."""
    refs = DependsOn.of(task.front)
    if not refs or not (task.has_plan and task.readable):
        return []
    home = home_of(task)
    found = []
    for ref in refs:
        why = reader.find(ref, home)
        if isinstance(why, str):
            found.append(f'{PlanKey.DEPENDS_ON.written} {ref}: {why}; it stays unclaimable until the key is dropped')
    path = reader.cycle(task.id, refs, home)
    if path:
        found.append(f'{PlanKey.DEPENDS_ON.written} makes a cycle: {ARROW.join(path)}')
    if task.status == Status.BLOCKED.key and (not problems(task, reader)):
        found.append(f'blocked, and every {PlanKey.DEPENDS_ON.written} is Complete: it can resume')
    elif task.status == Status.BLOCKED.key:
        found.append(f'blocked by {PlanKey.DEPENDS_ON.written}: ' + '; '.join(problems(task, reader)))
    return found
