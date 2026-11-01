#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
_files = import_module('modules-plugable.management.task.services.task_files')
_generation = import_module('modules-plugable.management.task.services.task_generation')
_tl = import_module('modules.management.timeline.services.timeline_files')
FACTS_NAME = _files.TASK_FACTS_NAME
PLAN_BODY = '# T\n\n## Request\nx\n\n## Why\n\n## Steps\n\n## Next\n'


def new_task(folder: Path, status: str = 'queued', title: str = 'T', project='P', start_date: str = '2026-10-13T00:00:00Z', plan: str | None = PLAN_BODY, report: str | None = None, report_status: str = '', **facts) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    held = {'title': title, 'status': status.lower(), 'project': str(project), 'start_date': start_date, 'writer': _generation.TASK_TYPE_UUID}
    held.update({key: value for key, value in facts.items() if value is not None})
    _files.write_facts(folder, held)
    if plan is not None:
        _tl.add_text(folder, 'plan', plan, 'agent')
    if report is not None:
        _tl.add_text(folder, 'report', report, 'agent', fields={'status': report_status} if report_status else None)
    return folder


_plan_file = import_module('modules-plugable.management.task.services.plan_file')
_header = import_module('modules.knowledge.text.services.header_text')
WRITTEN_FACTS = {key.written: fact for fact, key in _files.FRONT_KEY.items()}
WRITTEN_FACTS['Opened'] = 'start_date'


def from_plan_text(folder: Path, text: str) -> Path:
    lines = text.splitlines(keepends=True)
    front, start = _plan_file.front_matter([line.rstrip('\r\n') for line in lines])
    facts = {WRITTEN_FACTS[key]: value for key, value in (front or {}).items() if key in WRITTEN_FACTS}
    status = _plan_file.status_word(facts.pop('status', ''))
    folder.mkdir(parents=True, exist_ok=True)
    facts['status'] = status
    facts['writer'] = _generation.TASK_TYPE_UUID
    _files.write_facts(folder, facts)
    _tl.add_text(folder, 'plan', ''.join(lines[start:]), 'agent')
    return folder


def add_report(folder: Path, status: str, body: str = '# Report\n') -> None:
    _tl.add_text(folder, 'report', body, 'agent', fields={'status': status.lower()} if status else None)


def set_status(folder: Path, status: str) -> None:
    pairs = _header.parse((folder / FACTS_NAME).read_bytes().decode('utf-8-sig').splitlines())
    pairs['status'] = status.lower()
    ordered = {key: pairs[key] for key in (*_files.FACTS, *pairs) if key in pairs}
    (folder / FACTS_NAME).write_text(_header.render(ordered, _files.BLOCK_FACTS, _files.BLOCK_FACTS), encoding='utf-8', newline='\n')
