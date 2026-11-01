#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules').parent
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
RecordKey = import_module('modules.knowledge.content.primitive.record_key').RecordKey
RecordKeySet = import_module('modules.knowledge.content.primitive.record_key_set').RecordKeySet

class Sample(RecordKeySet):
    ALPHA = RecordKey('alpha', 'the first')
    BETA = RecordKey('beta', 'the second', 'Beta Key', ('old beta',))

class RecordKeyPins(unittest.TestCase):

    def test_a_key_holds_what_it_says_of_itself(self) -> None:
        key = Sample.BETA
        self.assertEqual((key.key, key.description, key.written, key.earlier), ('beta', 'the second', 'Beta Key', ('old beta',)))

    def test_the_written_form_defaults_to_the_capitalized_key(self) -> None:
        self.assertEqual(Sample.ALPHA.written, 'Alpha')

    def test_a_set_iterates_its_keys_in_the_order_declared(self) -> None:
        self.assertEqual([key.key for key in Sample], ['alpha', 'beta'])
        self.assertEqual(tuple(Sample), (Sample.ALPHA, Sample.BETA))

    def test_neither_is_an_enum(self) -> None:
        self.assertFalse(hasattr(Sample, '__members__'))
        self.assertFalse(hasattr(RecordKey, '__members__'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
