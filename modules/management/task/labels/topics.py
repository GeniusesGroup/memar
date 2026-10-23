#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/labels/topics.py — the topic that names this module, declared by it.

A topic that names a module is a reference to that module, declared by the
module itself ([Label → Where labels are declared](../../../knowledge/label/label.md#where-labels-are-declared)).
The streams of work an organization's tasks run are not this kernel module's:
they are declared in the task domain's pluggable part.
"""
from __future__ import annotations
from modules.knowledge.documentation.plan.labels.topic import topic
LABELS = (
    topic('task', '01a14aad-9352-77c5-970f-1bc2b884b5dc', 'Work on the task module itself: what a task is, its records and its verbs.'),
)
