#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content edit` in `modules-plugable/computer/filesystem/services/content_edit.py`.

    python modules-plugable/computer/filesystem/tests/content_edit.py

The subject is the exact-text replacement, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the file edited and the Memar
root the lock lives under are both inside one, made under the folder
`modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed again.

What is pinned, and what each pin is for:

  EditTakesTheLock    The read, the match, and the write happen under the
                      per-file lock, the lock is gone once the edit ends, a
                      refused edit changes nothing, and the bytes written are
                      the ones the newline flag names.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_lock = plugable_load('computer.filesystem.services.fs_lock')
fs_lock = _m_fs_lock
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_edit = import_module('modules-plugable.computer.filesystem.services.content_edit')

class EditTakesTheLock(unittest.TestCase):
    """The edit verb takes the per-file lock around the read and the write.

    The caller believes the file contains exactly `--old`, and that belief is
    checked against the file as it is at the moment of the write; the lock is
    what keeps the copy read and the bytes written one interval.

    Called in-process rather than through a child, because what is under test is
    which function the verb reaches, and a child would answer only that the
    command line works — with the root it resolves on this machine, not the
    scratch one whose locks are then inspected.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n', encoding='utf-8', newline='\n')
        self.scratch_root = self.root / 'memar'
        self.scratch_root.mkdir()
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.scratch_root)
        patched.start()
        self.addCleanup(patched.stop)

    def args(self, **overrides) -> Namespace:
        defaults = dict(file=str(self.target), old=None, old_file=None, new=None, new_file=None, all=False, newline=None)
        defaults.update(overrides)
        return Namespace(**defaults)

    def held_locks(self) -> list[Path]:
        return list((self.scratch_root / 'temp').rglob('*.lock'))

    def test_an_edit_takes_the_lock_around_the_read_and_the_write(self) -> None:
        taken: list[Path] = []
        saved = fs_lock.edit_task

        def record(target, **keywords):
            taken.append(target)
            return saved(target, **keywords)
        fs_lock.edit_task = record
        self.addCleanup(setattr, fs_lock, 'edit_task', saved)
        content_edit.cmd_edit(self.args(old='# Notes', new='# Renamed'), self.root)
        self.assertEqual(taken, [self.target])
        self.assertEqual(self.target.read_text(encoding='utf-8'), '# Renamed\n')

    def test_an_edit_leaves_the_lock_behind_it(self) -> None:
        content_edit.cmd_edit(self.args(old='# Notes', new='# Renamed'), self.root)
        self.assertEqual(self.held_locks(), [])

    def test_a_refused_edit_leaves_no_lock_and_no_change(self) -> None:
        with self.assertRaises(SystemExit):
            content_edit.cmd_edit(self.args(old='# Absent', new='x'), self.root)
        self.assertEqual(self.held_locks(), [])
        self.assertEqual(self.target.read_text(encoding='utf-8'), '# Notes\n')

    def test_an_edit_with_a_newline_flag_writes_the_line_ending_it_names(self) -> None:
        self.target.write_text('# Notes\n\nBody\n', encoding='utf-8', newline='\n')
        content_edit.cmd_edit(self.args(old='Body', new='Text', newline='crlf'), self.root)
        self.assertEqual(self.target.read_bytes(), b'# Notes\r\n\r\nText\r\n')
if __name__ == '__main__':
    unittest.main(verbosity=2)
