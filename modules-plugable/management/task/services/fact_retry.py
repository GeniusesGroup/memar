#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from typing import Callable
from machine.console import fail
_m_errors = import_module('modules-plugable.management.task.errors.errors')
Task_Error_Changed = _m_errors.Task_Error_Changed
Task_Error_WrittenByPredecessor = _m_errors.Task_Error_WrittenByPredecessor
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
        except Task_Error_WrittenByPredecessor as refused:
            fail(f'task {task} was written by the module {refused.writer}, which is EndOfLife; its successor is {refused.successor}. Convert this task with {refused.conversion} and ask again')
    fail(f'the {name} of task {task} kept changing while it was being rewritten, so nothing was written; try again')
