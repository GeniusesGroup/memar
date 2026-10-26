#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that `volatile`, the reference adapter of the store contract, keeps the contract.

    python modules/computer/memory/volatile/tests/volatile.py

The subject is `volatile.py`, named for the file that holds it per
[Test Naming](../../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that
owns it per [Test Placement](../../../../process/test/rules/test-placement/test-placement.md); its expectations are the
cases of [Memory Conformance](../../conformance/conformance.md), run through the suite's runner.

Nothing here reads or writes a file. `volatile` is run built four ways, so that every case that is not a capability's
applies to one of them:

  Sparse            any address and value length, compare-and-write, atomic, no limits.
  SparseLimited     8-byte addresses and the three limits declared.
  FixedCompare      16-byte addresses and 32-byte values, compare-and-write.
  Dense             a block: 2-byte positions, a capacity of 16,384, 16-byte values, no compare-and-write, not atomic.
  EveryCaseApplies  every case of the suite that no capability calls for applies to at least one of the four.
"""
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
Limits = _m_store.Limits
Parameters = _m_store.Parameters
Volatile = _m_volatile.Volatile
INSTANCES = {'Sparse': (Parameters(), Limits(), True), 'SparseLimited': (Parameters(address_length=8), Limits(writes_per_batch=50, bytes_per_batch=4096, bytes_per_value=1024), True), 'FixedCompare': (Parameters(address_length=16, value_length=32), Limits(), True), 'Dense': (Parameters(address_length=2, dense=True, capacity=16384, value_length=16, compare_and_write=False), Limits(), False)}
for _name, (_parameters, _limits, _atomic) in INSTANCES.items():
    globals()[_name] = type(_name, (_m_conformance.test_case(lambda p=_parameters, l=_limits, a=_atomic: Volatile(p, l, atomic_batch=a)),), {})

class EveryCaseApplies(unittest.TestCase):

    def test_every_case_no_capability_calls_for_runs_on_one_instance(self) -> None:
        capabilities = {'durable', 'shared'}
        wanted = {each.name for each in _m_conformance.CASES if each.group not in capabilities}
        ran = set().union(*(_m_conformance.applied(Volatile(p, l, atomic_batch=a)) for p, l, a in INSTANCES.values()))
        self.assertEqual(sorted(wanted - ran), [])
if __name__ == '__main__':
    unittest.main()
