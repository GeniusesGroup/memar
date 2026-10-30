#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from typing import Protocol, runtime_checkable
_m_store = import_module('modules.computer.memory.store.protocol.store')

@runtime_checkable
class Lockable(Protocol):
    lease: float

    def lock(self, address: bytes) -> _m_store.Read | _m_store.Refused:
        ...

    def unlock(self, address: bytes, value: bytes | None) -> _m_store.BatchAnswer:
        ...
