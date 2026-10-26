#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for where a suite writes, in `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py`.

    python modules-plugable/computer/memory/filesystem/tests/fs_test_scratch.py

The subject is the one owner of MEMAR_TEST_SCRATCH, named for the file that
holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside the fallback folder the module itself makes, and
git is asked only whether a path is ignored.

What is pinned, and what each pin is for:

  VariableNamesTheFolder  A set variable naming a folder is that folder; one
                          naming nothing is refused rather than created.
  FallbackIsIgnoredScratch
                          Unset, the folder is temp/test-scratch/ in this
                          checkout — never the OS temporary directory — and git
                          ignores it, so a run leaves nothing git sees.
  RemovedWhole            A suite's folder is removed whole, read-only git
                          objects included; a file held for a moment is waited
                          for, and what still cannot go fails loudly instead
                          of staying behind unseen.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
scratch = _m_fs_test_scratch
import os
import stat
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent
SCRIPTS = REPO / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True

class VariableNamesTheFolder(unittest.TestCase):

    def test_a_folder_the_variable_names_is_used_as_it_is(self) -> None:
        with tempfile.TemporaryDirectory(dir=scratch.suite_scratch()) as named:
            with unittest.mock.patch.dict(os.environ, {scratch.VARIABLE: named}):
                self.assertEqual(scratch.suite_scratch(), Path(named))

    def test_a_variable_naming_nothing_is_refused_not_created(self) -> None:
        with tempfile.TemporaryDirectory(dir=scratch.suite_scratch()) as parent:
            missing = Path(parent) / 'no-such-folder'
            with unittest.mock.patch.dict(os.environ, {scratch.VARIABLE: str(missing)}):
                with self.assertRaises(SystemExit):
                    scratch.suite_scratch()
            self.assertFalse(missing.exists())

class FallbackIsIgnoredScratch(unittest.TestCase):

    def test_unset_it_is_temp_test_scratch_in_this_checkout(self) -> None:
        environment = {key: value for key, value in os.environ.items() if key != scratch.VARIABLE}
        with unittest.mock.patch.dict(os.environ, environment, clear=True):
            folder = scratch.suite_scratch()
        self.assertEqual(folder, CHECKOUT / 'temp' / scratch.FALLBACK_NAME)
        self.assertTrue(folder.is_dir())
        self.assertFalse(folder.resolve().is_relative_to(Path(tempfile.gettempdir()).resolve()))

    def test_git_ignores_the_fallback(self) -> None:
        probe = (Path('temp') / scratch.FALLBACK_NAME / 'probe').as_posix()
        asked = subprocess.run(['git', '-C', str(CHECKOUT), 'check-ignore', '-q', probe], capture_output=True)
        if asked.returncode == 128:
            self.skipTest('this copy of the scripts is not inside a git checkout')
        self.assertEqual(asked.returncode, 0, f"{probe} is not ignored by the checkout's .gitignore")

class RemovedWhole(unittest.TestCase):

    def make_tree(self) -> Path:
        root = Path(tempfile.mkdtemp(dir=scratch.suite_scratch()))
        self.addCleanup(scratch.remove_tree, root)
        objects = root / 'repo.git' / 'objects' / 'ab'
        objects.mkdir(parents=True)
        for name in ('cdef', '0123'):
            (objects / name).write_bytes(b'x')
            os.chmod(objects / name, stat.S_IREAD)
        return root

    def test_read_only_files_are_removed_with_the_rest(self) -> None:
        root = self.make_tree()
        scratch.remove_tree(root)
        self.assertFalse(root.exists())
        scratch.remove_tree(root)

    def test_a_file_held_for_a_moment_is_waited_for(self) -> None:
        root = self.make_tree()
        real = scratch.shutil.rmtree
        refusals = [PermissionError(13, 'held by another process')]

        def held_once(path, **handler):
            if refusals:
                raise refusals.pop()
            real(path, **handler)
        with unittest.mock.patch.object(scratch.shutil, 'rmtree', side_effect=held_once), unittest.mock.patch.object(scratch, 'REMOVE_PAUSE_SECONDS', 0):
            scratch.remove_tree(root)
        self.assertFalse(root.exists())

    def test_what_cannot_go_fails_loudly_rather_than_staying_silently(self) -> None:
        root = self.make_tree()
        refused = PermissionError(13, 'held by another process')
        with unittest.mock.patch.object(scratch.shutil, 'rmtree', side_effect=refused), unittest.mock.patch.object(scratch, 'REMOVE_PAUSE_SECONDS', 0), self.assertRaises(PermissionError):
            scratch.remove_tree(root)
        self.assertTrue(root.exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
