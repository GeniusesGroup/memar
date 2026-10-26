#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `ReportPart` in `primitive/report_part.py`.

    python modules/management/task/tests/report_part.py

The subject is the parts under a task report's front matter, in order, and the hand-back part a task adds when it needs a decision. Named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

What is pinned: the headings are those the specification names, in its order, each with a meaning; each is read back from its text in any case; any other text is no member.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services')); sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
from modules.management.task.report.primitive.report_part import ReportPart
WORDS = ('What ran', 'Check', 'Result', 'Left open', 'Decisions needed')

class ReportPartPins(unittest.TestCase):

    def test_the_headings_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(ReportPart.headings(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in ReportPart:
            with self.subTest(member=member.name):
                self.assertTrue(member.purpose)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in ReportPart:
            self.assertIs(ReportPart.read(' ' + member.heading.upper() + ' '), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(ReportPart.read('no such heading'))

    def test_the_hand_back_part_is_not_one_every_report_has(self) -> None:
        self.assertEqual(ReportPart.every_report(), ('What ran', 'Check', 'Result', 'Left open'))
        self.assertTrue(ReportPart.DECISIONS_NEEDED.hand_back)
if __name__ == '__main__':
    unittest.main(verbosity=2)
