#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/content_questions_lint.py — the fields an Open Questions entry carries, checked.

An entry written during a task stands alone by carrying State, Options, Anchor
and Blocks ([Open Questions](../../modules/content/documentation/handoff/handoff.md#open-questions)).
`content check` warns, never errors, on an entry missing one, because entries
written before the rule are still valid. The entries are the ones
`content_questions` lists: a heading one level below `Open Questions`.
"""
from __future__ import annotations

import re
from pathlib import Path

from services.content_questions import SECTION, _FENCE, _HEADING

FIELDS = ("State", "Options", "Anchor", "Blocks")
_FIELD = re.compile(
    r"^\s*(?:[-*]\s+)?\*{0,2}(State|Options|Anchor|Blocks)(?: continuation)?(?::\*{0,2}|\*{0,2}\s*:)", re.I
)


def entry_warnings(path: Path) -> list[str]:
    """One `line N: entry 'HEADING' lacks FIELDS` for each entry of PATH missing a field."""
    entries: list[list] = []
    section_level = entry_level = 0
    fenced = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if _FENCE.match(line):
            fenced = not fenced
            continue
        if fenced:
            continue
        heading = _HEADING.match(line)
        if heading:
            level, title = len(heading.group(1)), heading.group(2)
            if section_level and level <= section_level:
                section_level = 0
            if not section_level:
                if title == SECTION:
                    section_level, entry_level = level, level + 1
            elif level == entry_level:
                entries.append([number, title, set()])
            continue
        if section_level and entries:
            field = _FIELD.match(line)
            if field:
                entries[-1][2].add(field.group(1).capitalize())
    return [
        f"line {number}: entry '{title}' lacks {', '.join(missing)}"
        for number, title, have in entries
        if (missing := [name for name in FIELDS if name not in have])
    ]
