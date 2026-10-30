#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum

class Unavailability(enum.Enum):
    NOT_HELD = 'NotHeld'
    UNREACHABLE = 'Unreachable'
    FAILED = 'Failed'

    def summary(self) -> str:
        return {Unavailability.NOT_HELD: 'the batch expects a value at, or writes, an address the adapter does not hold', Unavailability.UNREACHABLE: 'the adapter cannot decide, as when a shared store it must ask cannot be reached', Unavailability.FAILED: 'the adapter could not finish and has made sure the batch can no longer commit'}[self]

class Refusal(enum.Enum):
    MALFORMED = 'Malformed'
    TOO_LARGE = 'TooLarge'
    NOT_ATOMIC = 'NotAtomic'

    def summary(self) -> str:
        return {Refusal.MALFORMED: 'the input breaks a rule of the contract or of the instantiation', Refusal.TOO_LARGE: 'the batch exceeds a limit the adapter declares', Refusal.NOT_ATOMIC: 'the batch needs an atomicity the adapter does not declare'}[self]

class Raised(Exception):

    def __init__(self, reason: Unavailability | Refusal, detail: str='') -> None:
        super().__init__(reason.value, detail)
        self.reason = reason
        self.detail = detail
