#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import re
from pathlib import Path
_m_catalog = import_module('modules.knowledge.content.primitive.catalog')
Pending = import_module('modules-plugable.knowledge.documentation.changelog.primitive.pending').Pending
import_module('modules-plugable.knowledge.documentation.changelog.primitive.done')
import_module('modules-plugable.knowledge.documentation.changelog.primitive.rejected')
_m_markdown = import_module('modules-plugable.computer.codec.markdown.services.markdown')
without_code = _m_markdown.without_code
STATES = _m_catalog.Catalog(Path(__file__).resolve().parents[1] / 'changelog' / 'primitive', 'propagation-state').words()
CHANGELOG_KIND = 'changelog'
_FIELD = re.compile(r'^([ \t]*)[-*][ \t]+Propagates to:[ \t]*$')
_ITEM = re.compile(r'^[ \t]*[-*][ \t]+(?P<artifact>\S.*?):[ \t]*(?P<state>' + '|'.join(STATES) + r')(?![A-Za-z])')


def _items(body: str) -> list:
    visible = without_code(body).split('\n')
    original = body.split('\n')
    found = []
    inside = None
    for index, line in enumerate(visible):
        field = _FIELD.match(line)
        if field:
            inside = len(field.group(1).expandtabs())
            continue
        if inside is None:
            continue
        if line.strip() and len(line) - len(line.lstrip()) <= inside:
            inside = None
            continue
        item = _ITEM.match(original[index]) if line.strip() else None
        if item:
            found.append((item.group('artifact').strip(), item.group('state'), index + 1, original[index].strip().lstrip('-* \t')))
    return found


def open_propagations(contents) -> list:
    latest: dict = {}
    for task_id, content in contents:
        if content.header.get('kind') != CHANGELOG_KIND:
            continue
        for artifact, state, line, text in _items(content.body):
            latest.pop(artifact, None)
            latest[artifact] = (state, task_id, content.number, line, text)
    return [(task_id, number, line, text) for state, task_id, number, line, text in latest.values() if state == Pending.word]
