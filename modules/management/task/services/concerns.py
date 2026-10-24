#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/concerns.py — what a plan gives away about work that looks finished or abandoned yet is not complete.

Why this exists. The sweep moves only `complete` tasks, because idle is not
finished and a folder is what carries an unfinished task to the next task.
The price is that a task whose agent forgot to set its status stays for
ever, and the owner has to audit the folders by hand to find which ones are
that. `concerns` answers for one task, from its plan alone, whether it looks
like one of three such cases, so `list`, `gc`, and `digest` can say so beside
the task. It only says: nothing here moves, writes, or closes a folder, and
whether a flagged task is finished is the person's word, given to `close`.

The three cases, each a fact about the plan and no judgment of the work:
every step of the plan is checked while the status is still active; the Request
is empty, so no one was told what the task is, and the plan has been quiet for
a day, long enough that it is not simply a plan being written; and the plan
has no status at all. A status that is present but outside the vocabulary is
named by `task_report.disagreement`, which `list` already shows, so it is
not named twice. A complete task raises nothing, however it looks, and a plan of
the earlier sectioned form is not judged by a Request or by steps it never had.
"""
from __future__ import annotations
import re
from modules.management.task.plan.primitive.plan_part import PlanPart
from modules.knowledge.status.primitive.status import Status
from modules.management.task.services.folder import Task, measured_idle
from modules.management.task.services.plan_file import is_complete, part_text
from modules.management.task.services.report_file import report_shape_problem
EMPTY_REQUEST_IDLE_DAYS = 1
_CHECKBOX = re.compile('^\\s*[-*]\\s+\\[([ xX])\\]')

def all_steps_checked(steps: str) -> bool:
    """Whether STEPS, a plan's Steps text, holds at least one checkbox and every one is checked."""
    boxes = [match.group(1) for line in steps.splitlines() if (match := _CHECKBOX.match(line))]
    return bool(boxes) and all((box != ' ' for box in boxes))

def concerns(task: Task) -> list[str]:
    """The reasons TASK looks finished or abandoned though it is not done; none for a sound or unreadable one."""
    if not (task.has_plan and task.readable):
        return []
    found: list[str] = []
    for problem in (task.shape, report_shape_problem(task.path)):
        if problem:
            found.append(problem)
    if task.shape or task.front is None or is_complete(task.status):
        return found
    plan = task.path / 'plan.md'
    if not task.status:
        found.append('it has no status')
    try:
        if task.status == Status.ACTIVE.key and all_steps_checked(part_text(plan, PlanPart.STEPS.heading)):
            found.append('every step is checked, yet the status is active')
        if not part_text(plan, PlanPart.REQUEST.heading):
            idle = measured_idle(task.path)
            if idle is not None and idle >= EMPTY_REQUEST_IDLE_DAYS:
                found.append(f'its Request is empty and nothing has changed for {idle:.1f} days')
    except OSError:
        pass
    return found
