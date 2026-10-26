#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""`volatile`, the reference adapter of the store contract: a store kept in the memory of the process.

What it is and why it is kernel is [Memory Volatile](volatile.md); the contract it realizes is
`modules/computer/memory/store/protocol/store.py`. It is built with the parameters, the limits and the atomicity it is
given, so that the suite's model group can build it with another adapter's declarations. Its declared limits: whatever
`Parameters` and `Limits` it is built with; `atomic_batch` as given; not `durable`, not `shared_between_processes`,
no `fallback`, not `lockable`, not `replicated`. It keeps nothing outside the process, so it declares nothing of the
working tree either. Each `open()` is a new handle on the same memory; the handles of one memory are isolated by one
lock, and a batch paused at the commit point holds it. It keeps every committed batch's addresses, so `changes` answers
from any state it ever answered.
"""
from __future__ import annotations
import bisect
import os
import threading
from importlib import import_module
from typing import Callable, Sequence
_m_store = import_module('modules.computer.memory.store.protocol.store')
ABSENT = _m_store.ABSENT
Absent = _m_store.Absent
Capability = _m_store.Capability
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Stats = _m_store.Stats
Unavailability = _m_store.Unavailability
Unavailable = _m_store.Unavailable
token = _m_store.token
TOKEN_LENGTH = len(token(b''))

class _Memory:
    """What the handles of one store share: the values, the held addresses in order, and the addresses of each commit."""

    def __init__(self, parameters: Parameters) -> None:
        self.lock = threading.RLock()
        self.values: dict[bytes, bytes] = {}
        self.order: list[bytes] = [i.to_bytes(parameters.address_length, 'big') for i in range(parameters.capacity)] if parameters.dense else []
        self.commits: list[tuple[bytes, ...]] = []
        self.name = os.urandom(8)

class Volatile:
    """A store in the memory of the process; see the module's docstring for what it declares."""

    def __init__(self, parameters: Parameters=Parameters(), limits: Limits=Limits(), atomic_batch: bool=True, memory: _Memory | None=None) -> None:
        if parameters.dense and (not parameters.address_length or parameters.capacity is None or parameters.capacity > 256 ** parameters.address_length):
            raise ValueError('a dense store needs a fixed address length and a capacity the addresses can count')
        self.parameters = parameters
        self.limits = limits
        self.capabilities = frozenset({Capability.ATOMIC_BATCH} if atomic_batch else ())
        self._memory = memory or _Memory(parameters)
        self._hook: Callable[[], None] | None = None

    def open(self) -> 'Volatile':
        """A new handle on the same store."""
        return Volatile(self.parameters, self.limits, Capability.ATOMIC_BATCH in self.capabilities, self._memory)

    def _takes(self, at: object) -> bool:
        p = self.parameters
        if not isinstance(at, bytes) or (p.address_length is not None and len(at) != p.address_length):
            return False
        return not p.dense or int.from_bytes(at, 'big') < p.capacity

    def _read(self, at: bytes):
        held = self._memory.values.get(at)
        if held is None:
            if not self.parameters.dense:
                return ABSENT
            held = self.parameters.unwritten()
        return Found(held, token(held))

    def get(self, addresses: Sequence[bytes]):
        if not all((self._takes(at) for at in addresses)):
            return Refused(Refusal.MALFORMED, 'an address the store does not take')
        with self._memory.lock:
            return [self._read(at) for at in addresses]

    def list(self, from_: bytes | None=None, to: bytes | None=None, after: bytes | None=None, limit: int | None=None, descending: bool=False):
        if limit is not None and limit < 1:
            return Refused(Refusal.MALFORMED, 'a limit below one')
        if from_ is not None and to is not None and (from_ > to):
            return Refused(Refusal.MALFORMED, 'a from after a to')
        with self._memory.lock:
            order = self._memory.order
            low = bisect.bisect_left(order, from_) if from_ is not None else 0
            high = bisect.bisect_left(order, to) if to is not None else len(order)
            if descending:
                if after is not None:
                    high = min(high, bisect.bisect_left(order, after))
                start = low if limit is None else max(low, high - limit)
                return tuple(reversed(order[start:high])) if start < high else ()
            if after is not None:
                low = max(low, bisect.bisect_right(order, after))
            end = high if limit is None else min(high, low + limit)
            return tuple(order[low:end]) if low < end else ()

    def _refusal(self, expect: Sequence, write: Sequence):
        p, limits = (self.parameters, self.limits)
        if not write:
            return Refused(Refusal.MALFORMED, 'a batch with no write')
        written = [at for at, _ in write]
        expected = [at for at, _ in expect]
        if len(set(written)) != len(written) or len(set(expected)) != len(expected):
            return Refused(Refusal.MALFORMED, 'an address written twice or expected twice')
        if not all((self._takes(at) for at in written + expected)):
            return Refused(Refusal.MALFORMED, 'an address the store does not take')
        if not all((isinstance(data, bytes) for _, data in write)):
            return Refused(Refusal.MALFORMED, 'a value that is not bytes')
        if not all((isinstance(e, Absent) or (isinstance(e, bytes) and len(e) == TOKEN_LENGTH) for _, e in expect)):
            return Refused(Refusal.MALFORMED, 'an expectation that is neither a token nor absent')
        if p.value_length is not None and any((len(data) != p.value_length for _, data in write)):
            return Refused(Refusal.MALFORMED, 'a value of another length than the fixed one')
        if limits.writes_per_batch is not None and len(write) > limits.writes_per_batch:
            return Refused(Refusal.TOO_LARGE, 'writes per batch')
        if limits.bytes_per_value is not None and any((len(data) > limits.bytes_per_value for _, data in write)):
            return Refused(Refusal.TOO_LARGE, 'bytes per value')
        if limits.bytes_per_batch is not None and sum((len(data) for _, data in write)) > limits.bytes_per_batch:
            return Refused(Refusal.TOO_LARGE, 'bytes per batch')
        if expect and (not p.compare_and_write):
            return Refused(Refusal.NOT_ATOMIC, 'an expectation on a store that cannot compare and write')
        if Capability.ATOMIC_BATCH not in self.capabilities and (len(write) > 1 or any((at != written[0] for at in expected))):
            return Refused(Refusal.NOT_ATOMIC, 'more than one address on a store that is not atomic')
        return None

    def batch(self, expect: Sequence, write: Sequence):
        refused = self._refusal(expect, write)
        if refused:
            return refused
        memory = self._memory
        with memory.lock:
            for index, (at, expectation) in enumerate(expect):
                found = self._read(at)
                holds = isinstance(found, Absent) if isinstance(expectation, Absent) else isinstance(found, Found) and found.token == expectation
                if not holds:
                    return Conflict(index)
            if self._hook is not None:
                try:
                    self._hook()
                except Exception:
                    return Unavailable(Unavailability.FAILED)
            for at, data in write:
                if at not in memory.values and (not self.parameters.dense):
                    bisect.insort(memory.order, at)
                memory.values[at] = bytes(data)
            memory.commits.append(tuple(sorted({at for at, _ in write})))
            return Committed()

    def state(self) -> bytes:
        with self._memory.lock:
            return self._memory.name + len(self._memory.commits).to_bytes(8, 'big')

    def changes(self, since: bytes):
        memory = self._memory
        with memory.lock:
            count = int.from_bytes(since[8:], 'big') if len(since) == 16 and since[:8] == memory.name else -1
            if not 0 <= count <= len(memory.commits):
                return Refused(Refusal.MALFORMED, 'a state this store never answered')
            return tuple(sorted({at for commit in memory.commits[count:] for at in commit}))

    def stats(self) -> Stats:
        return Stats()

    def at_commit_point(self, hook: Callable[[], None] | None) -> None:
        self._hook = hook

    def drop_derived_structures(self) -> None:
        """`volatile` derives nothing from its values that it does not update in the same step."""
