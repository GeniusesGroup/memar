#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import re
Request = import_module('modules-plugable.knowledge.documentation.plan.primitive.request').Request
Steps = import_module('modules-plugable.knowledge.documentation.plan.primitive.steps').Steps
from modules.knowledge.label.services.status_words import Status
_m_folder = import_module('modules-plugable.management.task.services.folder')
Task = _m_folder.Task
measured_idle = _m_folder.measured_idle
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
is_complete = _m_plan_file.is_complete
part_text = _m_plan_file.part_text
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
report_shape_problem = _m_report_file.report_shape_problem
EMPTY_REQUEST_IDLE_DAYS = 1
_CHECKBOX = re.compile('^\\s*[-*]\\s+\\[([ xX])\\]')

def all_steps_checked(steps: str) -> bool:
    boxes = [match.group(1) for line in steps.splitlines() if (match := _CHECKBOX.match(line))]
    return bool(boxes) and all((box != ' ' for box in boxes))

def concerns(task: Task) -> list[str]:
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
        if task.status == Status.ACTIVE.key and all_steps_checked(part_text(plan, Steps.heading)):
            found.append('every step is checked, yet the status is active')
        if not part_text(plan, Request.heading):
            idle = measured_idle(task.path)
            if idle is not None and idle >= EMPTY_REQUEST_IDLE_DAYS:
                found.append(f'its Request is empty and nothing has changed for {idle:.1f} days')
    except OSError:
        pass
    return found
