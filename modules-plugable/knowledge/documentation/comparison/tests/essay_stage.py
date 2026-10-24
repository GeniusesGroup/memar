#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `EssayStage` in `primitive/essay_stage.py`.

    python modules-plugable/knowledge/documentation/comparison/tests/essay_stage.py

The subject is the ten stages a comparison essay carries, as numbered sections in this order. Named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../../modules/process/test/rules/test-placement/test-placement.md).

What is pinned: the headings are those the specification names, in its order, each with a meaning; each is read back from its text in any case; any other text is no member.
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
_m_essay_stage = import_module('modules-plugable.knowledge.documentation.comparison.primitive.essay_stage')
EssayStage = _m_essay_stage.EssayStage
WORDS = ('What each project is', 'Source status of the inspected checkout', 'What the other project has that this one does not', 'Where this project is stronger', 'Failure modes in the other project', 'Costs and limits on both sides', 'The adoption filter', 'The possible relationship between the projects', 'The decision', 'Open for critique')

class EssayStagePins(unittest.TestCase):

    def test_the_headings_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(EssayStage.headings(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in EssayStage:
            with self.subTest(member=member.name):
                self.assertTrue(member.purpose)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in EssayStage:
            self.assertIs(EssayStage.read(' ' + member.heading.upper() + ' '), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(EssayStage.read('no such heading'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
