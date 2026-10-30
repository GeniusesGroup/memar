#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
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
Cost = _m_conformance.Cost
Found = _m_store.Found
Lockable = _m_lockable.Lockable
address = _m_conformance.address
token = _m_store.token
value = _m_conformance.value

def declares(store: Any) -> bool:
    return Capability.LOCKABLE in store.capabilities

def lock_excludes_second_holder(t: unittest.TestCase, make: Callable[[], Any]) -> None:
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
    store = make().open()
    t.assertEqual(isinstance(store, Lockable), declares(store))
WAITS = Cost(waits_on_clock=True)
CASES = [Case('lockable', declares, lock_excludes_second_holder, budget=60, cost=WAITS), Case('lockable', declares, lock_lapses_with_lease, budget=60, cost=WAITS), Case('lockable', lambda store: True, lock_refused_when_not_lockable)]
