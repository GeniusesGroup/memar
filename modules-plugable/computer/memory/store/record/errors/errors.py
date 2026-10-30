#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
from importlib import import_module
_m_errors = import_module('modules.computer.memory.store.errors.errors')
Raised = _m_errors.Raised
Refusal = _m_errors.Refusal

class Bad(enum.Enum):
    KEY = 'BadKey'
    ID = 'BadID'
    LABELS = 'BadLabels'
    INSTANT = 'BadInstant'
    BOUNDS = 'BadBounds'
    LIMIT = 'BadLimit'
    ALL_OF = 'BadAllOf'

    def summary(self) -> str:
        return {Bad.KEY: 'a key whose id or domain key is not of the form', Bad.ID: 'an id that is not of the form', Bad.LABELS: 'a `labels` part that is not ids ascending without repetition', Bad.INSTANT: 'an instant that is not a whole number of milliseconds of six bytes', Bad.BOUNDS: 'a from after a to', Bad.LIMIT: 'a limit below one', Bad.ALL_OF: 'an all_of that is empty or holds what is not an id'}[self]

class NotLayable(Raised, ValueError):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'record is laid over a sparse store of any address and value length'
