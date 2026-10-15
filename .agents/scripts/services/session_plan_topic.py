#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan_topic.py — a plan's topic: the one subject `claims` batches by, normalized and written in place.

One value, not several: a task with two subjects is two tasks. It is free text normalized when written
(lower case, runs of white space as one hyphen), not a list the project keeps; a typo that splits one
subject in two is met by showing the topics in use and by warning of a near match (`session_topic`).
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from services.session_plan import front_matter
from services.session_plan_rewrite import key_of, line_end, rewrite
from services.session_record import PlanKey


def normalized_topic(text: str) -> str:
    """TEXT as a topic: stripped, lower case, each run of white space one hyphen; empty when nothing is left."""
    return "-".join(text.lower().split())


def checked_topic(text: str) -> str:
    """TEXT as a topic, normalized; refused when it holds a line break, since a topic is a one-line front-matter value."""
    if "\n" in text or "\r" in text:
        fail("a topic is one line; this one holds a line break")
    return normalized_topic(text)


def topic_of(front: dict[str, str] | None) -> str:
    """The topic FRONT matter gives its plan, normalized; empty when it has none."""
    return normalized_topic((front or {}).get(PlanKey.TOPIC.key, ""))


def set_topic(path: Path, topic: str) -> None:
    """Write TOPIC as PATH's `topic`, replacing the key or adding it last in the front matter; empty removes the key.

    Every other line is kept. A plan without front matter has no place for it
    and is refused. TOPIC is normalized here, so the plan never holds another
    form.
    """
    topic = checked_topic(topic)

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
