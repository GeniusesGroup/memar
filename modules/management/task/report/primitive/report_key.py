#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/report_key.py — the front-matter keys of a task report, declared once.

[Documentation — Report](../report.md) names the keys a report's front matter
holds; they are a closed set, so they are code and are written here and nowhere
else ([A Fact in Code Is Written Once](../../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
A report has no key of its own for how the run ended: that is its Status with
the Result part, so the keys are the task's id, the Title and the Status. The
earlier shapes (an `Outcome` key, a `Stop:` line) are not part of today's
record; the services that name them, so that a reader is told why such a file is
not read, keep them.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.record_key import ID_FIELD, RecordKey

class ReportKey(RecordKey):
    ID = ID_FIELD
    TITLE = ('title', 'TITLE, when known')
    STATUS = ('status', 'empty until the task ends, then one of the Statuses a report may state')
