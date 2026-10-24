#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `Confidence` in `primitive/confidence.py`.

    python modules-plugable/knowledge/documentation/handoff/tests/confidence.py

The subject is the confidence a handoff marks on every decision. Named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md).

What is pinned: the words are those the specification names, in its order, each with a meaning; each is read back from its text in any case; any other text is no member.
"""
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = TESTS.parents[4]
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services')); sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
_m_confidence = import_module('modules-plugable.knowledge.documentation.handoff.primitive.confidence')
Confidence = _m_confidence.Confidence
WORDS = ('Decided', 'Tentative', 'Explored-but-unresolved', 'Deferred')

class ConfidencePins(unittest.TestCase):

    def test_the_words_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(Confidence.words(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in Confidence:
            with self.subTest(member=member.name):
                self.assertTrue(member.meaning)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in Confidence:
            self.assertIs(Confidence.read(' ' + member.word.upper() + ' '), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(Confidence.read('no such word'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
