#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
from importlib import import_module
_m_errors = import_module('modules.computer.memory.store.errors.errors')
Raised = _m_errors.Raised
Refusal = _m_errors.Refusal

class Bad(enum.Enum):
    LAYOUT = 'BadLayout'
    LIMIT = 'BadLimit'
    REF = 'BadRef'
    PATTERN = 'BadPattern'
    EDGE = 'BadEdge'

    def summary(self) -> str:
        return {Bad.LAYOUT: 'a layout that does not match the bound layout for the relation', Bad.LIMIT: 'a limit below one', Bad.REF: 'a side_ref that is not of the form or is not held', Bad.PATTERN: 'a pattern that is not of the form', Bad.EDGE: 'an edge that is not of the form'}[self]

class NotLayable(Raised, ValueError):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'graph is laid over a sparse store of any address and value length'
