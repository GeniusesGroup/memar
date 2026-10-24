#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/practice_key.py — the front-matter keys of a Practice-facet document, declared once.

[Documentation — Practice](../practice.md) names exactly two, both required and
written in lower case, as the skill conventions it follows write them. They are
a closed set, so they are code and are written here and nowhere else
([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations
from modules.knowledge.content.primitive.record_key import RecordKey

class PracticeKey(RecordKey):
    NAME = ('name', "the skill's name, lowercase with hyphens, and the name of the file it heads", 'name')
    DESCRIPTION = ('description', 'what the skill does and when to use it: the only thing an agent sees before it triggers', 'description')
