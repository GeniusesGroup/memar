#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the project path type in `modules/process/project/primitive/project_path.py`.

    python modules/process/project/tests/project_path.py

The subject is a project given by its folder: the flag that carries it, how a
text is told to be written as a path, and what a value must be to be taken as
one. A path is never a name: a word that is not a folder is refused, not looked
up. Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).

Writes only in a scratch folder this suite makes and removes.

What is pinned, and what each pin is for:

  Flag      The flag, its metavar and the attribute a parser gives it.
  Written   What a text looks like when it is written as a path.
  Checking  An existing folder is taken as given; an empty value or a
            non-folder is refused, the refusal naming the flag.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch
from modules.process.project.primitive.project_path import ProjectPath


class Flag(unittest.TestCase):
    def test_the_flag_the_metavar_and_the_attribute(self) -> None:
        self.assertEqual((ProjectPath.FLAG, ProjectPath.METAVAR, ProjectPath.DEST), ("--project-path", "PATH", "project_path"))

    def test_the_attribute_is_what_a_parser_gives_the_flag(self) -> None:
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument(ProjectPath.FLAG, metavar=ProjectPath.METAVAR, default=None)
        self.assertTrue(hasattr(parser.parse_args([]), ProjectPath.DEST))


class Written(unittest.TestCase):
    def test_a_text_written_as_a_path(self) -> None:
        for text in ("/work/app", "C:\\work\\app","work/app", "work\\app", "./app", "../app", "~/app", ".app"):
            with self.subTest(text=text):
                self.assertTrue(ProjectPath.written_like(text))

    def test_a_plain_word_is_not(self) -> None:
        for text in ("memar", "organization", "app-2"):
            with self.subTest(text=text):
                self.assertFalse(ProjectPath.written_like(text))


class Checking(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.base = Path(self.scratch.name)

    def refused(self, value: object, **named: str) -> str:
        with self.assertRaises(SystemExit) as refusal:
            ProjectPath.checked(value, **named)
        return str(refusal.exception.code)

    def test_an_existing_folder_is_taken_as_given(self) -> None:
        folder = self.base / "app"
        folder.mkdir()
        self.assertEqual(ProjectPath.checked(str(folder)).folder, folder.resolve())
        self.assertEqual(ProjectPath.checked(folder).folder, folder.resolve())

    def test_an_empty_value_is_refused_naming_the_flag(self) -> None:
        for value in ("", "   "):
            with self.subTest(value=value):
                self.assertIn(ProjectPath.FLAG, self.refused(value))

    def test_a_value_that_is_not_a_folder_is_refused_and_a_hint_is_added(self) -> None:
        missing = str(self.base / "nope")
        self.assertIn("is not a folder", self.refused(missing))
        self.assertTrue(self.refused("nope", hint="; try the other flag").endswith("; try the other flag"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
