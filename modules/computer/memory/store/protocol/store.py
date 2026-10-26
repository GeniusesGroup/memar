#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The store contract: a store of bytes under addresses, read by `get` and `list`, written only by an atomic `batch`.

The one source of the contract's signatures, answers, parameters, limits and capability names; what each means, and
why, is [Memory Store](../store.md). It is written in Python because the tooling is, and becomes a Khayyam capsule later.

An address is a byte string with equality and the byte order ([Memory Address](../../address/address.md)); its length
is fixed or any, as the instantiation's `Parameters` say. A value is a byte string; a value found carries its token,
the SHA-256 of its bytes, and an expectation of a batch is a token or `ABSENT`. What a thing says of itself is its
`summary`, after `Summary` of `modules/computer/type/protocol/detail.kh`.
"""
from __future__ import annotations
import enum
import hashlib
from dataclasses import dataclass, field
from typing import Callable, Protocol, Sequence, Union, runtime_checkable

def token(value: bytes) -> bytes:
    """The token of a value: the SHA-256 of its bytes, the same in every adapter."""
    return hashlib.sha256(value).digest()

class Capability(enum.Enum):
    """What an adapter declares, once, of what it is; the suite runs the group each one calls for."""
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
    """The kind of address and the three properties a store is instantiated with.

    `address_length` is the fixed length of an address, or None for any length. A `dense` store holds a value at every
    address of its capacity, the first `capacity` addresses of `address_length` bytes in byte order (the integers below
    `capacity`, big-endian), so nothing reads Absent and `list` answers that range; a sparse store holds what was written.
    `value_length` is the fixed length of a value, or None for any length. `compare_and_write` says whether the medium can
    compare and write one address atomically, which an expectation needs.
    """
    address_length: int | None = None
    dense: bool = False
    capacity: int | None = None
    value_length: int | None = None
    compare_and_write: bool = True

    def unwritten(self) -> bytes:
        """What an address of a dense store that was never written holds: zero bytes of the fixed length, or none."""
        return bytes(self.value_length or 0)

@dataclass(frozen=True)
class Limits:
    """The limits an adapter declares; None is no limit. Bytes per batch is the sum of the lengths of the values written."""
    writes_per_batch: int | None = None
    bytes_per_batch: int | None = None
    bytes_per_value: int | None = None

@dataclass(frozen=True)
class Stats:
    """What the medium has cost since the store was opened, for an adapter whose medium costs either."""
    processes_started: int = 0
    files_opened: int = 0

class Refusal(enum.Enum):
    """Why a call or a batch is Refused: it is malformed, it exceeds a declared limit, or it needs an atomicity not declared."""
    MALFORMED = 'Malformed'
    TOO_LARGE = 'TooLarge'
    NOT_ATOMIC = 'NotAtomic'

    def summary(self) -> str:
        return {Refusal.MALFORMED: 'the input breaks a rule of the contract or of the instantiation', Refusal.TOO_LARGE: 'the batch exceeds a limit the adapter declares', Refusal.NOT_ATOMIC: 'the batch needs an atomicity the adapter does not declare'}[self]

class Unavailability(enum.Enum):
    """Why an answer is Unavailable: nothing was applied, and the fate of the input is settled."""
    NOT_HELD = 'NotHeld'
    UNREACHABLE = 'Unreachable'
    FAILED = 'Failed'

    def summary(self) -> str:
        return {Unavailability.NOT_HELD: 'the batch expects a value at, or writes, an address the adapter does not hold', Unavailability.UNREACHABLE: 'the adapter cannot decide, as when a shared store it must ask cannot be reached', Unavailability.FAILED: 'the adapter could not finish and has made sure the batch can no longer commit'}[self]

@dataclass(frozen=True)
class Found:
    value: bytes
    token: bytes

@dataclass(frozen=True)
class Absent:
    """The answer that nothing is held at an address, and, as `ABSENT`, the expectation that nothing is."""

ABSENT = Absent()

@dataclass(frozen=True)
class Unavailable:
    reason: Unavailability

@dataclass(frozen=True)
class Refused:
    """The input is refused as a whole and nothing is applied; `detail` says which rule, for a reader, and is no part of the answer."""
    reason: Refusal
    detail: str = field(default='', compare=False)

@dataclass(frozen=True)
class Conflict:
    """An expectation failed: `index` is the first failing one, in the order given; nothing is applied."""
    index: int

@dataclass(frozen=True)
class Committed:
    """Every write of the batch is applied."""
Expectation = Union[bytes, Absent]
Read = Union[Found, Absent, Unavailable]
BatchAnswer = Union[Refused, Unavailable, Conflict, Committed]

@runtime_checkable
class Store(Protocol):
    """A store of bytes under addresses. Every adapter realizes these, with the answers [Memory Store](../store.md) states."""
    parameters: Parameters
    limits: Limits
    capabilities: frozenset[Capability]

    def get(self, addresses: Sequence[bytes]) -> list[Read] | Refused:
        """One answer for each address, in the order given: Found, Absent, or Unavailable."""

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False) -> tuple[bytes, ...] | Unavailable | Refused:
        """The first `min(limit, n)` held addresses of `[from_, to)` after `after`, ascending; descending, the last ones before `after`."""

    def batch(self, expect: Sequence[tuple[bytes, Expectation]], write: Sequence[tuple[bytes, bytes]]) -> BatchAnswer:
        """Apply every write only if every expectation holds; the first answer that applies, in the order Refused, Unavailable, Conflict, Committed."""

    def state(self) -> bytes:
        """A token of the committed state, which changes when a batch commits and at no other time."""

    def changes(self, since: bytes) -> tuple[bytes, ...] | Refused:
        """The addresses written by the batches committed between the state `since` and now, ascending, each once."""

    def stats(self) -> Stats:
        """The processes started and the files opened since the store was opened."""

@runtime_checkable
class Seam(Protocol):
    """What every adapter exposes for tests: a hook run at the commit point, after a batch's expectations are checked and
    before it commits. A hook that returns lets the batch commit; one that raises makes it answer Unavailable with the
    reason Failed, applied nowhere. The suite pauses a writer with a hook that waits. `drop_derived_structures` deletes
    every structure the adapter derives from the store, which changes no answer."""

    def at_commit_point(self, hook: Callable[[], None] | None) -> None:
        ...

    def drop_derived_structures(self) -> None:
        ...
