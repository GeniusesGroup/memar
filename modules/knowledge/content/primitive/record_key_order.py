#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from typing import Iterator
from modules.knowledge.content.primitive.record_key import RecordKey

class RecordKeyOrder(type):

    def __iter__(cls) -> Iterator[RecordKey]:
        return iter([value for value in vars(cls).values() if isinstance(value, RecordKey)])
