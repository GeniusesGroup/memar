#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
from pathlib import Path
from typing import NamedTuple
from importlib import import_module
_index = import_module('modules.knowledge.text.services.index')
RULE_DOCUMENT = re.compile(r'(?:^|/)rules/([^/]+)/\1\.md$')
SENTENCE_END = re.compile(r'(?<=[.!?])\s')
WHY = 'why-it-exists'
LINK = re.compile(r'\[([^\]]*)\]\([^)]*\)')

class RuleHit(NamedTuple):
    document: str
    anchor: str
    why: str

class FindRules:

    def __init__(self, root: Path) -> None:
        self._root = Path(root)

    def do(self, subject: str, topics: list[str], most: int) -> list[RuleHit]:
        index = _index.build(self._root)
        found: dict[str, int] = {}
        for number in index.rank(subject):
            path = index.units[number].path
            if RULE_DOCUMENT.search(path) and path not in found:
                found[path] = number
        ordered = sorted(found, key=lambda path: 0 if self._has_topic(path, index.texts.get(path, ''), topics) else 1)
        return [self._hit(index, path, found[path]) for path in ordered[:max(most, 0)]]

    @staticmethod
    def _has_topic(path: str, text: str, topics: list[str]) -> bool:
        head = text.split('\n\n', 1)[0] if text.startswith('---') else ''
        words = set(re.split(r'[/_.-]', path.lower())) | set(re.split(r'\W+', head.lower()))
        return any(topic.lower() in words for topic in topics)

    @staticmethod
    def _hit(index, path: str, number: int) -> RuleHit:
        unit = index.units[number]
        why = ''
        for other in index.units:
            if other.path == path and other.anchor == WHY:
                why = FindRules._first_sentence(index.text_of(other), heading=True)
        if not why:
            for other in index.units:
                if other.path == path and other.anchor == 'the-rule':
                    why = FindRules._first_sentence(index.text_of(other), heading=True)
        return RuleHit(path, unit.anchor or 'the-rule', why)

    @staticmethod
    def _first_sentence(text: str, heading: bool) -> str:
        lines = text.splitlines()
        if heading and lines and lines[0].lstrip().startswith('#'):
            lines = lines[1:]
        paragraph = []
        for line in lines:
            if line.strip():
                paragraph.append(line.strip())
            elif paragraph:
                break
        flat = LINK.sub(r'\1', ' '.join(paragraph))
        return SENTENCE_END.split(flat, maxsplit=1)[0] if flat else ''
