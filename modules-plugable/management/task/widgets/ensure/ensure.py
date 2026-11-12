#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from pathlib import Path

ensure_task = import_module('modules-plugable.management.task.services.ensure').ensure_task
set_priority = import_module('modules-plugable.management.task.services.task_thing_services').set_priority


def open(task_id: str | None=None, title: str | None=None, parent: str | None=None, queued: bool=False, priority: int | None=None, labels: list[str] | None=None, project: str | None=None, depends_on: list[str] | None=None) -> tuple[str, Path]:
    sid, path = ensure_task(task_id, title, parent, queued, labels, project, depends_on)
    if priority is not None:
        set_priority(sid, priority, project)
    return (sid, path)
