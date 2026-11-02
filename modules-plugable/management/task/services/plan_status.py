#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from modules.knowledge.label.labels.Label_Status import Label_Status
from importlib import import_module
from machine.console import fail
status_word = import_module('modules-plugable.management.task.services.plan_file').status_word
PLAN = import_module('modules-plugable.knowledge.documentation.primitive.record').PLAN
change_fact = import_module('modules-plugable.management.task.services.fact_retry').change_fact

def set_status(store, project, task, status: str, only_from: tuple | None = None) -> None:
    status = status_word(status)
    wanted = None if only_from is None else tuple(status_word(word) for word in only_from)
    for word in (status, *(wanted or ())):
        if word not in Label_Status.keys(PLAN.kind):
            fail(f"{word!r} is not a status; the statuses are {', '.join(Label_Status.keys(PLAN.kind))}")

    def make(was: str):
        found = status_word(was)
        if wanted is not None and found not in wanted:
            fail(f"task {task} is {found or 'without a status'} now, no longer {' or '.join(only_from)}, so it is not set to {status}")
        return status
    change_fact(task, 'status', lambda: store.read_status(project, task), lambda value, version: store.replace_status(project, task, value, version), make)
