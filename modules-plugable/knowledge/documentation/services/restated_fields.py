#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import re
from importlib import import_module
from pathlib import Path
_m_document_module = import_module('modules-plugable.knowledge.documentation.services.document_module')
RULE = 'modules-plugable/knowledge/documentation/rules/document-restates-no-code/document-restates-no-code.md'
LEAST_RESTATED = 3
FENCE = re.compile('(?ms)^(```|~~~).*?^\\1[ \\t]*$')
LINKED_CELL = re.compile('^\\[([^\\]]+)\\]\\([^)]*\\)$')
SEPARATOR_ROW =re.compile('^\\|?[ \\t]*:?-{2,}:?[ \\t]*(\\|[ \\t]*:?-{2,}:?[ \\t]*)*\\|?$')


def _without_fences(text: str) -> str:
    return FENCE.sub(lambda match: re.sub('[^\\n]', ' ', match.group(0)), text)


def _first_cell(row: str) -> str:
    cell = row.strip().strip('|').split('|')[0].strip()
    linked = LINKED_CELL.match(cell)
    if linked:
        cell = linked.group(1)
    return cell.strip().strip('`*_ ').removesuffix('()').strip().lower()


def _tables(text: str):
    lines = _without_fences(text).splitlines()
    index = 0
    while index < len(lines):
        if lines[index].lstrip().startswith('|') and index + 1 < len(lines) and SEPARATOR_ROW.match(lines[index + 1].strip()):
            start = index
            index += 2
            rows: list[str] = []
            while index < len(lines) and lines[index].lstrip().startswith('|'):
                rows.append(lines[index])
                index += 1
            yield (start + 1, rows)
        else:
            index += 1


def restated_field_problems(path: Path, text: str, cache: dict, root: Path) -> list[str]:
    module = _m_document_module.module_of(path, root, cache)
    if module is None:
        return []
    names = _m_document_module.declared_names(module, root, cache)
    if not names:
        return []
    problems: list[str] = []
    for line, rows in _tables(text):
        restated = sorted({cell for cell in map(_first_cell, rows) if cell in names})
        if len(restated) >= LEAST_RESTATED:
            files = sorted({names[cell].relative_to(module).as_posix() for cell in restated})
            problems.append(f"line {line}: a table whose first column restates {len(restated)} names that {', '.join(files)} of this module declares ({', '.join(restated)}); a document restates no type, field or signature that code declares, it links to the file ({RULE})")
    return problems
