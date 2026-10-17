#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan_topic.py — a plan's topic written in place: one key rewritten, removed when empty, every other line kept.

What a topic is and how text becomes one are the type's (`services/topic.py`); this file only writes the key.
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from services.session_plan import front_matter
from services.session_plan_rewrite import key_of, line_end, rewrite
from services.session_record import PlanKey
from services.topic import Topic


def set_topic(path: Path, topic: str) -> None:
    """Write TOPIC as PATH's `topic`, replacing the key or adding it last in the front matter; empty removes the key.

    Every other line is kept. A plan without front matter has no place for it
    and is refused. TOPIC is normalized here, so the plan never holds another
    form.
    """
    topic = Topic.checked(topic)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its topic cannot be set")
        written = [f"{PlanKey.TOPIC.written}: {topic}{line_end(lines[0])}"] if topic else []
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.TOPIC.written:
                return [*lines[:index], *written, *lines[index + 1:]]
        return [*lines[:start - 1], *written, *lines[start - 1:]]

    rewrite(path, change)
