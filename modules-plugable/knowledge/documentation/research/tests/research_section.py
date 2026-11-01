#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
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
Catalog = import_module('modules.knowledge.content.primitive.catalog').Catalog
BUDGET_SECONDS = 10
FOLDER = TESTS.parent / 'primitive'
CATALOG = Catalog(FOLDER, 'research-section')
NAMES = ('Table of Contents', 'Status', 'Question and Goals', 'Participants', 'Methodology', 'Findings', 'Open Questions', 'Conclusion', 'Related Artifacts', 'Notes')

class ResearchSectionPins(unittest.TestCase):

    def test_the_names_are_the_specifications_in_its_order(self) -> None:
        self.assertEqual(CATALOG.headings(), NAMES)

    def test_each_is_a_type_declared_in_a_file_of_the_folder(self) -> None:
        base = import_module('modules.knowledge.content.primitive.section').Section
        for member in CATALOG:
            with self.subTest(member=member.__name__):
                self.assertTrue(isinstance(member, type) and issubclass(member, base))
                self.assertEqual(Path(sys.modules[member.__module__].__file__).parent, FOLDER)
                self.assertIn('research-section', member.labels)

    def test_each_says_what_it_means(self) -> None:
        for member in CATALOG:
            with self.subTest(member=member.__name__):
                self.assertTrue(member.purpose)

    def test_each_carries_its_own_order(self) -> None:
        self.assertEqual([member.order for member in CATALOG], sorted(member.order for member in CATALOG))
        self.assertEqual(len({member.order for member in CATALOG}), len(CATALOG))

    def test_each_is_read_back_in_any_case(self) -> None:
        for member in CATALOG:
            self.assertIs(CATALOG.read(' ' + member.heading.upper() + ' '), member)

    def test_any_other_text_is_no_member(self) -> None:
        self.assertIsNone(CATALOG.read('no such heading'))

    def test_the_first_five_are_mandatory(self) -> None:
        self.assertEqual([member.heading for member in CATALOG if 'mandatory' in member.labels], list(NAMES[:5]))

if __name__ == '__main__':
    unittest.main(verbosity=2)
