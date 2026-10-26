#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The conformance suite of the store contract: the cases that decide whether an adapter keeps it, and their runner.

The subject is the store contract of [Memory Store](../store/store.md) as `store/protocol/store.py` writes it; why the
suite is a module of its own, and which cases are the contract's and which a capsule's, is
[Memory Conformance](conformance.md). Each case below is one function whose docstring states it; its name is the
case's name with hyphens. A case whose docstring carries `owed:memory.port.contract-suite` is pending: it is written
and runs only for an adapter declaring its capability, and no adapter that declares it has run it yet. Since
2026-10-26 every case here runs on `git-store`, and none carries the mark; the pending ones are `lockable`'s.

An adapter's own `tests/` call `test_case(make)`, `make` returning a new, empty adapter each time it is called: an
object whose `open()` opens a store, each call a new handle on the same store. The runner gives each case its own
adapter and runs the cases each store's parameters and capabilities call for; a capability declared by a pluggable
module brings its own `Case`s in `cases`. A case that reaches another process asks the adapter for `opener()`, the
dotted module, the function and the keyword arguments that open the same adapter in a child, and runs this file there
as `python conformance.py child ...`.
"""
from __future__ import annotations
import hashlib
import json
import random
import subprocess
import sys
import threading
import time
import unittest
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Protocol
HERE = Path(__file__).resolve().parent
TOP = next((p for p in HERE.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
if str(TOP) not in sys.path:
    sys.path.insert(0, str(TOP))
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
ABSENT = _m_store.ABSENT
Absent = _m_store.Absent
Capability = _m_store.Capability
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Seam = _m_store.Seam
Unavailability = _m_store.Unavailability
Unavailable = _m_store.Unavailable
token = _m_store.token
Volatile = _m_volatile.Volatile
OWED = 'owed:memory.port.contract-suite'

class Adapter(Protocol):
    """What the suite takes as input: each `open()` a new handle on one store."""

    def open(self) -> Any:
        ...

@dataclass(frozen=True)
class Case:
    """One case: its group (the capability or parameter that calls for it), when it applies to a store, and its check."""
    group: str
    applies: Callable[[Any], bool]
    check: Callable[[unittest.TestCase, Callable[[], Adapter]], None]

    @property
    def name(self) -> str:
        return self.check.__name__.replace('_', '-')
CASES: list[Case] = []

def case(group: str, applies: Callable[[Any], bool]=lambda store: True) -> Callable:

    def register(check: Callable) -> Callable:
        CASES.append(Case(group, applies, check))
        return check
    return register

def test_case(make: Callable[[], Adapter], cases: list[Case] | None=None) -> type[unittest.TestCase]:
    """A TestCase class with one test for each case that applies to the stores `make` opens."""
    probe = make().open()
    attributes: dict[str, Any] = {}
    for each in CASES + list(cases or ()):
        if not each.applies(probe):
            continue

        def method(self: unittest.TestCase, check: Callable=each.check) -> None:
            check(self, make)
        method.__doc__ = each.check.__doc__
        attributes['test_' + each.check.__name__] = method
    return type('Conformance', (unittest.TestCase,), attributes)

def applied(store: Any, cases: list[Case] | None=None) -> set[str]:
    """The names of the cases that apply to a store."""
    return {each.name for each in CASES + list(cases or ()) if each.applies(store)}

def sparse(store: Any) -> bool:
    return not store.parameters.dense

def comparing(store: Any) -> bool:
    return store.parameters.compare_and_write

def atomic(store: Any) -> bool:
    return Capability.ATOMIC_BATCH in store.capabilities

def address(store: Any, i: int) -> bytes:
    """The i-th address of the cases: within the capacity of a dense store, of the fixed length when one is declared."""
    length = store.parameters.address_length
    if store.parameters.dense:
        i %= store.parameters.capacity
    if length:
        return i.to_bytes(length, 'big')
    return b'k' + i.to_bytes(4, 'big')

def value(store: Any, seed: int, length: int=8) -> bytes:
    """A value made from a seed, of the fixed length when one is declared."""
    size = store.parameters.value_length if store.parameters.value_length is not None else length
    block = token(seed.to_bytes(8, 'big'))
    return (block * (size // len(block) + 1))[:size]

def other_size(store: Any) -> int:
    return store.parameters.value_length + 1

def get1(store: Any, at: bytes) -> Any:
    return store.get([at])[0]

def put(t: unittest.TestCase, store: Any, at: bytes, data: bytes) -> None:
    t.assertEqual(store.batch([], [(at, data)]), Committed())

def snapshot(store: Any, addresses: list[bytes]) -> list[Any]:
    return store.get(addresses)

def limit_ok(store: Any, length: int) -> bool:
    most = store.limits.bytes_per_value
    batch = store.limits.bytes_per_batch
    return (most is None or length <= most) and (batch is None or length <= batch)

def write_in_batches(t: unittest.TestCase, store: Any, writes: list[tuple[bytes, bytes]]) -> None:
    per = store.limits.writes_per_batch or 100
    if not atomic(store):
        per = 1
    if store.limits.bytes_per_batch:
        per = max(1, min(per, store.limits.bytes_per_batch // max(1, max((len(v) for _, v in writes)))))
    for start in range(0, len(writes), per):
        t.assertEqual(store.batch([], writes[start:start + per]), Committed())

@case('core', sparse)
def get_absent(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`get-absent`: an address never written reads Absent, and an empty value written reads Found with an empty value."""
    store = make().open()
    t.assertEqual(store.get([address(store, 1)]), [ABSENT])
    if store.parameters.value_length in (None, 0):
        put(t, store, address(store, 2), b'')
        t.assertEqual(get1(store, address(store, 2)), Found(b'', token(b'')))

