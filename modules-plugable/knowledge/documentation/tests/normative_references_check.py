#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what `memar content check` reports of a normative-references list, in `modules-plugable/knowledge/documentation/services/normative_references_check.py`.

    python modules-plugable/knowledge/documentation/tests/normative_references_check.py

The subject is the governance report of the rule
[Normative References](../../rules/normative_references/normative_references.md):
the checks of proposal v3, section 4.9, on Memar's lists and on a project's. Named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Pinned on lists and documents of the suite's own, in a scratch checkout whose
Memar place is the declared one; on the real checkout only that Memar's lists
report nothing.

What is pinned, and what each pin is for:

  Word          A list whose word names no kind and is not the every-act word
                is a problem that lists the known words.
  Target        An entry whose link names no Markdown file inside the
                repository — outside it, not Markdown, or external — is a
                problem; a missing file or anchor is the anchor check's, and
                `check_file` reports it.
  Mark          An entry with no mark, or one that differs from its section's
                current hash, is a problem that says to re-read the section
                and update the hash.
  Drops         A drop whose passage no Memar list names drops nothing.
  RootRelative  An entry whose link is root-relative is a problem.
  Warnings      A file named like a list outside the declared place is not read
                and is warned of; the same passage twice in one list is warned
                of; neither is a problem.
  Through       `check_file` reports a list's problems with the file's others;
                a file outside the place is not judged as a list.
  Project       A list in a folder its project's `normative_references`
                preference names is judged as a list: a relative link must name
                a Markdown file of the project, a published address a section of
                Memar's checkout; a drop with no reason is a problem, a drop of
                an every-act section is refused, and one of a passage no Memar
                list names drops nothing. Only a drop that removes a passage is
                counted, and `check`'s summary line says how many. A list beside
                or below the declared folders is not judged and is warned of. A
                list of Memar naming a published address is a problem.
  Real          Memar's own lists report no problem.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
PUBLISHED_PAGES = _m_fs_memar.PUBLISHED_PAGES
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import argparse
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
_m_content_check = import_module('modules-plugable.knowledge.documentation.services.content_check')
check_file = _m_content_check.check_file
cmd_check = _m_content_check.cmd_check
_m_content_section = import_module('modules-plugable.computer.codec.markdown.services.content_section')
by_anchor = _m_content_section.by_anchor
section_hash = _m_content_section.section_hash
_m_normative_references = import_module('modules-plugable.knowledge.documentation.services.normative_references')
EVERY_ACT = _m_normative_references.EVERY_ACT
LIST_NAME = _m_normative_references.LIST_NAME
PREFERENCE = _m_normative_references.PREFERENCE
lists = _m_normative_references.lists
memar_place = _m_normative_references.memar_place
_m_normative_references_check = import_module('modules-plugable.knowledge.documentation.services.normative_references_check')
OUTSIDE_WARNING = _m_normative_references_check.OUTSIDE_WARNING
list_drops = _m_normative_references_check.list_drops
list_problems = _m_normative_references_check.list_problems
list_warnings = _m_normative_references_check.list_warnings
from modules.process.project.services.preferences import preferences_path, preferences_text
from modules.management.task.labels.task_kind import TaskKind
ROOT = SCRIPTS.parent.parent
DOC = '# Doc\n\n## Abstract\nDOC-ABSTRACT\n\n## One\nONE-TEXT\n\n## Two\nTWO-TEXT\n'
UP = '../../../../../'
WORD = TaskKind.DESIGN.word

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name).resolve()
        (self.root / 'docs').mkdir()
        (self.root / 'docs' / 'doc.md').write_text(DOC, encoding='utf-8', newline='\n')
        (self.root / 'docs' / 'data.txt').write_text('data\n', encoding='utf-8', newline='\n')
        self.place = memar_place(self.root)
        self.place.folder.mkdir(parents=True)
        self.write(EVERY_ACT, self.entry('one'))

    def entry(self, anchor: str, mark: str | None=None, link: str | None=None) -> str:
        if mark is None:
            found = by_anchor(DOC, anchor)
            mark = section_hash(found) if found else '0' * 12
        return f"- [Doc → {anchor}]({link or f'{UP}docs/doc.md#{anchor}'}) — why. `reviewed {mark}`"

    def write(self, word: str, *entries: str, folder: Path | None=None) -> Path:
        path = (folder or self.place.folder) / LIST_NAME.format(word=word)
        path.write_text(f'# Normative References — {word}\nWhy.\n\n' + '\n'.join(entries) + '\n', encoding='utf-8', newline='\n')
        return path

    def problems(self, word: str, *entries: str) -> list[str]:
        return list_problems(self.write(word, *entries), self.root)

