#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/protocol/labels/topics.py — the topic that names this module, declared by it.

A topic that names a module is a reference to that module, declared by the
module itself ([Label → Where labels are declared](../../label/label.md#where-labels-are-declared)).
"""
from __future__ import annotations
from modules.knowledge.label.primitive.topic import topic
LABELS = (
    topic('protocol', '01a19249-6472-7b5a-abf6-cba2a3e7921c', 'Work on the protocol module itself: what a protocol is, how a protocol is written.'),
)
