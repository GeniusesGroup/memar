#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the lock of one install at a time, in `bundles/memar/services/install/services/lock.py`.

    python bundles/memar/services/install/tests/lock.py

The take itself is pinned beside the file that writes it, `bundles/memar_fs/tests/fs_lock.py`;
what is pinned here is what the install lock is called, where it lies, and that a held one is waited for and then refused.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_lock = import_module('bundles.memar.services.install.services.lock')
_m_fs_lock = import_module('bundles.memar_fs.services.fs_lock')
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = next(p for p in TESTS.parents if p.name == 'bundles').parent
sys.path.insert(0, str(REPO / 'bundles' / 'memar'))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True

class InstallLock(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)

    def test_the_lock_lies_beside_the_folder_it_guards(self) -> None:
        target = self.root / 'Memar'
        self.assertEqual(_m_lock.lock_path(target), self.root / _m_lock.INSTALL_LOCK_NAME)

    def test_a_free_lock_is_taken_and_released(self) -> None:
        lock = _m_lock.lock_path(self.root / 'Memar')
        self.assertEqual(_m_lock.take_lock(lock), 0)
        self.assertTrue(lock.exists())
        _m_fs_lock.release_lock(lock)
        self.assertFalse(lock.exists())

    def test_a_held_lock_is_waited_for_by_the_shared_take_with_the_install_deadline(self) -> None:
        lock = _m_lock.lock_path(self.root / 'Memar')
        with unittest.mock.patch.object(_m_fs_lock, 'take_advisory_lock') as take:
            self.assertEqual(_m_lock.take_lock(lock), 0)
        arguments = take.call_args
        self.assertEqual(arguments.args, (lock,))
        self.assertEqual(arguments.kwargs['wait_seconds'], _m_lock.LOCK_WAIT_SECONDS)
        self.assertIn(str(lock), arguments.kwargs['waiting_message'])
        self.assertIn(str(lock), arguments.kwargs['timeout_message'])

    def test_a_held_lock_is_refused_after_the_wait_naming_the_file(self) -> None:
        lock = _m_lock.lock_path(self.root / 'Memar')
        self.assertEqual(_m_lock.take_lock(lock), 0)
        self.addCleanup(_m_fs_lock.release_lock, lock)
        with unittest.mock.patch.object(_m_lock, 'LOCK_WAIT_SECONDS', 600), unittest.mock.patch.object(_m_fs_lock.time, 'monotonic', side_effect=[0, 1000, 1000]), unittest.mock.patch.object(_m_fs_lock.time, 'sleep'), contextlib.redirect_stderr(io.StringIO()) as shown:
            with self.assertRaises(SystemExit) as refused:
                _m_lock.take_lock(lock)
        self.assertIn(str(lock), str(refused.exception.code))
        self.assertIn('another Memar install is running', shown.getvalue())
if __name__ == '__main__':
    unittest.main(verbosity=2)
