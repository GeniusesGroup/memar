#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `ExplanationKey` in `primitive/explanation_key.py`.

    python modules/knowledge/documentation/explanation/tests/explanation_key.py

The subject is the front-matter keys a Explanation-facet document carries. Named for the file that holds it per
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

from modules.knowledge.documentation.explanation.primitive.explanation_key import ExplanationKey


class ExplanationKeyPins(unittest.TestCase):
    def test_the_keys_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual([key.key for key in ExplanationKey], ['title', 'status', 'start date', 'id'])

    def test_each_has_a_description_and_a_written_form(self) -> None:
        for key in ExplanationKey:
            self.assertTrue(key.description)
            self.assertTrue(key.written)

    def test_id_and_start_date_are_the_fields_a_session_record_shares(self) -> None:
        from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
        self.assertEqual(ExplanationKey.ID.value, PlanKey.ID.value)
        self.assertEqual(ExplanationKey.START_DATE.value, PlanKey.START_DATE.value)


if __name__ == "__main__":
    unittest.main(verbosity=2)
