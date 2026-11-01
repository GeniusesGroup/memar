#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_errors = import_module('modules.computer.memory.store.errors.errors')
Raised = _m_errors.Raised
Refusal = _m_errors.Refusal
Unavailability = _m_errors.Unavailability

class BadParameter(Exception):

    def __init__(self, detail: str='') -> None:
        super().__init__(detail)
        self.detail = detail

    def summary(self) -> str:
        return 'A files adapter parameter the manifest must not carry'

class BadAddress(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'An address the files path encoding cannot map'

class RootCollision(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'A memory root that nests inside another class\'s memory root'

class Lost(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Unavailability.FAILED, detail)

    def summary(self) -> str:
        return 'The files medium lost a committed batch the adapter expected to hold'

class BadBody(Raised):

    def __init__(self, detail: str='') -> None:
        super().__init__(Refusal.MALFORMED, detail)

    def summary(self) -> str:
        return 'A node file body the bound codec cannot unpack'

class BadCodec(BadParameter):

    def __init__(self, name: str='') -> None:
        super().__init__(name)

    def summary(self) -> str:
        return 'A files-body-codec name that is not registered'
