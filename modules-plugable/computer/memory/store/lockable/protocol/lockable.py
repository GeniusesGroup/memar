#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The optional capability `lockable` of a store: `lock` and `unlock` of an address, with a lease.

The Python form of `lockable.kh` beside it, for an address of the store contract
(`modules/computer/memory/store/protocol/store.py`) rather than a record id. A store that can hold an address
exclusively declares `Capability.LOCKABLE` and is a `Lockable`; the holder is the handle that locked, the `Locker` of
`modules/process/sync/` with a lease, so a holder that dies or forgets releases the address when its lease lapses. The
default control of concurrent writers stays the expectation of a batch (owner, 2026-10-25). `lease` is the store's
limit, in seconds, after which a lock its holder has not unlocked lapses.
"""
from __future__ import annotations
from importlib import import_module
from typing import Protocol, runtime_checkable
_m_store = import_module('modules.computer.memory.store.protocol.store')

@runtime_checkable
class Lockable(Protocol):
    lease: float

    def lock(self, address: bytes) -> _m_store.Read | _m_store.Refused:
        """Wait until this handle holds the address, then answer what it holds, as `get` would."""

    def unlock(self, address: bytes, value: bytes | None) -> _m_store.BatchAnswer:
        """Write the value, when one is given, and release the address; Conflict when this handle no longer holds it."""
