#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from pathlib import Path
_header = import_module('modules.knowledge.text.services.header_text')

TASK_TYPE_UUID = '6e94ed31-f133-485c-a3c0-72def253b37b'
G2_TYPE_UUID = 'fec2d0e7-eb2b-4179-9f94-2b38b956849f'
FIRST_GENERATION_TYPE_UUID = '0594ae4f-8708-434f-9d42-d489f4089c09'
WRITER_FACT = 'writer'
CONVERTED_FROM_FACT = 'converted_from'
PREVIOUS_FOLDER = 'previous'
CONVERSION_SERVICE = 'modules-plugable/management/task/services/task_conversion.py'
FACTS_NAME = 'task.yaml'
OLD_PLAN_NAME = 'plan.md'


def writer_of(folder: Path) -> tuple:
    path = folder / FACTS_NAME
    if not path.is_file():
        return (FIRST_GENERATION_TYPE_UUID, False)
    stamp = _header.parse(path.read_bytes().decode('utf-8-sig').splitlines()).get(WRITER_FACT, '').strip()
    if not stamp:
        return (FIRST_GENERATION_TYPE_UUID, False)
    return (stamp, True)


def is_task_record(folder: Path) -> bool:
    return (folder / FACTS_NAME).is_file() or (folder / OLD_PLAN_NAME).is_file()


def count_written_by(root: Path, writer: str) -> int:
    return sum(1 for folder in sorted(root.iterdir()) if folder.is_dir() and is_task_record(folder) and writer_of(folder)[0] == writer)
