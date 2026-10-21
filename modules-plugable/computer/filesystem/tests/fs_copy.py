#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for whether a copy still matches, in `modules-plugable/computer/filesystem/services/fs_copy.py`.

    python modules-plugable/computer/filesystem/tests/fs_copy.py

The subject is the tree comparison of `modules-plugable/computer/filesystem/services/fs_copy.py`, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Both trees are written into a scratch folder and removed with it.

What is pinned, and what each pin is for:

  CopyMatches        A tree copied with the same ignore rule matches, and what
                     the rule leaves out is left out of the comparison on both
                     sides.
  CopyDiffers        A file changed, added, or gone on either side is a
                     difference, including a change that keeps the size.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_copy = import_module('modules-plugable.computer.filesystem.services.fs_copy')
differs = _m_fs_copy.differs
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = TESTS.parents[3]
SCRIPTS = REPO / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True
IGNORE = shutil.ignore_patterns('*.pyc', 'node_modules')

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        root = Path(scratch.name)
        self.source = root / 'source'
        (self.source / 'part').mkdir(parents=True)
        (self.source / 'a.md').write_text('alpha\n', encoding='utf-8')
        (self.source / 'part' / 'b.md').write_text('beta\n', encoding='utf-8')
        self.dest = root / 'dest'
        shutil.copytree(self.source, self.dest, ignore=IGNORE)

class CopyMatches(Fixture):

    def test_a_copy_matches_its_source(self) -> None:
        self.assertFalse(differs(self.source, self.dest, IGNORE))

    def test_what_the_rule_leaves_out_is_not_compared(self) -> None:
        (self.source / 'node_modules').mkdir()
        (self.source / 'node_modules' / 'dep.js').write_text('dev\n', encoding='utf-8')
        (self.dest / 'part' / 'x.pyc').write_bytes(b'\x00')
        self.assertFalse(differs(self.source, self.dest, IGNORE))

class CopyDiffers(Fixture):

    def test_a_change_an_addition_or_a_removal_differs(self) -> None:
        cases = (lambda: (self.dest / 'a.md').write_text('alphA\n', encoding='utf-8'), lambda: (self.dest / 'extra.md').write_text('mine\n', encoding='utf-8'), lambda: (self.dest / 'part' / 'b.md').unlink())
        for change in cases:
            with self.subTest(change=change):
                shutil.rmtree(self.dest)
                shutil.copytree(self.source, self.dest, ignore=IGNORE)
                change()
                self.assertTrue(differs(self.source, self.dest, IGNORE))
if __name__ == '__main__':
    unittest.main(verbosity=2)
