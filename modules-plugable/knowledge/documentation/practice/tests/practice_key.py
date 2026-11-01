#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services')); sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
_m_practice_key = import_module('modules-plugable.knowledge.documentation.practice.primitive.practice_key')
PracticeKey = _m_practice_key.PracticeKey

class PracticeKeyPins(unittest.TestCase):

    def test_the_keys_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual([key.key for key in PracticeKey], ['name', 'description'])

    def test_each_has_a_description_and_a_written_form(self) -> None:
        for key in PracticeKey:
            self.assertTrue(key.description)
            self.assertTrue(key.written)

    def test_practice_keys_are_written_in_lower_case(self) -> None:
        self.assertEqual([key.written for key in PracticeKey], ['name', 'description'])
if __name__ == '__main__':
    unittest.main(verbosity=2)
