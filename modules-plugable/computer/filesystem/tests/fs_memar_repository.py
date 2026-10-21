#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what a Memar repository is, in `machine/fs_memar_repository.py`.

    python .agents/scripts/machine/tests/fs_memar_repository.py

The subject is the one definition of a Memar repository, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Every repository here is made in a scratch folder under the one
`machine/fs_test_scratch.py` names, and removed with it.

What is pinned, and what each pin is for:

  EnclosingRepository  A path inside a Memar repository resolves to its nearest
                       ancestor repository, or to None outside one; the caller
                       errors rather than guessing.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar_repository as memar_repository


class EnclosingRepository(unittest.TestCase):
    """A path inside a repository resolves inward; outside resolves to None."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        # A walk past the scratch can reach the real repository (the session
        # folder the variable may point at sits inside this checkout), so
        # isolated to the scratch, outside resolves None wherever it sits.
        saved = memar_repository.is_memar_repository
        root = self.root.resolve()

        def isolated(path: Path) -> bool:
            try:
                Path(path).resolve().relative_to(root)
            except ValueError:
                return False
            return saved(path)

        memar_repository.is_memar_repository = isolated
        self.addCleanup(setattr, memar_repository, "is_memar_repository", saved)

    def make_repo(self, where: Path) -> Path:
        where.mkdir(parents=True, exist_ok=True)
        (where / "README.md").write_text("# Memar\n", encoding="utf-8")
        (where / "docs").mkdir(exist_ok=True)
        skill = where / ".agents" / "skills" / "memar" / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("# Memar\n", encoding="utf-8")
        return where

    def test_a_file_inside_returns_the_repository(self):
        repo = self.make_repo(self.root / "Memar")
        inner = repo / "docs" / "cognition.md"
        inner.write_text("# Cognition\n", encoding="utf-8")
        self.assertEqual(memar_repository.enclosing_repository(inner), repo)

    def test_a_directory_inside_returns_the_repository(self):
        repo = self.make_repo(self.root / "Memar")
        self.assertEqual(
            memar_repository.enclosing_repository(repo / "docs"), repo
        )

    def test_the_repository_root_returns_itself(self):
        repo = self.make_repo(self.root / "Memar")
        self.assertEqual(memar_repository.enclosing_repository(repo), repo)

    def test_outside_any_repository_returns_none(self):
        plain = self.root / "plain"
        plain.mkdir()
        target = plain / "notes.md"
        target.write_text("# Notes\n", encoding="utf-8")
        self.assertIsNone(memar_repository.enclosing_repository(target))

    def test_a_nested_repository_resolves_to_the_inner_one(self):
        outer = self.make_repo(self.root / "outer")
        inner = self.make_repo(outer / "inner")
        leaf = inner / "docs" / "leaf.md"
        leaf.write_text("# Leaf\n", encoding="utf-8")
        self.assertEqual(memar_repository.enclosing_repository(leaf), inner)

    def test_a_folder_missing_the_skill_is_not_a_repository(self):
        partial = self.root / "partial"
        partial.mkdir()
        (partial / "README.md").write_text("# Memar\n", encoding="utf-8")
        (partial / "docs").mkdir()
        target = partial / "docs" / "note.md"
        target.write_text("# Note\n", encoding="utf-8")
        self.assertIsNone(memar_repository.enclosing_repository(target))


if __name__ == "__main__":
    unittest.main(verbosity=2)