class Word(Fixture):

    def test_a_list_whose_word_names_no_kind_is_a_problem_listing_the_words(self) -> None:
        found = self.problems('modelling', self.entry('two'))
        self.assertEqual(len(found), 1, found)
        self.assertIn("'modelling' names no kind", found[0])
        for word in (EVERY_ACT, *TaskKind.words()):
            self.assertIn(word, found[0])

    def test_a_kinds_list_and_the_every_act_list_are_not(self) -> None:
        self.assertEqual(self.problems(WORD, self.entry('two')), [])
        self.assertEqual(self.problems(EVERY_ACT, self.entry('one')), [])

class Target(Fixture):

    def test_an_entry_naming_no_markdown_file_inside_the_repository_is_a_problem(self) -> None:
        outside = f"- [Out]({UP}../outside.md#x) — why. `reviewed {'0' * 12}`"
        not_markdown = f"- [Data]({UP}docs/data.txt) — why. `reviewed {'0' * 12}`"
        external = f"- [Web](https://example.org/doc.md#x) — why. `reviewed {'0' * 12}`"
        found = self.problems(WORD, outside, not_markdown, external)
        self.assertEqual([problem.split(':')[0] for problem in found], ['line 4', 'line 5', 'line 6'])
        for problem in found:
            self.assertIn('names no Markdown file of this repository', problem)

    def test_a_missing_file_or_anchor_is_left_to_the_anchor_check(self) -> None:
        missing = f"- [Gone]({UP}docs/gone.md#x) — why. `reviewed {'0' * 12}`"
        self.assertEqual(self.problems(WORD, missing, self.entry('nowhere')), [])
        reported = check_file(self.place.folder / LIST_NAME.format(word=WORD), root=self.root)
        self.assertEqual(len(reported), 2, reported)

class Mark(Fixture):

    def test_an_entry_with_no_mark_is_a_problem(self) -> None:
        bare = f'- [Doc → two]({UP}docs/doc.md#two) — why.'
        found, = self.problems(WORD, bare)
        self.assertTrue(found.startswith('line 4: no review mark'), found)

    def test_a_mark_that_differs_from_the_current_hash_is_a_problem(self) -> None:
        found, = self.problems(WORD, self.entry('two', mark='0' * 12))
        self.assertTrue(found.startswith('line 4: changed since reviewed: re-read the section, then update the hash'), found)
        self.assertIn(section_hash(by_anchor(DOC, 'two')), found)

class Drops(Fixture):

    def test_a_drop_whose_passage_no_memar_list_names_drops_nothing(self) -> None:
        drop = f'- Not read here: [Doc → two]({UP}docs/doc.md#two) — not here.'
        found, = self.problems(WORD, drop)
        self.assertTrue(found.startswith('line 4: drops nothing'), found)

    def test_a_drop_of_a_named_passage_is_not(self) -> None:
        drop = f'- Not read here: [Doc → one]({UP}docs/doc.md#one) — not here.'
        self.assertEqual(self.problems(WORD, drop), [])

class RootRelative(Fixture):

    def test_a_root_relative_entry_is_a_problem(self) -> None:
        found, = self.problems(WORD, self.entry('two', link='/docs/doc.md#two'))
        self.assertTrue(found.startswith('line 4: root-relative'), found)

class Warnings(Fixture):

    def test_a_file_named_like_a_list_outside_the_declared_place_is_warned_of(self) -> None:
        elsewhere = self.root / 'docs'
        path = self.write(WORD, self.entry('two'), folder=elsewhere)
        self.assertEqual(list_warnings(path, self.root), ['not read: outside the declared places'])
        self.assertEqual(list_problems(path, self.root), [])

    def test_the_same_passage_twice_in_one_list_is_warned_of(self) -> None:
        path = self.write(WORD, self.entry('two'), self.entry('two'))
        self.assertEqual(list_warnings(path, self.root), ['line 5: names the same passage as line 4'])
        self.assertEqual(list_problems(path, self.root), [])

    def test_an_ordinary_file_has_no_warning(self) -> None:
        self.assertEqual(list_warnings(self.root / 'docs' / 'doc.md', self.root), [])

class Through(Fixture):

    def test_check_file_reports_a_lists_problems(self) -> None:
        path = self.write(WORD, self.entry('two', mark='0' * 12))
        found = check_file(path, root=self.root)
        self.assertEqual(len(found), 1, found)
        self.assertIn('changed since reviewed', found[0])

    def test_check_file_does_not_judge_a_file_outside_the_place_as_a_list(self) -> None:
        path = self.write(WORD, self.entry('two', mark='0' * 12, link='doc.md#two'), folder=self.root / 'docs')
        self.assertEqual(check_file(path, root=self.root), [])
OWN = '# Own\n\n## Mine\nMINE-TEXT\n'

