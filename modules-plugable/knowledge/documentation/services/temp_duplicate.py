#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
_m_timeline_files = import_module('modules.management.timeline.services.timeline_files')

TEMP_FOLDER = 'temp'


def _body(data: bytes) -> str:
    return _m_timeline_files.content_of(0, data).body.rstrip('\r\n')


def temp_duplicate_problems(path: Path) -> list[str]:
    if path.parent.name != TEMP_FOLDER:
        return []
    task = path.parent.parent
    try:
        mine = _body(path.read_bytes()) if _m_timeline_files.content_of(0, path.read_bytes()).header == {} else path.read_bytes().decode('utf-8-sig').rstrip('\r\n')
    except (OSError, UnicodeDecodeError):
        return []
    if not mine.strip():
        return []
    problems: list[str] = []
    for number in _m_timeline_files.numbers(task):
        try:
            content = _m_timeline_files.read_content_file(task, number)
        except (OSError, UnicodeDecodeError):
            continue
        if content.body.rstrip('\r\n') == mine:
            problems.append(f'equals the body of {_m_timeline_files.content_name(number)} of the same task; the text is posted, so this copy is removed (task rule: the scratch folder holds no content)')
    return problems
