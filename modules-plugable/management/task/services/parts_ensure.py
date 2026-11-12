#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/parts_ensure.py — the ensure pieces the intake widget composes today.

Ensure is still one function; this surface names the composition slot Parts_Ensure so the intake widget does not
call ensure's CLI face. When ensure is split, each part replaces the body here and the widget stays.
"""
from __future__ import annotations
from importlib import import_module
from pathlib import Path

_m_ensure = import_module('modules-plugable.management.task.widgets.ensure.ensure')
open_ensure = _m_ensure.open


def parts_ensure(task_id: str | None=None, title: str | None=None, parent: str | None=None, queued: bool=False, priority: int | str | None=None, labels: list[str] | None=None, project: str | None=None, depends_on: list[str] | None=None) -> tuple[str, Path]:
    return open_ensure(task_id, title, parent, queued, priority, labels, project, depends_on)
