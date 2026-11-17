# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 30
COST = {'subprocesses': 0, 'writes_files': False, 'clock_waits': False}
SUBJECT = 'Types complete-identity catalog admission'
CONTRACT = 'modules/computer/types/protocol/types.eng.kh'
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
from modules.identity.identifier.errors.value import Identifier_Error_InvalidBytes
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

    def test_malformed_registration_refuses_before_catalog_mutation(self) -> None:
        types = Types()
        original = Ordered()
        types.register(original)
        for value in (bytes(8), bytes(15), bytes(17), bytes(32), bytearray(16), ID.hex(), 7, None):
            with self.subTest(value=value):
                class Invalid:
                    type_id = value
                self.assertIsInstance(types.register(Invalid()), Identifier_Error_InvalidBytes)
                self.assertIs(types.get_by_id(ID), original)

    def test_missing_identity_is_owner_refusal(self) -> None:
        self.assertIsInstance(Types().register(object()), Identifier_Error_InvalidBytes)

    def test_malformed_lookup_propagates_owner_refusal(self) -> None:
        types = Types()
        for value in (bytes(8), bytes(17), bytearray(16), ID.hex(), None):
            for method in (types.get_by_id, types.get_value_equality, types.get_value_order):
                with self.subTest(value=value, method=method.__name__):
                    self.assertIsInstance(method(value), Identifier_Error_InvalidBytes)

    def test_complete_zero_identity_is_not_an_implicit_missing_sentinel(self) -> None:
        class Zero:
            type_id = bytes(16)
        types = Types()
        value = Zero()
        self.assertIsNone(types.register(value))
        self.assertIs(types.get_by_id(bytes(16)), value)

    def test_full_identities_with_the_same_short_prefix_remain_distinct(self) -> None:
        class Other(Ordered):
            type_id = OTHER
        types = Types()
        first = Ordered()
        second = Other()
        self.assertIsNone(types.register(first))
        self.assertIsNone(types.register(second))
        self.assertIs(types.get_by_id(ID), first)
        self.assertIs(types.get_by_id(OTHER), second)

    def test_conflicting_registration_preserves_the_admitted_type(self) -> None:
        types = Types()
        original = Ordered()
        self.assertIsNone(types.register(original))
        self.assertEqual(types.register(Equal()), Unknown.REGISTERED)
        self.assertIs(types.get_by_id(ID), original)

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
