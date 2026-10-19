#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/confidence.py — the confidence a handoff marks on every decision, declared once.

[Documentation — Handoff](../handoff.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.word import Word


class Confidence(Word):
    DECIDED = ("Decided", "settled, with its reasoning")
    TENTATIVE = ("Tentative", "assumed meanwhile, to firm up or be dropped")
    EXPLORED_BUT_UNRESOLVED = ("Explored-but-unresolved", "looked into and not settled")
    DEFERRED = ("Deferred", "set aside on purpose")
