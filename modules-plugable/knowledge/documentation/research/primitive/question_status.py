#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/question_status.py — the standing of one question of a research, declared once.

[Documentation — Research](../research.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.word import Word


class QuestionStatus(Word):
    OPEN = ("Open", "not yet answered")
    ANSWERED = ("Answered", "answered, even before the conclusion is written")
    WITHDRAWN = ("Withdrawn", "dissolved: its premise was invalidated, or it merged into another")
