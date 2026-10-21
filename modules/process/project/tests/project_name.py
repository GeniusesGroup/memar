#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the project name type in `modules/process/project/primitive/project_name.py`.

    python modules/process/project/tests/project_name.py

The subject is a project given by its name: the flag that carries it, and what
a value must be to be taken as a name. A name is never a path: a value written
as a path is refused with the flag that takes a path, not looked up. Named for
the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).

Nothing here writes.

What is pinned, and what each pin is for:

  Flag      The flag, its metavar and the attribute a parser gives it.
  Checking  A word is taken as a name; an empty value or one written as a path
            is refused, the refusal naming the flag that fits.
  Words     What a help or an error says of the two flags together comes from
            the two types.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.process.project.primitive.project_name import ProjectName
from modules.process.project.primitive.project_path import ProjectPath

class Flag(unittest.TestCase):

    def test_the_flag_the_metavar_and_the_attribute(self) -> None:
        self.assertEqual((ProjectName.FLAG, ProjectName.METAVAR, ProjectName.DEST), ('--project', 'NAME', 'project'))

    def test_the_two_flags_differ_and_neither_prefixes_the_others_attribute(self) -> None:
        self.assertNotEqual(ProjectName.FLAG, ProjectPath.FLAG)
        self.assertNotEqual(ProjectName.DEST, ProjectPath.DEST)

class Checking(unittest.TestCase):

    def refused(self, value: str) -> str:
        with self.assertRaises(SystemExit) as refusal:
            ProjectName.checked(value)
        return str(refusal.exception.code)

    def test_a_word_is_taken_as_a_name_stripped(self) -> None:
        for value, expected in (('memar', 'memar'), ('  organization ', 'organization')):
            with self.subTest(value=value):
                checked = ProjectName.checked(value)
                self.assertEqual(checked, expected)
                self.assertIsInstance(checked, ProjectName)

    def test_an_empty_value_is_refused_naming_the_flag(self) -> None:
        for value in ('', '   '):
            with self.subTest(value=value):
                self.assertIn(ProjectName.FLAG, self.refused(value))

    def test_a_value_written_as_a_path_is_refused_with_the_flag_that_takes_a_path(self) -> None:
        for value in ('/work/app', 'work\\app', './app', '~/app'):
            with self.subTest(value=value):
                message = self.refused(value)
                self.assertIn('looks like a path', message)
                self.assertIn(ProjectPath.FLAG, message)

class Words(unittest.TestCase):

    def test_either_flag_with_its_metavar(self) -> None:
        self.assertEqual(ProjectName.either_words(), '--project NAME or --project-path PATH')
if __name__ == '__main__':
    unittest.main(verbosity=2)
