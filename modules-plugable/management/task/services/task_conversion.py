#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import NamedTuple
Task_Error_NotConvertible = import_module('modules-plugable.management.task.errors.errors').Task_Error_NotConvertible
_files = import_module('modules-plugable.management.task.services.task_files')
_generation = import_module('modules-plugable.management.task.services.task_generation')
_adapter = import_module('modules-plugable.management.task.services.task_predecessor_adapter')
_tl = import_module('modules.management.timeline.services.timeline_files')
SERVICE_NAME = _generation.CONVERSION_SERVICE
ANSWERED_FACTS = _adapter.CONVERTIBLE_FACTS


class Step(NamedTuple):
    converted: int
    left: int
    refused: list


def answers(folder: Path) -> dict:
    if (folder / _files.TASK_FACTS_NAME).is_file():
        facts = _files.read_facts(folder) or {}
        report = _tl.latest_content(folder, 'report')
        return {
            'plan': _files.plan_body(folder) or '',
            'report': (report.body, True, _files.status_word(report.header.get('status', ''))) if report else ('', False, ''),
            'facts': {fact: facts.get(fact, '') or '' for fact in ANSWERED_FACTS},
        }
    return {'plan': _adapter.read_plan(folder), 'report': _adapter.read_report(folder), 'facts': _adapter.read_facts(folder)}


def _stamp(folder: Path) -> None:
    path = folder / _files.TASK_FACTS_NAME
    pairs = _files._header.parse(path.read_bytes().decode('utf-8-sig').splitlines())
    pairs[_generation.WRITER_FACT] = _generation.TASK_TYPE_UUID
    ordered = {key: pairs[key] for key in (*_files.FACTS, *pairs) if key in pairs}
    _files._replace_file(path, lambda data: _files._header.render(ordered, _files.BLOCK_FACTS, _files.BLOCK_FACTS))


def pending_stamp(root: Path) -> list:
    return [folder.name for folder in sorted(root.iterdir()) if folder.is_dir() and (folder / _files.TASK_FACTS_NAME).is_file() and not _generation.writer_of(folder)[1]]


def stamp_task(folder: Path) -> bool:
    path = folder / _files.TASK_FACTS_NAME
    if not path.is_file() or _generation.writer_of(folder)[1]:
        return False
    before = answers(folder)
    held = path.read_bytes()
    _stamp(folder)
    if answers(folder) != before or _generation.writer_of(folder) != (_generation.TASK_TYPE_UUID, True):
        path.write_bytes(held)
        raise Task_Error_NotConvertible('the answers after the stamp differ from the answers before it')
    return True


def stamp_tasks(root: Path, limit: int) -> Step:
    pending = pending_stamp(root)
    taken = pending[:limit]
    stamped = 0
    refused = []
    for name in taken:
        try:
            stamped += 1 if stamp_task(root / name) else 0
        except Task_Error_NotConvertible as error:
            refused.append((name, error.reason))
    return Step(stamped, len(pending) - len(taken), refused)
