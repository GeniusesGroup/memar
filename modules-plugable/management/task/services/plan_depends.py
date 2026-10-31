#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
change_fact = import_module('modules-plugable.management.task.services.fact_retry').change_fact


def set_depends_on(store, project, task, depends_on) -> None:
    change_fact(task, 'depends_on', lambda: store.read_depends_on(project, task), lambda value, version: store.replace_depends_on(project, task, value, version), lambda was: depends_on)
