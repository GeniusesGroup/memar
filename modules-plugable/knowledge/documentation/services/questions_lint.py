#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
from pathlib import Path
from modules.knowledge.content.primitive.catalog import Catalog
QUESTION_KIND = 'question'
FIELDS = Catalog(Path(__file__).resolve().parent.parent / 'handoff' / 'primitive', 'warned').headings()
_FENCE = re.compile('^\\s*(```|~~~)')
_FIELD = re.compile('^\\s*(?:[-*]\\s+)?\\*{0,2}(' + '|'.join(FIELDS) + ')(?: continuation)?(?::\\*{0,2}|\\*{0,2}\\s*:)', re.I)


def question_warnings(content) -> list:
    if content.header.get('kind') != QUESTION_KIND:
        return []
    have = set()
    fenced = False
    for line in content.body.splitlines():
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        field = _FIELD.match(line)
        if field:
            have.add(field.group(1).capitalize())
    missing = [name for name in FIELDS if name not in have]
    return [f"question lacks {', '.join(missing)}"] if missing else []
