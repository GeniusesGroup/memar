#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for reading a project's `normative_references` preference, in `modules/process/project/services/preferences.py`.

    python modules/process/project/tests/preferences.py

The subject is the reader of the key that declares where a project's own lists
of the rule [Normative References](../../rules/normative_references/normative_references.md)
live (its section Declared places), named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The other keys are pinned by the suites of the services that read them.

Pinned on a scratch project of the suite's own.

What is pinned, and what each pin is for:

  Places    Each folder the key names, comma-separated and relative to the
            project's top folder, is a place of the project, in the order
            named, under the project's folder name, resolving Memar's
            published addresses against the checkout given.
  Unset     An empty or absent key, no preferences file, and no project give
            no place and no problem.
  Refused   A folder that does not exist, the top folder itself, an absolute
            path, and one that leaves the project are each a problem naming
            the file and the value, and give no place; the others still do.
  Template  The file `memar install` writes holds the key, empty, and says
            what it is.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.knowledge.content.services.normative_references import PREFERENCE, Place, normative_reference_places
from modules.process.project.services.preferences import BLOCK_KEY, preferences_path, preferences_text, read_preferences

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.memar = Path(scratch.name).resolve() / 'memar'
        self.memar.mkdir()
        self.project = Path(scratch.name).resolve() / 'orchard'
        for folder in ('rules/refs', 'docs/refs'):
            (self.project / folder).mkdir(parents=True)

    def prefer(self, value: str | None) -> None:
        path = preferences_path(self.project)
        key = '' if value is None else f'  {PREFERENCE}: {value}\n'
        path.write_text(f'name: orchard\n{BLOCK_KEY}:\n  tasks:\n{key}', encoding='utf-8', newline='\n')

    def places(self):
        return normative_reference_places(self.project, self.memar)

class Places(Fixture):

    def test_each_folder_named_is_a_place_in_the_order_named(self) -> None:
        self.prefer('rules/refs, docs/refs')
        places, problems = self.places()
        self.assertEqual(problems, [])
        self.assertEqual(places, [Place('orchard', self.project, self.project / 'rules' / 'refs', self.memar), Place('orchard', self.project, self.project / 'docs' / 'refs', self.memar)])

class Unset(Fixture):

    def test_an_empty_or_absent_key_and_no_file_give_nothing(self) -> None:
        self.assertEqual(self.places(), ([], []))
        for value in (None, ''):
            with self.subTest(value=value):
                self.prefer(value)
                self.assertEqual(self.places(), ([], []))

    def test_no_project_gives_nothing(self) -> None:
        self.assertEqual(normative_reference_places(None, self.memar), ([], []))

class Refused(Fixture):

    def test_a_folder_that_does_not_exist_is_a_problem_and_the_rest_are_read(self) -> None:
        self.prefer('rules/gone, rules/refs')
        places, problems = self.places()
        self.assertEqual([place.folder for place in places], [self.project / 'rules' / 'refs'])
        problem, = problems
        self.assertIn('rules/gone', problem)
        self.assertIn('not a folder', problem)
        self.assertIn(preferences_path(self.project).as_posix(), problem)

    def test_the_top_folder_an_absolute_path_and_one_leaving_the_project_are_problems(self) -> None:
        for value in ('.', './', str(self.project / 'rules' / 'refs'), '../memar', 'rules/../..'):
            with self.subTest(value=value):
                self.prefer(value)
                places, problems = self.places()
                self.assertEqual(places, [])
                self.assertEqual(len(problems), 1, problems)
                self.assertIn(PREFERENCE, problems[0])

class Manifest(Fixture):
    """The `memar:` block is read out of the project's manifest; the manifest's other keys are not Memar's."""

    def write(self, text: str) -> None:
        preferences_path(self.project).write_text(text, encoding='utf-8', newline='\n')

    def test_only_the_block_is_read(self) -> None:
        self.write('"@type": SoftwareSourceCode\ntasks: not-memars\nmemar:\n  # a note\n  tasks: work\n  records: off\nkeywords:\n  - records: x\n')
        self.assertEqual(read_preferences(self.project), {'tasks': 'work', 'records': 'off'})

    def test_a_manifest_without_the_block_or_no_manifest_sets_nothing(self) -> None:
        self.assertEqual(read_preferences(self.project), {})
        self.write('name: orchard\n')
        self.assertEqual(read_preferences(self.project), {})

    def test_the_text_written_for_values_reads_back_as_them(self) -> None:
        values = {'tasks': 'work/tasks', PREFERENCE: 'rules/refs, docs/refs'}
        self.write(preferences_text(values))
        self.assertEqual(read_preferences(self.project), values)
if __name__ == '__main__':
    unittest.main(verbosity=2)
