#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for reading the normative-references lists, in `modules-plugable/knowledge/documentation/services/normative_references.py`.

    python modules-plugable/knowledge/documentation/tests/normative_references.py

The subject is the reader of the lists the rule
[Normative References](../../rules/normative_references/normative_references.md)
declares, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

The shape is pinned on lists and documents of the suite's own, in a scratch
folder; on the real checkout only that Memar's place holds a list for every
kind and for every act, each with entries, so no pin holds a copy of a list.

What is pinned, and what each pin is for:

  Place        Only files named `normative_references-<word>.md` directly in a
               declared place are lists; a file of another name, one below the
               place, and a place that is no folder give none.
  Entry        An entry's label, link, target file, anchor, why and mark are
               read from its one line, with its line number; a drop is read as
               a drop with its reason and no mark.
  NotEntries   A line inside a fenced block, an indented one, a link in the
               list's sentence, and a line with no link are not entries.
  Links        A root-relative link names no file and says so; an entry with no
               anchor names the whole document.
  Published    In a project's list, a link at Memar's published address names
               that file of the Memar checkout the place was given, read and
               hashed from there; a relative link names the place's own
               repository; with no checkout given, the address names no file.
               The address is built from the one Memar is downloaded from.
  Hash         The current hash of an entry's section is what
               `memar content get-section FILE '#anchor' --hash` prints, and None
               for an anchor no heading answers to.
  Real         Memar's place holds a list for every kind and for every act.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
PUBLISH_BRANCH = _m_fs_memar.PUBLISH_BRANCH
PUBLISHED_PAGES = _m_fs_memar.PUBLISHED_PAGES
PUBLISHED_REPOSITORY = _m_fs_memar.PUBLISHED_REPOSITORY
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
_m_content_section = import_module('modules-plugable.computer.codec.markdown.services.content_section')
by_anchor = _m_content_section.by_anchor
section_hash = _m_content_section.section_hash
_m_normative_references = import_module('modules-plugable.knowledge.documentation.services.normative_references')
EVERY_ACT = _m_normative_references.EVERY_ACT
LIST_NAME = _m_normative_references.LIST_NAME
MEMAR_REPOSITORY = _m_normative_references.MEMAR_REPOSITORY
Place = _m_normative_references.Place
current_hash = _m_normative_references.current_hash
lists = _m_normative_references.lists
memar_place = _m_normative_references.memar_place
_m_task_kind = import_module('modules.management.task.labels.task_kind')
TaskKind = _m_task_kind.TaskKind
ROOT = SCRIPTS.parent.parent
DOC = '# Doc\n\n## Abstract\nDOC-ABSTRACT\n\n## One\nONE-TEXT\n\n### Inner\nINNER-TEXT\n\n## Two\nTWO-TEXT\n'
WORD = 'alpha'

def list_text(*lines: str) -> str:
    return '# Normative References — Alpha\nWhy this act reads these, with [a link](../docs/doc.md#one) that is no entry.\n\n' + '\n'.join(lines) + '\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.top = Path(scratch.name).resolve()
        (self.top / 'docs').mkdir()
        (self.top / 'docs' / 'doc.md').write_text(DOC, encoding='utf-8', newline='\n')
        self.folder = self.top / 'rules'
        self.folder.mkdir()
        self.place = Place('fixture', self.top, self.folder)

    def write(self, name: str, text: str) -> Path:
        path = self.folder / name
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def entries(self, *lines: str):
        self.write(LIST_NAME.format(word=WORD), list_text(*lines))
        found = lists([self.place])
        self.assertEqual(len(found), 1)
        return found[0].entries

class Place_(Fixture):

    def test_only_files_named_like_a_list_directly_in_the_place_are_lists(self) -> None:
        self.write(LIST_NAME.format(word=WORD), list_text())
        self.write(LIST_NAME.format(word=EVERY_ACT), list_text())
        self.write('other.md', list_text())
        (self.folder / 'below').mkdir()
        (self.folder / 'below' / LIST_NAME.format(word='beta')).write_text(list_text(), encoding='utf-8')
        found = lists([self.place])
        self.assertEqual(sorted((found_list.word for found_list in found)), [WORD, EVERY_ACT])
        self.assertTrue(all((found_list.place == self.place for found_list in found)))

    def test_a_place_that_is_no_folder_gives_no_list(self) -> None:
        self.assertEqual(lists([Place('fixture', self.top, self.top / 'nowhere')]), [])

class Entry(Fixture):

    def test_an_entry_is_read_from_its_one_line(self) -> None:
        entry, = self.entries('- [Doc → One](../docs/doc.md#one) — the reason it is read. `reviewed 0123456789ab`')
        self.assertEqual(entry.line, 4)
        self.assertEqual(entry.label, 'Doc → One')
        self.assertEqual(entry.link, '../docs/doc.md#one')
        self.assertEqual(entry.target, (self.top / 'docs' / 'doc.md').resolve())
        self.assertEqual(entry.path, 'docs/doc.md')
        self.assertEqual(entry.anchor, 'one')
        self.assertEqual(entry.why, 'the reason it is read.')
        self.assertEqual(entry.reviewed, '0123456789ab')
        self.assertFalse(entry.drops)
        self.assertEqual(entry.where, f'rules/{LIST_NAME.format(word=WORD)}:4')

    def test_an_entry_with_no_mark_has_none(self) -> None:
        entry, = self.entries('- [Doc → One](../docs/doc.md#one) — the reason it is read.')
        self.assertIsNone(entry.reviewed)
        self.assertEqual(entry.why, 'the reason it is read.')

    def test_a_drop_is_read_with_its_reason_and_no_mark(self) -> None:
        entry, = self.entries('- Not read here: [Doc → Two](../docs/doc.md#two) — this project has no such step.')
        self.assertTrue(entry.drops)
        self.assertEqual(entry.why, 'this project has no such step.')
        self.assertIsNone(entry.reviewed)

    def test_a_drop_with_no_reason_has_an_empty_why(self) -> None:
        entry, = self.entries('- Not read here: [Doc → Two](../docs/doc.md#two)')
        self.assertTrue(entry.drops)
        self.assertEqual(entry.why, '')

