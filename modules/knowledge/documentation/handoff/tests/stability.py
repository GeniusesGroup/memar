#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `Stability` in `primitive/stability.py`.

    python modules/knowledge/documentation/handoff/tests/stability.py

The subject is the stability a handoff marks on every assumption. Named for the file that holds it per
[Test Naming](../../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../process/test/rules/test-placement/test-placement.md).

What is pinned: the words are those the specification names, in its order, each with a meaning; each is read back from its text in any case; any other text is no member.
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

from modules.knowledge.documentation.handoff.primitive.stability import Stability

WORDS = ('Strong', 'Weak', 'Unexamined')


class StabilityPins(unittest.TestCase):
    def test_the_words_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(Stability.words(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in Stability:
            with self.subTest(member=member.name):
                self.assertTrue(member.meaning)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in Stability:
            self.assertIs(Stability.read(" " + member.word.upper() + " "), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(Stability.read("no such word"))




if __name__ == "__main__":
    unittest.main(verbosity=2)
