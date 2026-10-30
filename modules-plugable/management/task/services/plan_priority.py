#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/plan_priority.py — a plan's priority written in place: one key rewritten, every other line kept.

What a priority is, its bounds, its default and how a plan's value is read are the type's (`modules-plugable/knowledge/documentation/plan/primitive/priority.py`);
this file only writes the key.
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path
from machine.console import fail
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
front_matter = _m_plan_file.front_matter
_m_plan_rewrite = import_module('modules-plugable.management.task.services.plan_rewrite')
key_of = _m_plan_rewrite.key_of
line_end = _m_plan_rewrite.line_end
rewrite = _m_plan_rewrite.rewrite
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey

def set_priority(path: Path, priority: int) -> None:
    """Write PRIORITY as PATH's `priority`, replacing the key or adding it last in the front matter; every other line is kept.

    A plan without front matter has no place for it and is refused.
    """
    priority = Priority.checked(priority)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its priority cannot be set')
        written = f'{PlanKey.PRIORITY.written}: {priority}{line_end(lines[0])}'
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.PRIORITY.written:
                return [*lines[:index], written, *lines[index + 1:]]
        return [*lines[:start - 1], written, *lines[start - 1:]]
    rewrite(path, change)
