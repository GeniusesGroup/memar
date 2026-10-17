#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/topic.py — a plan's topic, declared once: the one subject `claims` batches by.

One value, not several: a task with two subjects is two tasks, and one value
keeps "the same topic" a plain equality. It is free text normalized when
written (lower case, runs of white space as one hyphen), not a list the project
keeps, because a kept list is a second thing to maintain and would stop a new
subject at the moment it appears. A typo that splits one subject in two is met
by showing the topics in use and by warning of a near match (`session_topic`).
A plan without a topic has none, and none is not a topic of its own.

It is a type so that the rule of normalizing and the check of a one-line value
are written here and nowhere else
([A Fact in Code Is Written Once](../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations

from machine.console import fail
from services.session_record import PlanKey


class Topic(str):
    """A plan's topic: lower case, each run of white space one hyphen; empty when the plan has none."""

    @classmethod
    def normalized(cls, text: str) -> Topic:
        """TEXT as a topic: stripped, lower case, each run of white space one hyphen; empty when nothing is left."""
        return cls("-".join(text.lower().split()))

    @classmethod
    def checked(cls, text: str) -> Topic:
        """TEXT as a topic, normalized; refused when it holds a line break, since a topic is a one-line front-matter value."""
        if "\n" in text or "\r" in text:
            fail("a topic is one line; this one holds a line break")
        return cls.normalized(text)

    @classmethod
    def of(cls, front: dict[str, str] | None) -> Topic:
        """The topic FRONT matter gives its plan, normalized; empty when it has none."""
        return cls.normalized((front or {}).get(PlanKey.TOPIC.key, ""))
