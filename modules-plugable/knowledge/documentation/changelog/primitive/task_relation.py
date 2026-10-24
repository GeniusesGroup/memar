#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/task_relation.py — how a change relates to an external task, declared once.

[Documentation — Changelog](../changelog.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class TaskRelation(Word):
    CLOSED = ('Closed', 'this change completes the task')
    PARTIAL = ('Partial', 'this change is progress toward the task but does not complete it')
    REFERENCE = ('Reference', 'mentioned for context, with no completion claim either way')
