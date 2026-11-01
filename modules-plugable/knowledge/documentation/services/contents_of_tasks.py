#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path, PurePosixPath
from typing import Iterator
_m_task_records = import_module('modules-plugable.management.task.services.task_records')
_m_timeline_files = import_module('modules.management.timeline.services.timeline_files')


def _is_content(record) -> bool:
    place = PurePosixPath(record.path)
    return _m_timeline_files.CONTENT_PATTERN.match(place.name) is not None and place.parent.name == record.task


def contents_of_tasks(root: Path, notes: list | None = None) -> Iterator[tuple]:
    records, said = _m_task_records.task_records(root)
    if notes is not None:
        notes.extend(said)
    held = [record for record in records if _is_content(record)]
    first = {}
    for position, record in enumerate(held):
        first.setdefault(record.task, position)
    held.sort(key=lambda record: (first[record.task], PurePosixPath(record.path).name))
    texts = _m_task_records.read_all(root, held)
    for record in held:
        text = texts.get(record.path)
        if text is None:
            continue
        number = int(_m_timeline_files.CONTENT_PATTERN.match(PurePosixPath(record.path).name).group(1))
        yield (record.task, _m_timeline_files.content_of(number, text.encode('utf-8')))
