#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""The `lockable` group of the conformance suite: the cases a store declaring `lockable` is decided by.

Owed by this module, which declares the capability ([Memory Store → The cases this module owes](../../../../../modules/computer/memory/store/store.md#the-cases-this-module-owes)),
and run through the suite's runner: an adapter's tests pass `CASES` to `test_case`. The protocol is
`protocol/lockable.py`. No adapter declares `lockable` yet, so the two cases that need one are pending.
"""
from __future__ import annotations
import threading
import time
import unittest
from importlib import import_module
from typing import Any, Callable
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_lockable = import_module('modules-plugable.computer.memory.store.lockable.protocol.lockable')
Capability = _m_store.Capability
Case = _m_conformance.Case
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Lockable = _m_lockable.Lockable
address = _m_conformance.address
token = _m_store.token
value = _m_conformance.value

def declares(store: Any) -> bool:
    return Capability.LOCKABLE in store.capabilities

def lock_excludes_second_holder(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`lock-excludes-second-holder` (owed:memory.port.contract-suite): while one handle holds an address, a second handle's `lock` does not return; when the first unlocks with a value, the second's returns Found with that value."""
    adapter = make()
    first, second = (adapter.open(), adapter.open())
    at = address(first, 1)
    first.lock(at)
    answers: list[Any] = []
    waiter = threading.Thread(target=lambda: answers.append(second.lock(at)))
    waiter.start()
    waiter.join(min(5.0, first.lease / 2))
    t.assertEqual(answers, [])
    data = value(first, 1)
    t.assertEqual(first.unlock(at, data), Committed())
    waiter.join()
    t.assertEqual(answers, [Found(data, token(data))])
    t.assertEqual(second.unlock(at, None), Committed())

def lock_lapses_with_lease(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`lock-lapses-with-lease` (owed:memory.port.contract-suite): a lock its holder never unlocks lapses after the lease and not before: a second handle's `lock` returns no sooner, and the first holder's late `unlock` is a Conflict that writes nothing."""
    adapter = make()
    first, second = (adapter.open(), adapter.open())
    at = address(first, 1)
    first.lock(at)
    started = time.monotonic()
    before = second.get([at])
    second.lock(at)
    t.assertGreaterEqual(time.monotonic() - started, first.lease * 0.99)
    t.assertIsInstance(first.unlock(at, value(first, 2)), Conflict)
    t.assertEqual(second.get([at]), before)
    second.unlock(at, None)

def lock_refused_when_not_lockable(t: unittest.TestCase, make: Callable[[], Any]) -> None:
    """`lock-refused-when-not-lockable`: a store offers `lock` exactly when it declares `lockable`: one that does not declare it is no `Lockable` and has no `lock` to call, and one that declares it is one."""
    store = make().open()
    t.assertEqual(isinstance(store, Lockable), declares(store))
CASES = [Case('lockable', declares, lock_excludes_second_holder), Case('lockable', declares, lock_lapses_with_lease), Case('lockable', lambda store: True, lock_refused_when_not_lockable)]
