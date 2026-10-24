#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/goal_status.py — the standing of one goal of a research, declared once.

[Documentation — Research](../research.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class GoalStatus(Word):
    MET = ('Met', 'the inquiry delivered it')
    PARTIALLY_MET = ('Partially met', 'the inquiry delivered part of it')
    UNMET = ('Unmet', 'the inquiry did not deliver it')
    DROPPED = ('Dropped', 'no longer sought')
