#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for reading a project's `normative_references` preference, in `services/project_preferences.py`.

    python .agents/scripts/services/tests/project_preferences.py

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

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# The scripts folder is two levels up from this suite's folder; running a file
# puts its own folder on the module search path, not its parent's.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch
from services.normative_references import PREFERENCE, Place
from services.project_preferences import PREFERENCES_TEXT, normative_reference_places, preferences_path


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.memar = Path(scratch.name).resolve() / "memar"
        self.memar.mkdir()
        self.project = Path(scratch.name).resolve() / "orchard"
        for folder in ("rules/refs", "docs/refs"):
            (self.project / folder).mkdir(parents=True)

    def prefer(self, value: str | None) -> None:
        path = preferences_path(self.project)
        path.parent.mkdir(parents=True, exist_ok=True)
        key = "" if value is None else f"{PREFERENCE}: {value}\n"
        path.write_text(f"---\nsessions:\n{key}---\n# Preferences\n", encoding="utf-8", newline="\n")

    def places(self):
        return normative_reference_places(self.project, self.memar)


class Places(Fixture):
    def test_each_folder_named_is_a_place_in_the_order_named(self) -> None:
        self.prefer("rules/refs, docs/refs")
        places, problems = self.places()
        self.assertEqual(problems, [])
        self.assertEqual(
            places,
            [
                Place("orchard", self.project, self.project / "rules" / "refs", self.memar),
                Place("orchard", self.project, self.project / "docs" / "refs", self.memar),
            ],
        )


class Unset(Fixture):
    def test_an_empty_or_absent_key_and_no_file_give_nothing(self) -> None:
        self.assertEqual(self.places(), ([], []))
        for value in (None, ""):
            with self.subTest(value=value):
                self.prefer(value)
                self.assertEqual(self.places(), ([], []))

    def test_no_project_gives_nothing(self) -> None:
        self.assertEqual(normative_reference_places(None, self.memar), ([], []))


class Refused(Fixture):
    def test_a_folder_that_does_not_exist_is_a_problem_and_the_rest_are_read(self) -> None:
        self.prefer("rules/gone, rules/refs")
        places, problems = self.places()
        self.assertEqual([place.folder for place in places], [self.project / "rules" / "refs"])
        (problem,) = problems
        self.assertIn("rules/gone", problem)
        self.assertIn("not a folder", problem)
        self.assertIn(preferences_path(self.project).as_posix(), problem)

    def test_the_top_folder_an_absolute_path_and_one_leaving_the_project_are_problems(self) -> None:
        for value in (".", "./", str(self.project / "rules" / "refs"), "../memar", "rules/../.."):
            with self.subTest(value=value):
                self.prefer(value)
                places, problems = self.places()
                self.assertEqual(places, [])
                self.assertEqual(len(problems), 1, problems)
                self.assertIn(PREFERENCE, problems[0])


class Template(unittest.TestCase):
    def test_the_installed_file_holds_the_key_empty_and_says_what_it_is(self) -> None:
        front = PREFERENCES_TEXT.split("---\n")[1]
        self.assertIn(f"\n{PREFERENCE}:\n", "\n" + front)
        self.assertIn(f"`{PREFERENCE}` names the folders", PREFERENCES_TEXT)


if __name__ == "__main__":
    unittest.main(verbosity=2)
