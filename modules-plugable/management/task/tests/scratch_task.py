#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
"""Scratch task directories for tests that need a chosen listing root under a TemporaryDirectory.

Production `task_dir` already lives under scratch `tasks_root()`; use this when a fixture
must place folders under a specific fake root (e.g. `locations=[...]` listing tests).
"""
from __future__ import annotations
from pathlib import Path
from typing import Callable
from machine.console import fail


def task_dir_under(root: Path) -> Callable[..., Path]:
    """A task_dir stand-in that materializes under ROOT so a mistaken mkdir cannot land in the checkout cwd."""

    def task_dir(task_id: str, *, create: bool=False) -> Path:
        if not task_id or task_id in ('.', '..') or '/' in task_id or '\\' in task_id:
            fail(f'refusing task id {task_id!r}: name one folder segment, not a path.')
        path = root / 'task-dirs' / task_id
        if create:
            path.mkdir(parents=True, exist_ok=True)
        return path

    return task_dir
