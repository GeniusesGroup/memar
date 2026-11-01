#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
_m_task_files = import_module('modules-plugable.management.task.services.task_files')
from modules.knowledge.label.primitive.label import Labels
PLAN_NAME = _m_plan_file.PLAN_NAME
REPORT_NAME = import_module('modules-plugable.knowledge.documentation.primitive.record').REPORT.file_name
FRONT_KEY = _m_task_files.FRONT_KEY
CONVERTIBLE_FACTS = ('title', 'status', 'priority', 'labels', 'depends_on', 'parent', 'conversation', 'project', 'start_date')


def _lines(path: Path) -> list:
    return _m_plan_file.read_bytes(path).decode('utf-8-sig').splitlines(keepends=True)


def _body(path: Path) -> tuple:
    lines = _lines(path)
    front, start = _m_plan_file.front_matter([line.rstrip('\r\n') for line in lines])
    return (front or {}, ''.join(lines[start:]))


def read_plan(folder: Path) -> str:
    return _body(folder / PLAN_NAME)[1]


def read_report(folder: Path) -> tuple:
    path = folder / REPORT_NAME
    if not path.is_file():
        return ('', False, '')
    front, body = _body(path)
    return (body, True, _m_plan_file.status_word(front.get('Status', '')))


def read_fact(folder: Path, fact: str) -> str:
    front = _body(folder / PLAN_NAME)[0]
    value = front.get(FRONT_KEY[fact].written, '')
    if fact == 'labels':
        return '\n'.join(Labels.read(value).lines())
    return _m_plan_file.status_word(value) if fact == 'status' else value.strip()


def read_facts(folder: Path) -> dict:
    return {fact: read_fact(folder, fact) for fact in CONVERTIBLE_FACTS}


def problem(folder: Path) -> str | None:
    front, _ = _body(folder / PLAN_NAME)
    if not front:
        return f'{PLAN_NAME} has no front matter'
    return _m_plan_file.plan_file_problem(folder / PLAN_NAME)


def read_report_lines(folder: Path) -> list:
    try:
        return (folder / REPORT_NAME).read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeDecodeError):
        return []
