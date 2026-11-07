#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import hashlib
import os
import subprocess
import time
import unittest
from importlib import import_module
from pathlib import Path
from typing import Any, Callable, Sequence
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
ABSENT = _m_store.ABSENT
Capability = _m_store.Capability
Case = _m_conformance.Case
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Unavailability = _m_store.Unavailability
Unavailable = _m_store.Unavailable
address = _m_conformance.address
put = _m_conformance.put
token = _m_store.token
value = _m_conformance.value
PUBLISHED_WITHIN = 60.0

class Scripted:

    def __init__(self, values: dict[bytes, bytes] | None=None, reachable: bool=True) -> None:
        self.values = dict(values or {})
        self.reachable = reachable

    def get(self, addresses: Sequence[bytes]) -> list[Any]:
        if not self.reachable:
            return [Unavailable(Unavailability.UNREACHABLE) for _ in addresses]
        return [Found(self.values[at], token(self.values[at])) if at in self.values else ABSENT for at in addresses]

    def list(self, from_: bytes, to: bytes | None) -> Any:
        if not self.reachable:
            return Unavailable(Unavailability.UNREACHABLE)
        return tuple(sorted((at for at in self.values if from_ <= at and (to is None or at < to))))

def falls_back(store: Any) -> bool:
    return Capability.FALLBACK in store.capabilities

def held_from(store: Any) -> tuple[tuple[bytes, None], ...]:
    return ((address(store, 1000), None),)

