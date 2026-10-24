#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/explanation_key.py — the front-matter keys of an Explanation-facet document, declared once.

[Documentation — Explanation](../explanation.md) names four; they are a closed
set, so they are code and are written here and nowhere else
([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
`ID` and `Start Date` are the fields a task's plan and report share
(`primitive/record_key.py`); the Explanation's own value for each is the
specification's (an hour-count integer, a calendar date).
"""
from __future__ import annotations
from modules.knowledge.documentation.primitive.record_key import ID_FIELD, START_DATE_FIELD, RecordKey

class ExplanationKey(RecordKey):
    TITLE = ('title', 'a short, unique, human-readable name for the document, in double quotes', 'Title')
    STATUS = ('status', "the document's maturity: one of the Status words of an Explanation-facet document", 'Status')
    START_DATE = START_DATE_FIELD
    ID = ID_FIELD
