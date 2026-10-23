#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/plan_part.py — the parts under a task plan's front matter, in order, declared once.

[Documentation — Plan](../plan.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.documentation.primitive.section import Section

class PlanPart(Section):
    REQUEST = ('Request', 'what was asked, and what checks it is done')
    WHY = ('Why', "the reason, in the writer's own words")
    STEPS = ('Steps', 'each step, local or delegated')
    NEXT = ('Next', 'what the next task does first')

    @classmethod
    def every_plan(cls) -> tuple[str, ...]:
        """The headings every plan has, in order."""
        return cls.headings()
