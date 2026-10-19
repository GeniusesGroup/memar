#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `HandoffSection` in `primitive/handoff_section.py`.

    python modules/knowledge/documentation/handoff/tests/handoff_section.py

The subject is the open catalog of state sections a handoff may carry. Named for the file that holds it per
[Test Naming](../../../../process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the module that owns it per
[Test Placement](../../../../process/test/rules/test-placement/test-placement.md).

What is pinned: the headings are those the specification names, in its order, each with a meaning; each is read back from its text in any case; any other text is no member.
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

from modules.knowledge.documentation.handoff.primitive.handoff_section import HandoffSection

WORDS = ('Topic & Purpose', 'Status', 'Decisions', 'Ambiguities Resolved', 'Open Questions', 'Anticipated Work', 'Assumptions', 'Key Definitions Established', 'Proposed Next Steps', 'Related Artifacts', 'Notes')


class HandoffSectionPins(unittest.TestCase):
    def test_the_headings_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(HandoffSection.headings(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in HandoffSection:
            with self.subTest(member=member.name):
                self.assertTrue(member.purpose)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in HandoffSection:
            self.assertIs(HandoffSection.read(" " + member.heading.upper() + " "), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(HandoffSection.read("no such heading"))




if __name__ == "__main__":
    unittest.main(verbosity=2)