class NotEntries(Fixture):

    def test_lines_of_other_shapes_are_not_entries(self) -> None:
        found = self.entries('```', '- [Doc → One](../docs/doc.md#one) — inside a fence. `reviewed 0123456789ab`', '```', '  - [Doc → One](../docs/doc.md#one) — indented.', '- a line with no link', '- [Doc → Two](../docs/doc.md#two) — the one entry.')
        self.assertEqual([entry.anchor for entry in found], ['two'])

class Links(Fixture):

    def test_a_root_relative_link_names_no_file(self) -> None:
        entry, = self.entries('- [Doc → One](/docs/doc.md#one) — root-relative.')
        self.assertTrue(entry.root_relative)
        self.assertIsNone(entry.target)
        self.assertIsNone(entry.path)

    def test_an_entry_with_no_anchor_names_the_whole_document(self) -> None:
        entry, = self.entries('- [Doc](../docs/doc.md) — the whole document.')
        self.assertEqual(entry.anchor, '')
        self.assertEqual(current_hash(entry), section_hash(DOC))

class Published(Fixture):
    """A project's list naming a passage of Memar by Memar's published address."""

    def setUp(self) -> None:
        super().setUp()
        self.memar = self.top / 'memar'
        (self.memar / 'docs').mkdir(parents=True)
        (self.memar / 'docs' / 'doc.md').write_text(DOC.replace('TWO-TEXT', 'MEMAR-TWO'), encoding='utf-8', newline='\n')
        self.place = Place('fixture', self.top, self.folder, self.memar)

    def test_a_published_address_names_the_section_in_memars_checkout(self) -> None:
        entry, = self.entries(f'- [Memar → Two]({PUBLISHED_PAGES}docs/doc.md#two) — why. `reviewed 0123456789ab`')
        self.assertTrue(entry.published)
        self.assertEqual(entry.target, (self.memar / 'docs' / 'doc.md').resolve())
        self.assertEqual(entry.path, 'docs/doc.md')
        self.assertEqual(entry.repository, MEMAR_REPOSITORY)
        self.assertEqual(entry.anchor, 'two')
        self.assertEqual(current_hash(entry), section_hash(by_anchor(DOC.replace('TWO-TEXT', 'MEMAR-TWO'), 'two')))

    def test_a_relative_link_names_the_places_own_repository(self) -> None:
        entry, = self.entries('- [Doc → Two](../docs/doc.md#two) — why.')
        self.assertFalse(entry.published)
        self.assertEqual(entry.repository, 'fixture')
        self.assertEqual(entry.target, (self.top / 'docs' / 'doc.md').resolve())

    def test_with_no_checkout_given_a_published_address_names_no_file(self) -> None:
        self.place = Place('fixture', self.top, self.folder)
        entry, = self.entries(f'- [Memar → Two]({PUBLISHED_PAGES}docs/doc.md#two) — why.')
        self.assertIsNone(entry.target)
        self.assertIsNone(entry.path)

    def test_the_published_address_is_the_one_memar_is_downloaded_from(self) -> None:
        from bundles.memar.services.install.services.project import SCRIPTS_RAW
        self.assertTrue(PUBLISHED_PAGES.startswith(f'https://github.com/{PUBLISHED_REPOSITORY}/blob/{PUBLISH_BRANCH}/'))
        self.assertIn(f'/{PUBLISHED_REPOSITORY}/{PUBLISH_BRANCH}/', SCRIPTS_RAW)

class Hash(Fixture):

    def test_the_hash_is_the_sections_as_section_hash_prints_it(self) -> None:
        entry, = self.entries('- [Doc → One](../docs/doc.md#one) — why.')
        self.assertEqual(current_hash(entry), section_hash(by_anchor(DOC, 'one')))

    def test_an_edit_in_a_subsection_changes_the_hash(self) -> None:
        entry, = self.entries('- [Doc → One](../docs/doc.md#one) — why.')
        before = current_hash(entry)
        (self.top / 'docs' / 'doc.md').write_text(DOC.replace('INNER-TEXT', 'INNER-EDITED'), encoding='utf-8', newline='\n')
        self.assertNotEqual(current_hash(entry), before)

    def test_an_anchor_no_heading_answers_to_has_no_hash(self) -> None:
        entry, = self.entries('- [Doc → Gone](../docs/doc.md#gone) — why.')
        self.assertIsNone(current_hash(entry))

class Real(unittest.TestCase):

    def test_memars_place_holds_a_list_for_every_kind_and_every_act_each_with_entries(self) -> None:
        found = {found_list.word: found_list for found_list in lists([memar_place(ROOT)])}
        for word in (EVERY_ACT, *TaskKind.words()):
            with self.subTest(word=word):
                self.assertIn(word, found)
                self.assertTrue(found[word].entries)
if __name__ == '__main__':
    unittest.main(verbosity=2)
