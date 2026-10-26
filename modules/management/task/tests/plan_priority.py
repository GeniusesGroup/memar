#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the priority type in `modules/management/task/plan/primitive/priority.py`.

    python modules/management/task/tests/plan_priority.py

The subject is a plan's priority, declared once: how soon a queued task is
taken, a whole number from 1 to 10, the higher sooner, the middle value when a
plan has none or a hand-edited one is not a number in range. Named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)):
the services that rank, check and describe a priority call the type, and the
words a help prints come from it.

Nothing here writes.

What is pinned, and what each pin is for:

  Bounds    The lowest, the highest and the default are the type's own values.
  Reading   Text is a priority only when it is a whole number within the
            bounds; a plan's front matter reads as the default otherwise.
  Checking  A value from a person is refused with the bounds named.
  Words     What a help says of the range comes from the type.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.management.task.plan.primitive.priority import Priority
from modules.management.task.plan.primitive.plan_key import PlanKey

class Bounds(unittest.TestCase):

    def test_the_lowest_the_highest_and_the_default(self) -> None:
        self.assertEqual((Priority.LOWEST, Priority.HIGHEST, Priority.DEFAULT), (1, 10, 5))

    def test_each_is_a_priority_and_a_whole_number(self) -> None:
        for value in (Priority.LOWEST, Priority.HIGHEST, Priority.DEFAULT):
            self.assertIsInstance(value, Priority)
            self.assertIsInstance(value, int)

class Reading(unittest.TestCase):

    def test_a_whole_number_within_the_bounds_is_a_priority(self) -> None:
        for text, expected in (('1', 1), ('5', 5), ('10', 10), (' 7 ', 7)):
            with self.subTest(text=text):
                self.assertEqual(Priority.read(text), expected)

    def test_anything_else_is_not(self) -> None:
        for text in ('', '0', '11', '-1', '5.5', 'high', '5 6'):
            with self.subTest(text=text):
                self.assertIsNone(Priority.read(text))

    def test_a_plans_front_matter_reads_as_its_priority_or_the_default(self) -> None:
        key = PlanKey.PRIORITY.key
        self.assertEqual(Priority.of({key: '8'}), 8)
        self.assertEqual(Priority.of({key: '99'}), Priority.DEFAULT)
        self.assertEqual(Priority.of({}), Priority.DEFAULT)
        self.assertEqual(Priority.of(None), Priority.DEFAULT)

class Checking(unittest.TestCase):

    def test_a_value_in_range_is_returned_as_a_priority(self) -> None:
        for value in ('3', 3):
            with self.subTest(value=value):
                checked = Priority.checked(value)
                self.assertEqual(checked, 3)
                self.assertIsInstance(checked, Priority)

    def test_a_value_out_of_range_is_refused_naming_the_bounds(self) -> None:
        for value in ('0', '11', 'x', 11):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit) as refused:
                    Priority.checked(value)
                message = str(refused.exception.code)
                self.assertIn(str(Priority.LOWEST), message)
                self.assertIn(str(Priority.HIGHEST), message)

class Words(unittest.TestCase):

    def test_the_range_is_said_from_the_bounds(self) -> None:
        self.assertEqual(Priority.range_words(), f'{Priority.LOWEST} to {Priority.HIGHEST}')

    def test_the_default_is_said_from_the_default(self) -> None:
        self.assertIn(str(Priority.DEFAULT), Priority.default_words())
if __name__ == '__main__':
    unittest.main(verbosity=2)
