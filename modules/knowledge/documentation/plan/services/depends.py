#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/plan/services/depends.py — a plan's Depends_on written in place: one key rewritten, removed when empty, every other line kept.

What the key holds and how text becomes it is the type's (`modules/management/task/services/dependency.py`);
this file only writes the key, as `session_plan_labels` writes a label. The
Status a changed key gives the session is `session_depends`'s, after this.
"""
from __future__ import annotations
from pathlib import Path
from machine.console import fail
from machine.modules_import import load as modules_load
DependsOn = modules_load('management', 'task', 'services', 'dependency').DependsOn
from modules.knowledge.documentation.plan.services.plan import front_matter
from modules.knowledge.documentation.plan.services.rewrite import key_of, line_end, rewrite
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey

def set_depends_on(path: Path, depends_on: DependsOn) -> None:
    """Write DEPENDS_ON as PATH's `Depends_on`, replacing the key or adding it last in the front matter; empty removes the key.

    Every other line is kept. A plan without front matter has no place for it
    and is refused. The references are not checked here: the caller has
    (`depends_on.refused_for_writing`).
    """

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its {PlanKey.DEPENDS_ON.written} cannot be set')
        written = [f'{PlanKey.DEPENDS_ON.written}: {depends_on.text()}{line_end(lines[0])}'] if depends_on else []
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.DEPENDS_ON.written:
                return [*lines[:index], *written, *lines[index + 1:]]
        return [*lines[:start - 1], *written, *lines[start - 1:]]
    rewrite(path, change)
