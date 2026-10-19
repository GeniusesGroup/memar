#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `PracticeKey` in `primitive/practice_key.py`.

    python modules/knowledge/documentation/practice/tests/practice_key.py

The subject is the front-matter keys a Practice-facet document carries. Named for the file that holds it per
[Test Naming](../../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../process/test/rules/test-placement/test-placement.md).

What is pinned: the keys are the specification's, in its order, each with a description and a written form.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TOP = TESTS.parents[4]
sys.path.insert(0, str(TOP / ".agents" / "scripts"))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True

from modules.knowledge.documentation.practice.primitive.practice_key import PracticeKey


class PracticeKeyPins(unittest.TestCase):
    def test_the_keys_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual([key.key for key in PracticeKey], ['name', 'description'])

    def test_each_has_a_description_and_a_written_form(self) -> None:
        for key in PracticeKey:
            self.assertTrue(key.description)
            self.assertTrue(key.written)

    def test_practice_keys_are_written_in_lower_case(self) -> None:
        self.assertEqual([key.written for key in PracticeKey], ["name", "description"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
