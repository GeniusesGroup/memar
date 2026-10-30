#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import enum
import hashlib
from importlib import import_module
from dataclasses import dataclass, field
from typing import Callable, Protocol, Sequence, Union, runtime_checkable
_m_errors = import_module('modules.computer.memory.store.errors.errors')
Refusal = _m_errors.Refusal
Unavailability = _m_errors.Unavailability

def token(value: bytes) -> bytes:
    return hashlib.sha256(value).digest()

class Capability(enum.Enum):
    ATOMIC_BATCH = 'atomic_batch'
    DURABLE = 'durable'
    SHARED_BETWEEN_PROCESSES = 'shared_between_processes'
    FALLBACK = 'fallback'
    LEAVES_WORKING_TREE_UNTOUCHED = 'leaves_working_tree_untouched'
    LOCKABLE = 'lockable'
    REPLICATED = 'replicated'

    def summary(self) -> str:
        return _CAPABILITY_SUMMARIES[self]
_CAPABILITY_SUMMARIES = {Capability.ATOMIC_BATCH: 'a batch of more than one write, or with expectations on more than one address, is applied atomically', Capability.DURABLE: 'a committed batch survives the abrupt end of the process that wrote it', Capability.SHARED_BETWEEN_PROCESSES: 'several processes may use one store at once', Capability.FALLBACK: 'the adapter asks a shared store for an address it does not hold', Capability.LEAVES_WORKING_TREE_UNTOUCHED: "the adapter keeps nothing in the project's working tree and changes no file it tracks or shows", Capability.LOCKABLE: 'the store offers the optional `Lock` and `Unlock` of an address, with a lease', Capability.REPLICATED: 'every committed batch is published to a shared store soon after it commits'}

@dataclass(frozen=True)
class Parameters:
    address_length: int | None = None
    dense: bool = False
    capacity: int | None = None
    value_length: int | None = None
    compare_and_write: bool = True

    def unwritten(self) -> bytes:
        return bytes(self.value_length or 0)

@dataclass(frozen=True)
class Limits:
    writes_per_batch: int | None = None
    bytes_per_batch: int | None = None
    bytes_per_value: int | None = None

@dataclass(frozen=True)
class Stats:
    processes_started: int = 0
    files_opened: int = 0

@dataclass(frozen=True)
class Found:
    value: bytes
    token: bytes

@dataclass(frozen=True)
class Absent:
    pass

ABSENT = Absent()

@dataclass(frozen=True)
class Unavailable:
    reason: Unavailability

@dataclass(frozen=True)
class Refused:
    reason: Refusal
    detail: str = field(default='', compare=False)

@dataclass(frozen=True)
class Conflict:
    index: int

@dataclass(frozen=True)
class Committed:
    pass
Expectation = Union[bytes, Absent]
Read = Union[Found, Absent, Unavailable]
BatchAnswer = Union[Refused, Unavailable, Conflict, Committed]

@runtime_checkable
class Store(Protocol):
    parameters: Parameters
    limits: Limits
    capabilities: frozenset[Capability]

    def get(self, addresses: Sequence[bytes]) -> list[Read] | Refused:
        ...

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> tuple[bytes, ...] | Unavailable | Refused:
        ...

    def batch(self, expect: Sequence[tuple[bytes, Expectation]], write: Sequence[tuple[bytes, bytes]]) -> BatchAnswer:
        ...

    def state(self) -> bytes:
        ...

    def changes(self, since: bytes) -> tuple[bytes, ...] | Refused:
        ...

    def stats(self) -> Stats:
        ...

@runtime_checkable
class Seam(Protocol):

    def at_commit_point(self, hook: Callable[[], None] | None) -> None:
        ...

    def drop_derived_structures(self) -> None:
        ...
