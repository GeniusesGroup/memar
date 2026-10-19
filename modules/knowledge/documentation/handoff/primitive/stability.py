#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/stability.py — the stability a handoff marks on every assumption, declared once.

[Documentation — Handoff](../handoff.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.word import Word


class Stability(Word):
    STRONG = ("Strong", "unlikely to change")
    WEAK = ("Weak", "may well change")
    UNEXAMINED = ("Unexamined", "taken as given and not looked at")
