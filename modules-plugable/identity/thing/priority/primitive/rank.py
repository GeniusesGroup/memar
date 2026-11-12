#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from typing import ClassVar
from machine.console import fail

class Priority_Rank(int):
    LOWEST: ClassVar[Priority_Rank]
    HIGHEST: ClassVar[Priority_Rank]
    TYPE_UUID = 'ef475e97-7f2a-5378-b6ab-a5e6823c540a'

    @classmethod
    def read(cls, text: str) -> Priority_Rank | None:
        text = text.strip()
        if not text.isdigit():
            return None
        number = int(text)
        return cls(number) if cls.LOWEST <= number <= cls.HIGHEST else None

    @classmethod
    def checked(cls, value: str | int) -> Priority_Rank:
        found = cls.read(str(value))
        if found is None:
            fail(f'a priority rank is a whole number from {cls.LOWEST} to {cls.HIGHEST}; {value!r} is not one')
        return found

    @classmethod
    def of_absent(cls) -> Priority_Rank:
        return cls.LOWEST

    @classmethod
    def listing(cls) -> str:
        return f'{cls.LOWEST} to {cls.HIGHEST}'

Priority_Rank.LOWEST = Priority_Rank(1)
Priority_Rank.HIGHEST = Priority_Rank(10)
