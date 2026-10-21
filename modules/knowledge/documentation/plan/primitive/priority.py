#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/plan/primitive/priority.py — a plan's priority, declared once: how soon a queued task is taken.

A whole number from 1 to 10, the higher sooner. It is a type so that the
bounds, the default and the words a help prints about them are written here and
nowhere else ([A Fact in Code Is Written Once](../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)):
`session_plan_priority` reads and writes the key by it, `session_claims` ranks
by it, and the help of `new` and `priority` call `range_words` and
`default_words`.

A plan that writes none has the middle value, so every plan written before
priorities existed waits as an ordinary task; a value that is not a number in
range reads as the middle too, since a plan is scratch a person edits by hand
and one typo must not stop the line (`of`). A value a person types to a command
is another matter and is refused (`checked`).
"""
from __future__ import annotations
from typing import ClassVar
from machine.console import fail
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey

class Priority(int):
    """A plan's priority: a whole number from `LOWEST` to `HIGHEST`, the higher sooner."""
    LOWEST: ClassVar[Priority]
    HIGHEST: ClassVar[Priority]
    DEFAULT: ClassVar[Priority]

    @classmethod
    def read(cls, text: str) -> Priority | None:
        """TEXT as a priority, or None when it is not a whole number within the bounds."""
        text = text.strip()
        if not text.isdigit():
            return None
        number = int(text)
        return cls(number) if cls.LOWEST <= number <= cls.HIGHEST else None

    @classmethod
    def of(cls, front: dict[str, str] | None) -> Priority:
        """The priority FRONT matter gives its plan: its `priority`, or `DEFAULT` when absent or not in range."""
        found = cls.read((front or {}).get(PlanKey.PRIORITY.key, ''))
        return cls.DEFAULT if found is None else found

    @classmethod
    def checked(cls, value: str | int) -> Priority:
        """VALUE as a priority; refused when it is not a whole number within the bounds."""
        found = cls.read(str(value))
        if found is None:
            fail(f'a priority is a whole number from {cls.range_words()}, the higher sooner; {value!r} is not one')
        return found

    @classmethod
    def range_words(cls) -> str:
        """The range as a help says it: `1 to 10`."""
        return f'{cls.LOWEST} to {cls.HIGHEST}'

    @classmethod
    def default_words(cls) -> str:
        """What a plan without one counts as, as a help says it."""
        return f'a plan without one counts as {cls.DEFAULT}'
Priority.LOWEST = Priority(1)
Priority.HIGHEST = Priority(10)
Priority.DEFAULT = Priority(5)
