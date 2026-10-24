#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/entry_section.py — the content sections of a changelog entry: the one every entry has, then the optional catalog, declared once.

[Documentation — Changelog](../changelog.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.documentation.primitive.section import Section

class EntrySection(Section):
    WHAT_CHANGED = ('What changed', 'the change itself, as structured statements')
    CONSIDERED_AND_NOT_DONE = ('Considered and not done', 'alternatives examined and not applied in this change, each with its reason')
    SURVEYED = ('Surveyed', 'what was checked, against what, and what the check found')
    EXAMINED_AND_NOT_ADOPTED = ('Examined and not adopted', 'material examined against the artifact and deliberately not carried, with the reason')
    RELATED_WORK = ('Related work', 'comparative surveys of how other projects organize the same problem')
    DELIBERATION = ('Deliberation', 'the chronology of positions in a multi-participant task')
    DECISION = ('Decision', 'the final ruling on what was and was not applied')
