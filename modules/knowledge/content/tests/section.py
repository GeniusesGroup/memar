#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules').parent
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
Section = import_module('modules.knowledge.content.primitive.section').Section

class SectionPins(unittest.TestCase):

    def test_a_section_type_says_everything_about_itself_by_class_attributes(self) -> None:
        class Risks(Section):
            heading = 'Risks'
            purpose = 'what could go wrong'
            order = 3
            labels = ('optional-section',)
        self.assertEqual((Risks.heading, Risks.purpose, Risks.order, Risks.labels), ('Risks', 'what could go wrong', 3, ('optional-section',)))

    def test_the_other_texts_default_to_empty(self) -> None:
        class Risks(Section):
            heading = 'Risks'
        self.assertEqual((Risks.use, Risks.distinct_from, Risks.reason, Risks.labels), ('', '', '', ()))

    def test_it_is_a_plain_class_with_no_members(self) -> None:
        self.assertFalse(hasattr(Section, '__members__'))
        self.assertEqual(Section.__mro__, (Section, object))

    def test_it_is_not_a_dataclass(self) -> None:
        self.assertFalse(hasattr(Section, '__dataclass_fields__'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
