#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `ResearchSection` in `primitive/research_section.py`.

    python modules/knowledge/documentation/research/tests/research_section.py

The subject is the sections of a research: the mandatory core first, then the optional catalog. Named for the file that holds it per
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

from modules.knowledge.documentation.research.primitive.research_section import ResearchSection

WORDS = ('Table of Contents', 'Status', 'Question and Goals', 'Participants', 'Methodology', 'Findings', 'Open Questions', 'Conclusion', 'Related Artifacts', 'Notes')


class ResearchSectionPins(unittest.TestCase):
    def test_the_headings_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(ResearchSection.headings(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in ResearchSection:
            with self.subTest(member=member.name):
                self.assertTrue(member.purpose)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in ResearchSection:
            self.assertIs(ResearchSection.read(" " + member.heading.upper() + " "), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(ResearchSection.read("no such heading"))



    def test_the_core_is_the_first_five(self) -> None:
        self.assertEqual([s.name for s in ResearchSection if s.mandatory], [s.name for s in list(ResearchSection)[:5]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
