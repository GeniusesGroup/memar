#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from datetime import datetime, timezone
from pathlib import Path
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN_NAME = _m_plan_file.PLAN_NAME
REPORT_NAME = _m_record.REPORT.file_name


def create_report_md(folder: Path, text: str) -> None:
    try:
        with (folder / REPORT_NAME).open('x', encoding='utf-8', newline='\n') as report:
            report.write(text)
    except FileExistsError:
        pass


def create_plan_md(folder: Path, task: str, title: str, parent, conversation, project: Path, status: str, priority, labels, depends_on) -> None:
    opened = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    text = _m_plan_file.plan_skeleton(task, title, opened, project, parent=parent, conversation=conversation, status=status, priority=priority, labels=labels, depends_on=depends_on)
    try:
        with (folder / PLAN_NAME).open('x', encoding='utf-8', newline='\n') as plan:
            plan.write(text)
    except FileExistsError:
        pass
