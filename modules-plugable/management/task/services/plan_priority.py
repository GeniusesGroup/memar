#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority
change_fact = import_module('modules-plugable.management.task.services.fact_retry').change_fact


def set_priority(store, project, task, priority) -> None:
    priority = Priority.checked(priority)
    change_fact(task, 'priority', lambda: store.read_priority(project, task), lambda value, version: store.replace_priority(project, task, value, version), lambda was: priority)
