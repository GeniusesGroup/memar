#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The `fallback`, `working-tree` and `replicated` groups of the conformance suite, owed by `git-store`.

[Memory Conformance](../../../../../modules/computer/memory/conformance/conformance.md) states the first two, restated
for addresses; the note of 2026-10-26 in task `20261023-T074642Z-5420` names the third; why they are coded here is
[git-store Handoff](git-store.handoff.md#decisions). An adapter's tests pass `CASES` to the suite's `test_case`. Each case
is one function whose docstring states it, and reaches the store through the seam below, which an adapter declaring the
group offers on the object `make()` returns:

  fall_back(fallback, held)   the handles opened after it ask FALLBACK, or the adapter's own when it is None, for
                              what lies outside HELD, a tuple of (from, to) ranges, `to` None for no end.
  working_tree()              the working tree of the project the store belongs to, or None.
  shared_reachable(flag)      whether the shared store can be reached from now on.
  shared_state()              the state of the class at the shared store, as `state()` answers it, or None.
  sibling()                   a new, empty adapter on another machine's store of the same class and shared store.
  close()                     ends what the adapter runs in this process: its git processes and its publishing.

A handle of a `replicated` store answers `lag()`, the batches ahead of the shared store, the age of the oldest and a
refusal.
"""
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
    """A fallback for the cases: it holds the values it is given, or cannot be reached."""

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
    """The held ranges of the cases: every address from the 1000th of the cases on."""
    return ((address(store, 1000), None),)

def unavailable_is_not_absent(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`unavailable-is-not-absent`: with the shared store unreachable, an address the adapter does not hold reads Unavailable and not Absent, and a held address never written reads Absent."""
    adapter = make()
    probe = adapter.open()
    adapter.fall_back(Scripted(reachable=False), held_from(probe))
    store = adapter.open()
    t.assertEqual(store.get([address(store, 1), address(store, 1001)]), [Unavailable(Unavailability.UNREACHABLE), ABSENT])

def list_unavailable_is_not_short(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`list-unavailable-is-not-short`: with the part of the addresses the adapter does not hold unreachable, a range that covers it answers Unavailable and one that does not answers completely."""
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
    """`held-only-updates`: outside the held ranges an expectation of a value and a write are Unavailable as NotHeld, an `absent` expectation is Unavailable as Unreachable until the shared store has answered, and a stale expectation is Unavailable and not Conflict; inside them a creation commits without asking."""
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
    """`fallback-not-found`: an address outside the held ranges that the shared store answers is not there reads Absent, through the adapter's own fallback, and a range outside them lists nothing."""
    adapter = make()
    probe = adapter.open()
    adapter.fall_back(None, held_from(probe))
    store = adapter.open()
    t.assertEqual(store.get([address(store, 1)]), [ABSENT])
    t.assertEqual(store.list(to=address(store, 1000)), ())

def fallback_found(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`fallback-found`: an address the shared store holds reads Found with its value as of the asking, a read after that value changed reads the new one, and what was read is not written into the adapter's store."""
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
    """What a person and git see of a working tree: each file outside `.git` with its bytes' hash, git's status with the ignored files, and its index."""
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
    """`working-tree-unchanged`: after a sequence of every operation, including a dropped derived structure and a second process's batch, a listing of the project's working tree, its tracked and ignored files and its index are as they were."""
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
    """Whether the shared store reaches the store's state, and the lag none, within WITHIN seconds."""
    ends = time.monotonic() + within
    while time.monotonic() < ends:
        if adapter.shared_state() == store.state() and store.lag().batches == 0:
            return True
        time.sleep(0.2)
    return False

def committed_batch_reaches_shared_store(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`committed-batch-reaches-shared-store`: a batch committed at the local compare-and-swap reaches the shared store soon after, by itself, and the lag returns to none."""
    adapter = make()
    store = adapter.open()
    put(t, store, address(store, 1), value(store, 1))
    t.assertTrue(_settles(store, adapter), store.lag())
    put(t, store, address(store, 2), value(store, 2))
    t.assertTrue(_settles(store, adapter), store.lag())

def unreachable_shared_store_keeps_the_batch_and_retries(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`unreachable-shared-store-keeps-the-batch-and-retries`: with the shared store unreachable a batch commits without waiting for it and the lag counts it; once the shared store is reachable again, the batch reaches it without another write."""
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
    """`lag-survives-a-restart`: batches committed while the shared store is unreachable are counted, with the age of the oldest, by a new adapter on the same store that holds nothing in memory from the first; it publishes them once the shared store is reachable."""
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
    """`publish-refused-as-not-fast-forward-is-reported`: when another machine has published a batch of the same class first, this store's batch commits locally, its push is refused as not a fast-forward, the refusal is reported in the lag, and the shared store keeps the other machine's batch."""
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