def unavailable_is_not_absent(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    probe = adapter.open()
    adapter.fall_back(Scripted(reachable=False), held_from(probe))
    store = adapter.open()
    t.assertEqual(store.get([address(store, 1), address(store, 1001)]), [Unavailable(Unavailability.UNREACHABLE), ABSENT])

def list_unavailable_is_not_short(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    probe = adapter.open()
    adapter.fall_back(Scripted(reachable=False), held_from(probe))
    store = adapter.open()
    written = [address(store, i) for i in (1001, 1003, 1002)]
    t.assertEqual(store.batch([], [(at, value(store, 1)) for at in written]), Committed())
    t.assertEqual(store.list(), Unavailable(Unavailability.UNREACHABLE))
    t.assertEqual(store.list(from_=address(store, 2), to=address(store, 1002)), Unavailable(Unavailability.UNREACHABLE))
    t.assertEqual(store.list(from_=address(store, 1000)), tuple(sorted(written)))

def held_only_updates(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    probe = adapter.open()
    fallback = Scripted(reachable=False)
    adapter.fall_back(fallback, held_from(probe))
    store = adapter.open()
    outside, inside = (address(store, 1), address(store, 1001))
    t.assertEqual(store.batch([], [(outside, value(store, 1))]), Unavailable(Unavailability.NOT_HELD))
    t.assertEqual(store.batch([(outside, token(value(store, 1)))], [(inside, value(store, 1))]), Unavailable(Unavailability.NOT_HELD))
    t.assertEqual(store.batch([(outside, token(b'stale')), (inside, token(b'stale'))], [(inside, value(store, 1))]), Unavailable(Unavailability.NOT_HELD))
    t.assertEqual(store.batch([(outside, ABSENT)], [(inside, value(store, 1))]), Unavailable(Unavailability.UNREACHABLE))
    t.assertEqual(store.get([inside]), [ABSENT])
    t.assertEqual(store.batch([(inside, ABSENT)], [(inside, value(store, 2))]), Committed())
    fallback.reachable = True
    t.assertEqual(store.batch([(outside, ABSENT)], [(inside, value(store, 3))]), Committed())
    fallback.values[outside] = value(store, 9)
    t.assertEqual(store.batch([(outside, ABSENT)], [(inside, value(store, 4))]), Conflict(0))
    t.assertEqual(store.get([inside]), [Found(value(store, 3), token(value(store, 3)))])

def fallback_not_found(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    probe = adapter.open()
    adapter.fall_back(None, held_from(probe))
    store = adapter.open()
    t.assertEqual(store.get([address(store, 1)]), [ABSENT])
    t.assertEqual(store.list(to=address(store, 1000)), ())

def fallback_found(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    probe = adapter.open()
    at = address(probe, 1)
    fallback = Scripted({at: value(probe, 1)})
    adapter.fall_back(fallback, held_from(probe))
    store = adapter.open()
    since = store.state()
    t.assertEqual(store.get([at]), [Found(value(store, 1), token(value(store, 1)))])
    t.assertEqual(store.list(to=address(store, 1000)), (at,))
    fallback.values[at] = value(store, 2)
    t.assertEqual(store.get([at]), [Found(value(store, 2), token(value(store, 2)))])
    t.assertEqual((store.state(), store.changes(since), store.list(from_=address(store, 1000))), (since, (), ()))

def _working_tree_view(tree: Path) -> tuple:
    files = []
    for folder, folders, names in os.walk(tree):
        folders[:] = [each for each in folders if each != '.git']
        for name in names:
            path = Path(folder) / name
            files.append((path.relative_to(tree).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest()))
    status = subprocess.run(['git', '-C', str(tree), 'status', '--porcelain=v1', '--ignored', '-z'], capture_output=True).stdout
    index = subprocess.run(['git', '-C', str(tree), 'ls-files', '-s', '-z'], capture_output=True).stdout
    return (sorted(files), status, index)

def working_tree_unchanged(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    tree = adapter.working_tree()
    t.assertIsNotNone(tree, 'an adapter declaring the capability names the working tree it leaves untouched')
    before = _working_tree_view(tree)
    store = adapter.open()
    since = store.state()
    _m_conformance.write_in_batches(t, store, [(address(store, i), value(store, i)) for i in range(40)])
    store.get([address(store, i) for i in range(0, 50, 3)])
    store.list(from_=address(store, 5), limit=4, descending=True)
    store.changes(since)
    store.drop_derived_structures()
    store.list()
    process = _m_conformance.child_batch(adapter, [], [(address(store, 99), value(store, 99))])
    t.assertEqual(process.communicate(timeout=120)[0].split(), ['Committed'])
    t.assertEqual(_working_tree_view(tree), before)

def replicated(store: Any) -> bool:
    return Capability.REPLICATED in store.capabilities

def _settles(store: Any, adapter: Any, within: float=PUBLISHED_WITHIN) -> bool:
    ends = time.monotonic() + within
    while time.monotonic() < ends:
        if adapter.shared_state() == store.state() and store.lag().batches == 0:
            return True
        time.sleep(0.2)
    return False

def committed_batch_reaches_shared_store(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    store = adapter.open()
    put(t, store, address(store, 1), value(store, 1))
    t.assertTrue(_settles(store, adapter), store.lag())
    put(t, store, address(store, 2), value(store, 2))
    t.assertTrue(_settles(store, adapter), store.lag())

def unreachable_shared_store_keeps_the_batch_and_retries(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    store = adapter.open()
    adapter.shared_reachable(False)
    started = time.monotonic()
    put(t, store, address(store, 1), value(store, 1))
    t.assertLess(time.monotonic() - started, 10)
    time.sleep(1)
    lag = store.lag()
    t.assertEqual(lag.batches, 1)
    t.assertIsNone(adapter.shared_state())
    adapter.shared_reachable(True)
    t.assertTrue(_settles(store, adapter), store.lag())

def lag_survives_a_restart(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    store = adapter.open()
    adapter.shared_reachable(False)
    put(t, store, address(store, 1), value(store, 1))
    put(t, store, address(store, 2), value(store, 2))
    adapter.close()
    time.sleep(1.1)
    module, function, keywords = adapter.opener()
    again = getattr(import_module(module), function)(**keywords)
    try:
        again.shared_reachable(False)
        reopened = again.open()
        lag = reopened.lag()
        t.assertEqual(lag.batches, 2)
        t.assertGreaterEqual(lag.oldest_age, 1.0)
        again.shared_reachable(True)
        t.assertTrue(_settles(reopened, again), reopened.lag())
    finally:
        again.close()

def publish_refused_as_not_fast_forward_is_reported(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    adapter = make()
    other = adapter.sibling()
    try:
        theirs = other.open()
        put(t, theirs, address(theirs, 1), value(theirs, 1))
        t.assertTrue(_settles(theirs, other), theirs.lag())
        store = adapter.open()
        put(t, store, address(store, 2), value(store, 2))
        ends = time.monotonic() + PUBLISHED_WITHIN
        while time.monotonic() < ends and (not store.lag().refused):
            time.sleep(0.2)
        lag = store.lag()
        t.assertTrue(lag.refused, lag)
        t.assertEqual(lag.batches, 1)
        t.assertEqual(adapter.shared_state(), theirs.state())
    finally:
        other.close()
CASES = [Case('fallback', falls_back, check) for check in (unavailable_is_not_absent, list_unavailable_is_not_short, held_only_updates, fallback_not_found, fallback_found)]
CASES.append(Case('working-tree', lambda store: Capability.LEAVES_WORKING_TREE_UNTOUCHED in store.capabilities, working_tree_unchanged))
REPLICATED_CASES = [Case('replicated', replicated, check) for check in (committed_batch_reaches_shared_store, unreachable_shared_store_keeps_the_batch_and_retries, lag_survives_a_restart, publish_refused_as_not_fast_forward_is_reported)]
CASES += REPLICATED_CASES
