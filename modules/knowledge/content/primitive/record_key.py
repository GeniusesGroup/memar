#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations

class RecordKey:
    __slots__ = ('key', 'description', 'earlier', '_written')

    def __init__(self, key: str, description: str, written: str | None=None, earlier: tuple[str, ...]=()) -> None:
        self.key = key
        self.description = description
        self.earlier = earlier
        self._written = written

    @property
    def written(self) -> str:
        return self._written or self.key.capitalize()

START_DATE_FIELD = RecordKey('start date', "when the record was first written, UTC: a plan's time, an Explanation's date, e.g. 2026-10-08T13:20:34Z", 'Start Date', ('opened',))
ID_FIELD = RecordKey('id', "the id of the record, found inside the document; a task's for a plan and a report", 'ID', ('task',))