@case('core')
def put_get_roundtrip(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`put-get-roundtrip`: values of length 0, 1, 255, a megabyte, every byte value, and bytes that are not valid text come back identical."""
    store = make().open()
    fixed = store.parameters.value_length
    if fixed is None:
        values = [b'', b'\x00', bytes(range(255)), bytes(1 << 20), bytes(range(256)), b'\xff\xfe\xc3\x28']
    else:
        values = [(bytes(range(256)) * (fixed // 256 + 1))[shift:shift + fixed] for shift in (0, 7, 128)] + [b'\xff\xfe\xc3\x28' * (fixed // 4) + b'\xc3' * (fixed % 4)]
    values = [each for each in values if limit_ok(store, len(each))]
    for i, data in enumerate(values):
        put(t, store, address(store, 10 + i), data)
    t.assertEqual(store.get([address(store, 10 + i) for i in range(len(values))]), [Found(data, token(data)) for data in values])

@case('core')
def put_replaces(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`put-replaces`: a second write replaces the first, and the token changes with the value."""
    store = make().open()
    at = address(store, 3)
    first, second = (value(store, 1), value(store, 2))
    put(t, store, at, first)
    put(t, store, at, second)
    found = get1(store, at)
    t.assertEqual(found, Found(second, token(second)))
    t.assertNotEqual(found.token, token(first))

@case('core')
def token_is_value_hash(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`token-is-value-hash`: equal bytes under two addresses have equal tokens, one changed byte changes it, and the token equals the SHA-256 of the bytes."""
    store = make().open()
    data = value(store, 5)
    changed = bytes([data[0] ^ 1]) + data[1:]
    for i, each in ((1, data), (2, data), (3, changed)):
        put(t, store, address(store, i), each)
    one, two, three = store.get([address(store, 1), address(store, 2), address(store, 3)])
    t.assertEqual(one.token, two.token)
    t.assertNotEqual(one.token, three.token)
    t.assertEqual(one.token, hashlib.sha256(data).digest())

@case('core', comparing)
def expect_holds_pass_and_conflict(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`expect-holds-pass-and-conflict`: an expectation on a current token commits; on a stale token it conflicts, names that expectation, and leaves every address as it was."""
    store = make().open()
    at, other = (address(store, 1), address(store, 2))
    put(t, store, at, value(store, 1))
    put(t, store, other, value(store, 9))
    stale = get1(store, at).token
    t.assertEqual(store.batch([(at, stale)], [(at, value(store, 2))]), Committed())
    before = snapshot(store, [at, other])
    t.assertEqual(store.batch([(at, stale)], [(at, value(store, 3))]), Conflict(0))
    t.assertEqual(snapshot(store, [at, other]), before)

@case('core', lambda store: comparing(store) and sparse(store))
def expect_absent_pass_and_conflict(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`expect-absent-pass-and-conflict`: an absent expectation commits for a never-written address and conflicts for a written one."""
    store = make().open()
    at = address(store, 4)
    t.assertEqual(store.batch([(at, ABSENT)], [(at, value(store, 1))]), Committed())
    t.assertEqual(store.batch([(at, ABSENT)], [(at, value(store, 2))]), Conflict(0))
    t.assertEqual(get1(store, at), Found(value(store, 1), token(value(store, 1))))

@case('core', atomic)
def batch_all_or_nothing(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`batch-all-or-nothing`: of three writes with the last expectation failing, or the second malformed (an address written twice), none is applied."""
    store = make().open()
    a, b, c = (address(store, i) for i in (1, 2, 3))
    for at in (a, b, c):
        put(t, store, at, value(store, 0))
    before = snapshot(store, [a, b, c])
    writes = [(a, value(store, 1)), (b, value(store, 2)), (c, value(store, 3))]
    if comparing(store):
        current = get1(store, a).token
        t.assertEqual(store.batch([(a, current), (b, current), (c, token(b'stale'))], writes), Conflict(2))
        t.assertEqual(snapshot(store, [a, b, c]), before)
    t.assertIsInstance(store.batch([], [writes[0], (a, value(store, 4)), writes[2]]), Refused)
    t.assertEqual(snapshot(store, [a, b, c]), before)

@case('core')
def batch_malformed_refused(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`batch-malformed-refused`: an empty batch, an address written twice, two expectations on one address, an address the instantiation does not take, a value of another size than the fixed one, and a batch over a declared limit are each refused with nothing applied."""
    store = make().open()
    p, limits = (store.parameters, store.limits)
    a, b = (address(store, 1), address(store, 2))
    put(t, store, a, value(store, 0))
    before = snapshot(store, [a, b])
    malformed: list[tuple[list, list]] = [([], []), ([], [(a, value(store, 1)), (a, value(store, 2))])]
    if comparing(store):
        malformed.append(([(a, ABSENT), (a, token(b'x'))], [(a, value(store, 1))]))
    if p.address_length:
        malformed.append(([], [(a + b'\x00', value(store, 1))]))
    if p.dense:
        malformed.append(([], [(p.capacity.to_bytes(p.address_length, 'big'), value(store, 1))]))
    if p.value_length is not None:
        malformed.append(([], [(a, bytes(other_size(store)))]))
    for expect, write in malformed:
        answer = store.batch(expect, write)
        t.assertIsInstance(answer, Refused, (expect, write))
        t.assertEqual(snapshot(store, [a, b]), before)
    if limits.bytes_per_value is not None and p.value_length is None:
        t.assertEqual(store.batch([], [(b, bytes(limits.bytes_per_value + 1))]), Refused(Refusal.TOO_LARGE))
        t.assertEqual(snapshot(store, [a, b]), before)

@case('core', lambda store: any((each is not None for each in (store.limits.writes_per_batch, store.limits.bytes_per_batch, store.limits.bytes_per_value))))
def batch_at_the_limits(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`batch-at-the-limits`: a batch at each limit the adapter declares, in writes, in bytes and in the size of one value, is committed, and a batch one over each is refused as TooLarge."""
    store = make().open()
    limits, fixed = (store.limits, store.parameters.value_length)
    small = value(store, 1, 1)
    if limits.writes_per_batch is not None and (atomic(store) or limits.writes_per_batch == 1):
        n = limits.writes_per_batch
        if limits.bytes_per_batch is None or (n + 1) * len(small) <= limits.bytes_per_batch:
            t.assertEqual(store.batch([], [(address(store, i), small) for i in range(n)]), Committed())
            t.assertEqual(store.batch([], [(address(store, i), small) for i in range(n + 1)]), Refused(Refusal.TOO_LARGE))
    if fixed is None and limits.bytes_per_value is not None:
        most = limits.bytes_per_value
        t.assertEqual(store.batch([], [(address(store, 1), bytes(most))]), Committed() if limits.bytes_per_batch is None or most <= limits.bytes_per_batch else Refused(Refusal.TOO_LARGE))
        t.assertEqual(store.batch([], [(address(store, 1), bytes(most + 1))]), Refused(Refusal.TOO_LARGE))
    if fixed is None and limits.bytes_per_batch is not None and atomic(store):
        total, per = (limits.bytes_per_batch, limits.bytes_per_value or limits.bytes_per_batch)
        sizes = [per] * (total // per) + ([total % per] if total % per else [])
        if limits.writes_per_batch is None or len(sizes) < limits.writes_per_batch:
            t.assertEqual(store.batch([], [(address(store, 100 + i), bytes(size)) for i, size in enumerate(sizes)]), Committed())
            t.assertEqual(store.batch([], [(address(store, 100 + i), bytes(size)) for i, size in enumerate(sizes)] + [(address(store, 99), b'\x00')]), Refused(Refusal.TOO_LARGE))

@case('core', lambda store: comparing(store) and atomic(store))
def batch_answer_order(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`batch-answer-order`: a batch that is malformed and also holds a stale expectation is Refused, one with two failing expectations names the first in the order given, and one with two expectations on an address is Refused. (Unavailable before Conflict, for an address the adapter does not hold, is the `fallback` group's `held-only-updates`.)"""
    store = make().open()
    a, b = (address(store, 1), address(store, 2))
    put(t, store, a, value(store, 1))
    put(t, store, b, value(store, 1))
    stale = token(b'stale')
    t.assertIsInstance(store.batch([(a, stale)], [(b, value(store, 2)), (b, value(store, 3))]), Refused)
    t.assertEqual(store.batch([(b, stale), (a, stale)], [(a, value(store, 2))]), Conflict(0))
    t.assertIsInstance(store.batch([(a, stale), (a, get1(store, a).token)], [(a, value(store, 2))]), Refused)

@case('core', lambda store: not atomic(store))
def not_atomic_refused(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`not-atomic-refused`: an adapter declaring `atomic_batch` false refuses a two-address batch and a one-address batch with an expectation on a second address, and commits a one-address write with an expectation on it."""
    store = make().open()
    a, b = (address(store, 1), address(store, 2))
    t.assertEqual(store.batch([], [(a, value(store, 1)), (b, value(store, 1))]), Refused(Refusal.NOT_ATOMIC))
    if comparing(store):
        put(t, store, b, value(store, 1))
        t.assertEqual(store.batch([(b, get1(store, b).token)], [(a, value(store, 2))]), Refused(Refusal.NOT_ATOMIC))
        put(t, store, a, value(store, 1))
        t.assertEqual(store.batch([(a, get1(store, a).token)], [(a, value(store, 3))]), Committed())

@case('core', atomic)
def batch_visible_whole(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`batch-visible-whole`: while one thread commits batches that write two addresses together, another reading them in one `get` call, and in one `list` call for a sparse store, never finds them inconsistent, over 10,000 rounds."""
    adapter = make()
    writer, reader = (adapter.open(), adapter.open())
    rounds, faults = (10000, [])
    pairs = [(address(writer, 2 * i), address(writer, 2 * i + 1)) for i in range(64)]

    def write() -> None:
        for n in range(rounds):
            a, b = pairs[n % len(pairs)]
            data = value(writer, n)
            if writer.batch([], [(a, data), (b, data)]) != Committed():
                faults.append(('batch', n))
    thread = threading.Thread(target=write)
    thread.start()
    while thread.is_alive():
        a, b = random.choice(pairs)
        one, two = reader.get([a, b])
        if one != two:
            faults.append(('get', one, two))
        if sparse(reader):
            held = set(reader.list())
            if any(((x in held) != (y in held) for x, y in pairs)):
                faults.append(('list',))
    thread.join()
    t.assertEqual(faults, [])

@case('core', comparing)
def concurrent_writers_no_lost_update(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`concurrent-writers-no-lost-update`: N writers each add one to a counter by reading it and writing with an expectation on the token, retrying on conflict, and the final value is N."""
    adapter = make()
    counter, writers = (address(adapter.open(), 7), 8)
    size = adapter.open().parameters.value_length or 8

    def encode(n: int) -> bytes:
        return n.to_bytes(size, 'big')
    put(t, adapter.open(), counter, encode(0))

    def add_one() -> None:
        store = adapter.open()
        while True:
            found = get1(store, counter)
            if store.batch([(counter, found.token)], [(counter, encode(int.from_bytes(found.value, 'big') + 1))]) == Committed():
                return
    threads = [threading.Thread(target=add_one) for _ in range(writers)]
    for each in threads:
        each.start()
    for each in threads:
        each.join()
    t.assertEqual(int.from_bytes(get1(adapter.open(), counter).value, 'big'), writers)

@case('core')
def list_order_and_range(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`list-order-and-range`: addresses come back in byte order, the range is half open, `after` excludes its address, and paging ascending and descending with `after` set to the last address returned visits every address once and never repeats a page."""
    store = make().open()
    if sparse(store):
        held = [address(store, i) for i in (5, 1, 9, 3, 7, 2, 8)]
        if not store.parameters.address_length:
            held += [b'k', b'k\x00', b'\x00', b'\xff\xff\xff\xff\xff\xff']
        write_in_batches(t, store, [(at, value(store, 1)) for at in held])
    else:
        held = list(store.list())
    expected = sorted(held)
    t.assertEqual(list(store.list()), expected)
    low, high = (expected[1], expected[4])
    t.assertEqual(list(store.list(from_=low, to=high)), expected[1:4])
    t.assertEqual(list(store.list(from_=low, to=high, after=expected[1])), expected[2:4])
    t.assertEqual(list(store.list(descending=True)), expected[::-1])
    for descending in (False, True):
        seen, after = ([], None)
        while True:
            page = list(store.list(after=after, limit=2, descending=descending))
            seen += page
            if len(page) < 2:
                break
            after = page[-1]
        t.assertEqual(seen, expected[::-1] if descending else expected)

@case('core')
def many_nodes(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`many-nodes`: 10,000 addresses are written in batches and read back by `get` and `list`, equal to what was written."""
    store = make().open()
    writes = [(address(store, i), value(store, i)) for i in range(10000)]
    write_in_batches(t, store, writes)
    t.assertEqual(store.get([at for at, _ in writes]), [Found(data, token(data)) for _, data in writes])
    listed = set(store.list())
    t.assertTrue({at for at, _ in writes} <= listed)
    if sparse(store):
        t.assertEqual(listed, {at for at, _ in writes})

@case('core')
def derived_structures_droppable(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`derived-structures-droppable`: dropping every derived structure through the seam and repeating a sequence of `list` and `get` calls changes no answer."""
    store = make().open()
    write_in_batches(t, store, [(address(store, i), value(store, i)) for i in range(50)])

    def answers() -> list:
        return [store.list(), store.list(limit=3, descending=True), store.list(from_=address(store, 10), to=address(store, 20)), store.get([address(store, i) for i in range(0, 60, 7)])]
    before = answers()
    t.assertIsInstance(store, Seam)
    store.drop_derived_structures()
    t.assertEqual(answers(), before)

@case('core')
def many_keys_one_pass(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`many-keys-one-pass`: a `get` of 1,000 addresses starts the same number of processes and opens the same number of files as a `get` of one."""
    store = make().open()
    write_in_batches(t, store, [(address(store, i), value(store, i)) for i in range(1000)])
    start = store.stats()
    store.get([address(store, 0)])
    one = store.stats()
    store.get([address(store, i) for i in range(1000)])
    many = store.stats()
    t.assertEqual((many.processes_started - one.processes_started, many.files_opened - one.files_opened), (one.processes_started - start.processes_started, one.files_opened - start.files_opened))

@case('core')
def read_inputs_refused(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`read-inputs-refused`: a `get` of an address the instantiation does not take, and a `list` with a `limit` of zero or a `from` after a `to`, are Refused and answer nothing."""
    store = make().open()
    p = store.parameters
    t.assertIsInstance(store.list(limit=0), Refused)
    t.assertIsInstance(store.list(from_=address(store, 2), to=address(store, 1)), Refused)
    if p.address_length:
        t.assertIsInstance(store.get([address(store, 1), b'\x00' * (p.address_length + 1)]), Refused)
    if p.dense:
        t.assertIsInstance(store.get([p.capacity.to_bytes(p.address_length, 'big')]), Refused)

@case('core')
def state_changes_on_commit_only(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`state-changes-on-commit-only`: `state()` is unchanged by reads and by a batch that is Refused or in Conflict, and changes when a batch commits."""
    store = make().open()
    at = address(store, 1)
    put(t, store, at, value(store, 1))
    first = store.state()
    store.get([at])
    store.list()
    t.assertIsInstance(store.batch([], []), Refused)
    if comparing(store):
        t.assertEqual(store.batch([(at, token(b'stale'))], [(at, value(store, 2))]), Conflict(0))
    t.assertEqual(store.state(), first)
    put(t, store, at, value(store, 2))
    t.assertNotEqual(store.state(), first)

@case('core')
def changes_since_lists_written_addresses(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`changes-since-lists-written-addresses`: `changes(since)` answers the addresses written by the batches committed after `since`, ascending and each once; from the current state it answers none; a state the store never answered is Refused."""
    store = make().open()
    put(t, store, address(store, 9), value(store, 1))
    since = store.state()
    written = [address(store, i) for i in (5, 3, 5, 8)]
    for i, at in enumerate(written):
        put(t, store, at, value(store, 10 + i))
    t.assertEqual(store.changes(since), tuple(sorted(set(written))))
    t.assertEqual(store.changes(store.state()), ())
    t.assertIsInstance(store.changes(b'\xff' * 3 + b'never'), Refused)

@case('dense', lambda store: store.parameters.dense)
def dense_has_no_absent(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`dense-has-no-absent`: every address of a dense store's capacity reads Found, never Absent, an unwritten one with the unwritten value, and `list` with no bounds answers the whole capacity range."""
    store = make().open()
    p = store.parameters
    put(t, store, address(store, 3), value(store, 3))
    every = [i.to_bytes(p.address_length, 'big') for i in range(p.capacity)]
    answers = store.get(every)
    t.assertFalse(any((isinstance(each, Absent) for each in answers)))
    t.assertEqual(answers[0], Found(p.unwritten(), token(p.unwritten())))
    t.assertEqual(list(store.list()), every)

@case('fixed-length', lambda store: store.parameters.value_length is not None)
def fixed_length_refuses_other_size(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`fixed-length-refuses-other-size`: a write of a value whose length is not the fixed length is Refused and nothing is applied."""
    store = make().open()
    at = address(store, 1)
    before = store.get([at])
    for size in (store.parameters.value_length - 1, store.parameters.value_length + 1):
        if size >= 0:
            t.assertEqual(store.batch([], [(at, bytes(size))]), Refused(Refusal.MALFORMED))
    t.assertEqual(store.get([at]), before)

@case('no-compare', lambda store: not comparing(store))
def no_compare_refuses_expectation(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`no-compare-refuses-expectation`: a store that cannot compare and write one address refuses a batch with any expectation, a token or `absent`, as NotAtomic, and commits the same write without one."""
    store = make().open()
    at = address(store, 1)
    put(t, store, at, value(store, 1))
    before = store.get([at])
    for expectation in (get1(store, at).token, ABSENT):
        t.assertEqual(store.batch([(at, expectation)], [(at, value(store, 2))]), Refused(Refusal.NOT_ATOMIC))
    t.assertEqual(store.get([at]), before)
    put(t, store, at, value(store, 2))

def child(adapter: Adapter, action: str, *arguments: str) -> subprocess.Popen:
    """Run an action on the same adapter in a child process; its answers come on its standard output, one per line."""
    module, function, keywords = adapter.opener()
    return subprocess.Popen([sys.executable, str(Path(__file__)), 'child', module, function, json.dumps(keywords), action, *arguments], stdout=subprocess.PIPE, text=True)

def child_batch(adapter: Adapter, expect: list, write: list) -> subprocess.Popen:
    encode = lambda expectation: None if isinstance(expectation, Absent) else expectation.hex()
    return child(adapter, 'batch', json.dumps([[at.hex(), encode(e)] for at, e in expect]), json.dumps([[at.hex(), data.hex()] for at, data in write]))

@case('durable', lambda store: Capability.DURABLE in store.capabilities)
def reopen_sees_committed(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`reopen-sees-committed`: after the store is closed and opened again by a new process, everything committed is there, with the same tokens."""
    adapter = make()
    store = adapter.open()
    written = [(address(store, i), value(store, i)) for i in (1, 2)]
    write_in_batches(t, store, written)
    del store
    process = child(adapter, 'get', json.dumps([at.hex() for at, _ in written]))
    t.assertEqual(process.communicate(timeout=120)[0].split(), [token(data).hex() for _, data in written])

@case('durable', lambda store: Capability.DURABLE in store.capabilities and atomic(store))
def kill_during_batch_is_atomic(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`kill-during-batch-is-atomic`: a child process commits batches each writing a pair of addresses, reports each commit on a pipe, and is killed at random moments, 200 times; on reopening, every batch the child reported is present, and every other batch is present whole or absent whole."""
    adapter = make()
    chance = random.Random(20261026)
    for round_ in range(200):
        start = round_ * 100000
        process = child(adapter, 'pairs', str(start))
        reported: list[int] = []
        wanted = chance.randrange(0, 30)
        while len(reported) < wanted:
            line = process.stdout.readline()
            if not line:
                break
            reported.append(int(line))
        process.kill()
        process.wait()
        store = adapter.open()
        last = max(reported, default=start - 1) + 2
        for n in range(start, last + 1):
            one, two = store.get([address(store, 2 * n), address(store, 2 * n + 1)])
            if n in reported:
                t.assertEqual((one, two), (Found(value(store, n), token(value(store, n))),) * 2)
            else:
                t.assertEqual(one, two)

@case('durable', lambda store: Capability.DURABLE in store.capabilities)
def killed_writer_leaves_no_lock(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`killed-writer-leaves-no-lock`: after a writer is killed while committing, a new process commits without waiting for the dead one."""
    adapter = make()
    process = child(adapter, 'pairs', '0')
    process.stdout.readline()
    process.kill()
    process.wait()
    store = adapter.open()
    started = time.monotonic()
    follower = child_batch(adapter, [], [(address(store, 1), value(store, 1))])
    t.assertEqual(follower.communicate(timeout=60)[0].split(), ['Committed'])
    t.assertLess(time.monotonic() - started, 30)

@case('durable', lambda store: Capability.DURABLE in store.capabilities and comparing(store))
def paused_live_writer_is_not_overtaken(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`paused-live-writer-is-not-overtaken`: two writers hold the same expectation on one address and the first is paused at the commit point for 60 seconds; the second waits or conflicts, and exactly one commits."""
    adapter = make()
    first, second = (adapter.open(), adapter.open())
    at = address(first, 1)
    put(t, first, at, value(first, 0))
    current = get1(first, at).token
    release = threading.Event()
    first.at_commit_point(lambda: release.wait(60))
    answers: dict[str, Any] = {}
    one = threading.Thread(target=lambda: answers.__setitem__('first', first.batch([(at, current)], [(at, value(first, 1))])))
    one.start()
    time.sleep(1)
    two = threading.Thread(target=lambda: answers.__setitem__('second', second.batch([(at, current)], [(at, value(second, 2))])))
    two.start()
    two.join(59)
    release.set()
    one.join()
    two.join()
    t.assertEqual(sorted((type(each).__name__ for each in answers.values())), ['Committed', 'Conflict'])

@case('durable', lambda store: Capability.DURABLE in store.capabilities)
def unknown_fate_settles_first(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`unknown-fate-settles-first`: a batch made to fail at the commit point is answered Unavailable with the reason Failed, and when the pause ends the batch is not applied."""
    adapter = make()
    store = adapter.open()
    at = address(store, 1)
    before = store.get([at])

    def fail() -> None:
        time.sleep(1)
        raise RuntimeError('made to fail at the commit point')
    store.at_commit_point(fail)
    t.assertEqual(store.batch([], [(at, value(store, 1))]), Unavailable(Unavailability.FAILED))
    store.at_commit_point(None)
    t.assertEqual(adapter.open().get([at]), before)

@case('shared', lambda store: Capability.SHARED_BETWEEN_PROCESSES in store.capabilities and comparing(store))
def two_processes_lose_cleanly(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`two-processes-lose-cleanly`: two processes write the same address with the same expectation; one commits, the other conflicts, and the store is readable."""
    adapter = make()
    store = adapter.open()
    at = address(store, 1)
    put(t, store, at, value(store, 0))
    current = get1(store, at).token
    processes = [child_batch(adapter, [(at, current)], [(at, value(store, n))]) for n in (1, 2)]
    answers = sorted((process.communicate(timeout=120)[0].strip() for process in processes))
    t.assertEqual(answers, ['Committed', 'Conflict'])
    t.assertIsInstance(get1(adapter.open(), at), Found)

@case('shared', lambda store: Capability.SHARED_BETWEEN_PROCESSES in store.capabilities)
def one_process_sees_the_others_commit(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`one-process-sees-the-others-commit`: a call of `get` and `list` that begins after another process's batch returned sees it, whatever derived structure the first process held before."""
    adapter = make()
    store = adapter.open()
    at = address(store, 5)
    store.get([at])
    store.list()
    process = child_batch(adapter, [], [(at, value(store, 5))])
    t.assertEqual(process.communicate(timeout=120)[0].split(), ['Committed'])
    t.assertEqual(get1(store, at), Found(value(store, 5), token(value(store, 5))))
    t.assertIn(at, store.list())

@case('shared', lambda store: Capability.SHARED_BETWEEN_PROCESSES in store.capabilities)
def changes_sees_other_process(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`changes-sees-other-process`: after another process commits a batch, `state()` differs from the state before it and `changes` from that state answers the addresses it wrote."""
    adapter = make()
    store = adapter.open()
    since = store.state()
    written = [address(store, 3), address(store, 4)]
    process = child_batch(adapter, [], [(at, value(store, 1)) for at in written])
    t.assertEqual(process.communicate(timeout=120)[0].split(), ['Committed'])
    t.assertNotEqual(store.state(), since)
    t.assertTrue(set(written) <= set(store.changes(since)))

@case('model')
def model_equivalence(t: unittest.TestCase, make: Callable[[], Adapter]) -> None:
    """`model-equivalence`: random sequences of `get`, `list` and `batch`, from a recorded seed, give the same answers on the adapter and on `volatile`, for at least 100,000 operations, the model built with the limits the adapter declares and the sequences kept within them; `changes` answers the same addresses."""
    store = make().open()
    model = Volatile(store.parameters, store.limits, atomic_batch=atomic(store))
    seed = 20261026
    chance = random.Random(seed)
    pool = [address(store, i) for i in range(200)]
    per = 1 if not atomic(store) else min(3, store.limits.writes_per_batch or 3)
    starts = (store.state(), model.state())
    for step in range(100000):
        kind = chance.random()
        if kind < 0.35:
            chosen = chance.sample(pool, chance.randint(1, 3))
            mine, theirs = (store.get(chosen), model.get(chosen))
        elif kind < 0.55:
            low, high = sorted(chance.sample(pool, 2))
            options = {'from_': low if chance.random() < 0.5 else None, 'to': high if chance.random() < 0.5 else None, 'after': chance.choice(pool) if chance.random() < 0.3 else None, 'limit': chance.randint(1, 10), 'descending': chance.random() < 0.5}
            mine, theirs = (store.list(**options), model.list(**options))
        else:
            targets = chance.sample(pool, chance.randint(1, per))
            write = [(at, value(store, chance.randrange(50), chance.randrange(0, 12))) for at in targets]
            write = [(at, data) for at, data in write if limit_ok(store, len(data))] or [(targets[0], value(store, 0, 1))]
            expect = []
            if comparing(store) and chance.random() < 0.5:
                at = write[0][0]
                current = model.get([at])[0]
                pick = chance.random()
                expect = [(at, current.token if isinstance(current, Found) and pick < 0.6 else ABSENT if pick < 0.8 else token(b'stale'))]
            mine, theirs = (store.batch(expect, write), model.batch(expect, write))
        if mine != theirs:
            t.fail(f'step {step} of seed {seed}: the adapter answered {mine!r} and the model {theirs!r}')
    t.assertEqual(store.changes(starts[0]), model.changes(starts[1]))

def _run_child(module: str, function: str, keywords: str, action: str, *arguments: str) -> None:
    store = getattr(import_module(module), function)(**json.loads(keywords)).open()
    if action == 'batch':
        expect = [(bytes.fromhex(at), ABSENT if e is None else bytes.fromhex(e)) for at, e in json.loads(arguments[0])]
        write = [(bytes.fromhex(at), bytes.fromhex(data)) for at, data in json.loads(arguments[1])]
        print(type(store.batch(expect, write)).__name__, flush=True)
    elif action == 'get':
        for answer in store.get([bytes.fromhex(at) for at in json.loads(arguments[0])]):
            print(answer.token.hex() if isinstance(answer, Found) else type(answer).__name__, flush=True)
    elif action == 'pairs':
        n = int(arguments[0])
        while True:
            data = value(store, n)
            if store.batch([], [(address(store, 2 * n), data), (address(store, 2 * n + 1), data)]) == Committed():
                print(n, flush=True)
            n += 1
if __name__ == '__main__' and len(sys.argv) > 1 and (sys.argv[1] == 'child'):
    _run_child(*sys.argv[2:])
