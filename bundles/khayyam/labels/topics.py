#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""bundles/khayyam/labels/topics.py — the topic that names this bundle, declared by it.

A topic that names a module is a reference to that module, declared by the
module itself ([Label → Where labels are declared](../../../modules/knowledge/label/label.md#where-labels-are-declared)).
"""
from __future__ import annotations
from modules.knowledge.documentation.plan.labels.topic import topic
LABELS = (
    topic('khayyam', '01a14a13-19e7-74d9-ba0b-8335ceaab682', 'Work on the Khayyam language and its toolchain: compiler, language server and targets.'),
)
