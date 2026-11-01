#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules').parent
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
Section = import_module('modules.knowledge.content.primitive.section').Section
Catalog = import_module('modules.knowledge.content.primitive.catalog').Catalog
SECTION_HEADER = 'from modules.knowledge.content.primitive.section import Section\n\n'
WORD_HEADER = 'from modules.knowledge.content.primitive.word import Word\n\n'

def declare_section(folder: Path, file: str, name: str, heading: str, order: int, labels: tuple[str, ...]) -> None:
    body = f'class {name}(Section):\n    heading = {heading!r}\n    purpose = "what it is for"\n    order = {order}\n    labels = {labels!r}\n'
    (folder / f'{file}.py').write_text(SECTION_HEADER + body, encoding='utf-8')

def declare_word(folder: Path, file: str, name: str, word: str, order: int, labels: tuple[str, ...]) -> None:
    body = f'class {name}(Word):\n    word = {word!r}\n    meaning = "what it means"\n    order = {order}\n    labels = {labels!r}\n'
    (folder / f'{file}.py').write_text(WORD_HEADER + body, encoding='utf-8')

class CatalogPins(unittest.TestCase):

    def setUp(self) -> None:
        self.dir = tempfile.TemporaryDirectory()
        self.folder = Path(self.dir.name)

    def tearDown(self) -> None:
        self.dir.cleanup()

    def test_the_order_of_the_types_is_theirs_not_the_file_names(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 2, ('s',))
        declare_section(self.folder, 'beta', 'Beta', 'Beta', 1, ('s',))
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Beta', 'Alpha'))

    def test_equal_orders_fall_back_to_the_class_name(self) -> None:
        declare_section(self.folder, 'one', 'Zed', 'Zed', 1, ('s',))
        declare_section(self.folder, 'two', 'Abe', 'Abe', 1, ('s',))
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Abe', 'Zed'))

    def test_only_the_types_with_the_label_are_collected(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s', 'extra'))
        declare_section(self.folder, 'beta', 'Beta', 'Beta', 2, ('t',))
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Alpha',))
        self.assertEqual(Catalog(self.folder, 'extra').headings(), ('Alpha',))
        self.assertEqual(len(Catalog(self.folder, 'none')), 0)

    def test_it_iterates_the_types_themselves(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s',))
        declare_section(self.folder, 'beta', 'Beta', 'Beta', 2, ('s',))
        catalog = Catalog(self.folder, 's')
        self.assertEqual(len(catalog), 2)
        self.assertTrue(all(isinstance(member, type) and issubclass(member, Section) for member in catalog))

    def test_read_strips_and_ignores_case(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha Beta', 1, ('s',))
        catalog = Catalog(self.folder, 's')
        self.assertIs(catalog.read('  ALPHA beta '), next(iter(catalog)))

    def test_read_gives_none_for_any_other_text(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s',))
        self.assertIsNone(Catalog(self.folder, 's').read('no such heading'))

    def test_words_are_collected_read_and_listed(self) -> None:
        declare_word(self.folder, 'pending', 'Pending', 'Pending', 1, ('w',))
        declare_word(self.folder, 'done', 'Done', 'Done', 2, ('w',))
        declare_word(self.folder, 'rejected', 'Rejected', 'Rejected', 3, ('w',))
        catalog = Catalog(self.folder, 'w')
        self.assertEqual(catalog.words(), ('Pending', 'Done', 'Rejected'))
        self.assertEqual(catalog.listing(), 'Pending, Done, or Rejected')
        self.assertIs(catalog.read(' DONE '), next(member for member in catalog if member.word == 'Done'))

    def test_a_single_word_lists_as_itself(self) -> None:
        declare_word(self.folder, 'only', 'Only', 'Only', 1, ('w',))
        self.assertEqual(Catalog(self.folder, 'w').listing(), 'Only')

    def test_sections_and_words_of_one_label_live_in_one_catalog(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('m',))
        declare_word(self.folder, 'pending', 'Pending', 'Pending', 2, ('m',))
        self.assertEqual(len(Catalog(self.folder, 'm')), 2)

    def test_files_that_start_with_an_underscore_and_other_files_are_skipped(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s',))
        declare_section(self.folder, '_hidden', 'Hidden', 'Hidden', 2, ('s',))
        (self.folder / 'notes.txt').write_text('x', encoding='utf-8')
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Alpha',))

    def test_a_file_that_declares_no_section_or_word_is_not_run(self) -> None:
        (self.folder / 'other.py').write_text('raise RuntimeError("run")\n', encoding='utf-8')
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s',))
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Alpha',))

    def test_a_class_only_imported_by_a_file_is_not_collected_twice(self) -> None:
        declare_section(self.folder, 'alpha', 'Alpha', 'Alpha', 1, ('s',))
        (self.folder / 'beta.py').write_text(SECTION_HEADER + 'class Beta(Section):\n    heading = "Beta"\n    order = 2\n    labels = ("s",)\n', encoding='utf-8')
        (self.folder / 'gamma.py').write_text('from alpha_stub import Alpha\n', encoding='utf-8')
        self.assertEqual(Catalog(self.folder, 's').headings(), ('Alpha', 'Beta'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
