#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
BUDGET_SECONDS = 60
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_fs_lock = import_module('bundles.memar_fs.services.fs_lock')
fs_lock = _m_fs_lock
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = next(p for p in TESTS.parents if p.name == 'bundles').parent
SCRIPTS = REPO / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.locks = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.locks.cleanup)
        self.lock_dir = Path(self.locks.name)

class TryLockGoesAway(Fixture):

    def test_a_held_lock_is_not_taken_and_a_released_one_is(self) -> None:
        lock = self.lock_dir / 'job.lock'
        self.assertTrue(fs_lock.try_lock(lock, 60))
        self.assertFalse(fs_lock.try_lock(lock, 60))
        fs_lock.release_lock(lock)
        self.assertTrue(fs_lock.try_lock(lock, 60))

    def test_a_dead_holders_lock_is_taken_over(self) -> None:
        lock = self.lock_dir / 'job.lock'
        lock.write_text('', encoding='utf-8')
        old = time.time() - 120
        os.utime(lock, (old, old))
        self.assertTrue(fs_lock.try_lock(lock, 60))

class AdvisoryTake(Fixture):

    def test_a_free_lock_is_taken_and_a_held_one_ends_the_run_after_the_wait(self) -> None:
        lock = self.lock_dir / 'job.lock'
        fs_lock.take_advisory_lock(lock, wait_seconds=5, stale_seconds=60, poll_seconds=0.05, waiting_message='', timeout_message='held')
        self.assertTrue(lock.exists())
        with self.assertRaises(SystemExit):
            fs_lock.take_advisory_lock(lock, wait_seconds=0.2, stale_seconds=60, poll_seconds=0.05, waiting_message='', timeout_message='held')
        fs_lock.release_lock(lock)
        self.assertFalse(lock.exists())

class OnceADay(Fixture):

    def test_the_first_claim_of_the_day_is_the_only_one(self) -> None:
        marker = self.lock_dir / 'daily' / 'job.daily'
        self.assertTrue(fs_lock.claim_today(marker))
        self.assertFalse(fs_lock.claim_today(marker))
        self.assertFalse(fs_lock.claim_today(marker))

    def test_a_marker_from_another_day_is_claimed_again(self) -> None:
        marker = self.lock_dir / 'job.daily'
        marker.write_text('2000-01-01\n', encoding='utf-8')
        self.assertTrue(fs_lock.claim_today(marker))
        self.assertFalse(fs_lock.claim_today(marker))
if __name__ == '__main__':
    unittest.main(verbosity=2)
