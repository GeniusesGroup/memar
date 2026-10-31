#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from typing import Callable
from machine.console import fail
Task_Error_Changed = import_module('modules-plugable.management.task.errors.errors').Task_Error_Changed
ATTEMPTS = 5


def change_fact(task: str, name: str, read: Callable, replace: Callable, make: Callable) -> None:
    for _ in range(ATTEMPTS):
        value, version = read()
        wanted = make(value)
        if wanted is None:
            return
        try:
            replace(wanted, version)
            return
        except Task_Error_Changed:
            continue
    fail(f'the {name} of task {task} kept changing while it was being rewritten, so nothing was written; try again')
