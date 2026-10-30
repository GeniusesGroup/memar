#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_errors = import_module('modules.computer.memory.store.errors.errors')
Raised = _m_errors.Raised
Refusal = _m_errors.Refusal
Unavailability = _m_errors.Unavailability

class BadReference(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'A reference the adapter may not keep a store in'

class ReferenceCollision(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'The reference of a class is a folder of the reference of another'

class NotInRepository(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'The project is not in a git repository'

class BadParameter(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'A key of the adapter is not class equals value pairs separated by commas, each class once, or holds a value it does not know'

class Lost(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Unavailability.FAILED, detail)

    def summary(self) -> str:
        return 'A long lived git process ended or answered what cannot be used'

class NotFastForward(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'The shared store refused a push because another writer published to the same reference first'
