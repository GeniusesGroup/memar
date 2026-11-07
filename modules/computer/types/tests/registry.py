#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 30
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_types = import_module('modules.computer.types.types')
_m_errors = import_module('modules.computer.types.errors.errors')
Types = _m_types.Types
Unknown = _m_errors.Unknown
ID = uuid.UUID('01900000-0000-7000-8000-0000000000a1').bytes
OTHER = uuid.UUID('01900000-0000-7000-8000-0000000000a2').bytes

class Equal:
    type_id = ID

    def values_equal(self, a: bytes, b: bytes) -> bool:
        return a == b

class Ordered(Equal):

    def compare_values(self, a: bytes, b: bytes) -> int:
        return (a > b) - (a < b)

class Registry(unittest.TestCase):

    def test_a_registered_type_is_found_by_its_id(self) -> None:
        types = Types()
        kind = Ordered()
        self.assertIsNone(types.register(kind))
        self.assertIs(types.get_by_id(ID), kind)

    def test_an_unregistered_id_is_refused(self) -> None:
        self.assertEqual(Types().get_value_order(OTHER), Unknown.NOT_REGISTERED)
        self.assertEqual(Types().get_value_equality(OTHER), Unknown.NOT_REGISTERED)

    def test_a_type_that_declares_no_order_is_refused_for_order_and_serves_equality(self) -> None:
        types = Types()
        kind = Equal()
        types.register(kind)
        self.assertEqual(types.get_value_order(ID), Unknown.NO_ORDER)
        self.assertIs(types.get_value_equality(ID), kind)

    def test_a_type_that_declares_no_equality_is_refused_for_both(self) -> None:
        class Bare:
            type_id = ID
        types = Types()
        types.register(Bare())
        self.assertEqual(types.get_value_equality(ID), Unknown.NO_EQUALITY)
        self.assertEqual(types.get_value_order(ID), Unknown.NO_ORDER)

    def test_a_type_registered_twice_is_refused(self) -> None:
        types = Types()
        types.register(Ordered())
        self.assertEqual(types.register(Ordered()), Unknown.REGISTERED)

if __name__ == '__main__':
    unittest.main()
