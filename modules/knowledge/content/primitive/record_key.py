#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/record_key.py — a front-matter key of a documentation record, declared once.

A record's keys are a closed set, so each is code ([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)):
a key is stored lower case, which is how callers ask for it, and written in
PascalCase, which for the one-word keys of the records is a capital. The facets
that declare a record's keys subclass `RecordKey` in their own `primitive/`
([PlanKey](../../../management/task/plan/primitive/plan_key.py), [ReportKey](../../../management/task/report/primitive/report_key.py)).
"""
from __future__ import annotations
from enum import Enum

class RecordKey(Enum):
    """A front-matter key: the (lower-case) key callers ask for, what it holds, how it is written, and its earlier names.

    The key is stored lower case, which is how callers ask for it. It is
    written in PascalCase, which for a one-word key is a capital; a key whose
    written form is otherwise (`ID`, `Start Date`) says so as the third item.
    The earlier names are those a file written before a rename still carries;
    they are read as the key and never written.
    """

    def __init__(self, key: str, description: str, written: str | None=None, earlier: tuple[str, ...]=()) -> None:
        self.key = key
        self.description = description
        self.earlier = earlier
        self._written = written

    @property
    def written(self) -> str:
        """The key as the front matter writes it."""
        return self._written or self.key.capitalize()
START_DATE_FIELD = ('start date', "when the record was first written, UTC: a plan's time, an Explanation's date, e.g. 2026-10-08T13:20:34Z", 'Start Date', ('opened',))
ID_FIELD = ('id', "the id of the record, found inside the document; a task's for a plan and a report", 'ID', ('task',))
