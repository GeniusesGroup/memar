#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `QuestionField` in `primitive/question_field.py`.

    python modules/knowledge/documentation/handoff/tests/question_field.py

The subject is the six fields an Open Questions entry carries. Named for the file that holds it per
[Test Naming](../../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../process/test/rules/test-placement/test-placement.md).

What is pinned: the six fields in the specification's order, each with a meaning; the four `content check` warns about are State, Options, Anchor and Blocks; a field is read back in any case.
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

from modules.knowledge.documentation.handoff.primitive.question_field import QuestionField


class QuestionFieldPins(unittest.TestCase):
    def test_the_six_fields_in_the_specifications_order(self) -> None:
        self.assertEqual(QuestionField.words(), ("Heading", "State", "Options", "Anchor", "Blocks", "Asked"))

    def test_four_are_warned_about(self) -> None:
        self.assertEqual([f.word for f in QuestionField if f.warned], ["State", "Options", "Anchor", "Blocks"])

    def test_each_has_a_meaning_and_is_read_back(self) -> None:
        for field in QuestionField:
            self.assertTrue(field.meaning)
            self.assertIs(QuestionField.read(field.word.upper()), field)


if __name__ == "__main__":
    unittest.main(verbosity=2)
