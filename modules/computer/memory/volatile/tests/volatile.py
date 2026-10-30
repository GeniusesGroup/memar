#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
TIER = 'unit'
BUDGET_SECONDS = 120
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

class BuildRefusesWhatTheAddressesCannotCount(unittest.TestCase):

    def test_a_dense_capacity_above_the_address_space_is_the_malformed_refusal(self) -> None:
        errors = import_module('modules.computer.memory.store.errors.errors')
        built, refusal = Volatile.build(Parameters(address_length=1, dense=True, capacity=257), Limits(), True)
        self.assertIsNone(built)
        self.assertIs(refusal, errors.Refusal.MALFORMED)

    def test_a_dense_store_without_a_fixed_address_length_is_the_malformed_refusal(self) -> None:
        errors = import_module('modules.computer.memory.store.errors.errors')
        built, refusal = Volatile.build(Parameters(dense=True, capacity=4), Limits(), True)
        self.assertIsNone(built)
        self.assertIs(refusal, errors.Refusal.MALFORMED)

    def test_a_capacity_the_addresses_can_count_builds(self) -> None:
        built, refusal = Volatile.build(Parameters(address_length=1, dense=True, capacity=256, value_length=1), Limits(), True)
        self.assertIsNone(refusal)
        self.assertIsInstance(built, Volatile)

    def test_the_constructor_raises_the_refusal_and_not_a_value_error(self) -> None:
        errors = import_module('modules.computer.memory.store.errors.errors')
        with self.assertRaises(errors.Raised) as caught:
            Volatile(Parameters(address_length=1, dense=True, capacity=257))
        self.assertIs(caught.exception.reason, errors.Refusal.MALFORMED)
        self.assertNotIsInstance(caught.exception, ValueError)
if __name__ == '__main__':
    unittest.main()
