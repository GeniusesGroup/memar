#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/report_part.py — the parts under a session report's front matter, in order, and the hand-back part a session adds when it needs a decision, declared once.

[Documentation — Report](../report.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.section import Section


class ReportPart(Section):
    WHAT_RAN = ("What ran", "what was done")
    CHECK = ("Check", "what the task's own check found")
    RESULT = ("Result", "how the run ended, with its Status")
    LEFT_OPEN = ("Left open", "what the next party still has to do")
    DECISIONS_NEEDED = ("Decisions needed", "the decisions the session hands back; at most ten lines")

    @property
    def hand_back(self) -> bool:
        """Whether this is the part a session adds when it needs someone's decision, and not one every report has."""
        return self is ReportPart.DECISIONS_NEEDED

    @classmethod
    def every_report(cls) -> tuple[str, ...]:
        """The headings every report has, in order: all but the hand-back part."""
        return tuple(part.heading for part in cls if not part.hand_back)


HAND_BACK_MAX_LINES = 10
"""The most lines the hand-back part may hold for a report to be a hand-back."""
