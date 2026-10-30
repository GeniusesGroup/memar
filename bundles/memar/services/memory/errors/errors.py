#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
from dataclasses import dataclass, field

class OpeningRefusal(enum.Enum):
    NOT_BOUND = 'NotBound'
    LESS_THAN_NEEDED = 'LessThanNeeded'
    SHARED_STORE = 'SharedStore'
    MALFORMED = 'Malformed'

    def summary(self) -> str:
        return {OpeningRefusal.NOT_BOUND: "the project's `memory` key does not name the class", OpeningRefusal.LESS_THAN_NEEDED: 'the adapter declares less than the class needs, or keeps a store `record` cannot be laid over', OpeningRefusal.SHARED_STORE: 'another class is bound to the same store', OpeningRefusal.MALFORMED: "the project's `memory` key is not in its form, or names an adapter no module offers"}[self]

@dataclass(frozen=True)
class OpenRefused:
    reason: OpeningRefusal
    detail: str = field(default='', compare=False)
