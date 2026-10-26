#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `EntrySection` in `primitive/entry_section.py`.

    python modules-plugable/knowledge/documentation/changelog/tests/entry_section.py

The subject is the content sections of a changelog entry: the one every entry has, then the optional catalog. Named for the file that holds it per
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
TOP = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services')); sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
_m_entry_section = import_module('modules-plugable.knowledge.documentation.changelog.primitive.entry_section')
EntrySection = _m_entry_section.EntrySection
WORDS = ('What changed', 'Considered and not done', 'Surveyed', 'Examined and not adopted', 'Related work', 'Deliberation', 'Decision')

class EntrySectionPins(unittest.TestCase):

    def test_the_headings_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(EntrySection.headings(), WORDS)

    def test_each_has_a_meaning(self) -> None:
        for member in EntrySection:
            with self.subTest(member=member.name):
                self.assertTrue(member.purpose)

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in EntrySection:
            self.assertIs(EntrySection.read(' ' + member.heading.upper() + ' '), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(EntrySection.read('no such heading'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