class Project(Fixture):
    """A project inside the scratch checkout, whose preference declares `rules/refs`; Memar's design list names doc.md#two."""

    def setUp(self) -> None:
        super().setUp()
        self.write(WORD, self.entry('two'))
        self.project = self.root / 'orchard'
        (self.project / 'docs').mkdir(parents=True)
        (self.project / 'docs' / 'own.md').write_text(OWN, encoding='utf-8', newline='\n')
        self.refs = self.project / 'rules' / 'refs'
        self.refs.mkdir(parents=True)
        preferences = preferences_path(self.project)
        preferences.write_text(preferences_text({PREFERENCE: 'rules/refs'}), encoding='utf-8', newline='\n')

    def own(self, mark: str | None=None, link: str='../../docs/own.md#mine') -> str:
        return f"- [Own → Mine]({link}) — why. `reviewed {mark or section_hash(by_anchor(OWN, 'mine'))}`"

    def published(self, anchor: str, drop: str | None=None) -> str:
        link = f'[Doc → {anchor}]({PUBLISHED_PAGES}docs/doc.md#{anchor})'
        if drop is not None:
            return f'- Not read here: {link}' + (f' — {drop}' if drop else '')
        found = by_anchor(DOC, anchor)
        return f"- {link} — why. `reviewed {(section_hash(found) if found else '0' * 12)}`"

    def project_list(self, *entries: str, folder: Path | None=None) -> Path:
        (folder or self.refs).mkdir(parents=True, exist_ok=True)
        return self.write(WORD, *entries, folder=folder or self.refs)

    def test_a_correct_list_in_a_declared_folder_has_no_problem_and_no_warning(self) -> None:
        path = self.project_list(self.own(), self.published('abstract'), self.published('two', drop='not here.'))
        self.assertEqual(list_problems(path, self.root), [])
        self.assertEqual(list_warnings(path, self.root), [])

    def test_a_list_in_a_declared_folder_is_judged(self) -> None:
        found, = list_problems(self.project_list(self.own(mark='0' * 12)), self.root)
        self.assertTrue(found.startswith('line 4: changed since reviewed'), found)

    def test_a_relative_link_leaving_the_project_names_no_file_of_it(self) -> None:
        found, = list_problems(self.project_list(self.own(link='../../../docs/doc.md#one')), self.root)
        self.assertIn('names no Markdown file of this repository', found)

    def test_a_published_address_naming_no_section_of_memar_is_a_problem(self) -> None:
        found, = list_problems(self.project_list(self.published('gone')), self.root)
        self.assertTrue(found.startswith('line 4: '), found)
        self.assertIn("names no section of Memar's checkout", found)

    def test_a_drop_with_no_reason_is_a_problem(self) -> None:
        found, = list_problems(self.project_list(self.published('two', drop='')), self.root)
        self.assertTrue(found.startswith('line 4: '), found)
        self.assertIn('no reason', found)

    def test_a_drop_of_an_every_act_section_is_refused(self) -> None:
        found, = list_problems(self.project_list(self.published('one', drop='not here.')), self.root)
        self.assertTrue(found.startswith('line 4: refused: the every-act sections cannot be dropped'), found)

    def test_a_drop_of_a_passage_no_memar_list_names_drops_nothing(self) -> None:
        found, = list_problems(self.project_list(self.published('abstract', drop='not here.')), self.root)
        self.assertTrue(found.startswith('line 4: drops nothing'), found)

    def test_only_a_drop_that_removes_a_passage_is_counted(self) -> None:
        path = self.project_list(self.published('two', drop='not here.'), self.published('two', drop=''), self.published('one', drop='not here.'))
        self.assertEqual(list_drops(path, self.root), 1)
        self.assertEqual(list_drops(self.place.folder / LIST_NAME.format(word=WORD), self.root), 0)

    def test_a_list_outside_or_below_the_declared_folders_is_not_read_and_is_warned_of(self) -> None:
        for folder in (self.project / 'docs', self.refs / 'below'):
            with self.subTest(folder=folder.name):
                path = self.project_list(self.own(mark='0' * 12), folder=folder)
                self.assertEqual(list_warnings(path, self.root), [OUTSIDE_WARNING])
                self.assertEqual(list_problems(path, self.root), [])
                self.assertEqual(list_drops(path, self.root), 0)

    def test_a_list_of_memar_naming_a_published_address_is_a_problem(self) -> None:
        found, = self.problems(WORD, self.published('two'))
        self.assertIn('a list of Memar links its sections relatively', found)

    def test_checks_summary_counts_the_drops(self) -> None:
        path = self.project_list(self.published('two', drop='not here.'))
        printed = io.StringIO()
        with contextlib.redirect_stdout(printed):
            cmd_check(argparse.Namespace(files=[str(path)], verbose=False, memar_rules=True), self.root)
        last = printed.getvalue().strip().splitlines()[-1]
        self.assertIn('0 problems', last)
        self.assertTrue(last.endswith("1 passage of Memar dropped by this project's lists"), last)

class Real(unittest.TestCase):

    def test_memars_lists_report_no_problem(self) -> None:
        for found in lists([memar_place(ROOT)]):
            with self.subTest(list=found.path.name):
                self.assertEqual(list_problems(found.path, ROOT), [])
                self.assertEqual(list_warnings(found.path, ROOT), [])
if __name__ == '__main__':
    unittest.main(verbosity=2)
