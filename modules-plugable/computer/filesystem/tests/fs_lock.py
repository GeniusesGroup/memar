#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the per-file advisory edit locks in `fs_lock.py`.

    python modules-plugable/computer/filesystem/tests/fs_lock.py

The subject is the per-file lock surface of `fs_lock.py`, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. Target files live in a scratch folder
inside this one and are removed again; lock and intent files live in a
scratch folder passed explicitly - the same explicit-dir shape the module
honors for tests - and are removed again. Default root resolution lives in
`fs_memar.py` on this shelf and is tested beside it in
`filesystem/tests/fs_memar.py`.

What is pinned, and what each pin is for:

  TakeAndRelease     Taking a free per-file lock creates it, and releasing
                     removes the lock and its intent note; one target always
                     maps to one lock, and two targets never share one.
  WaitAndTimeout     A second take while the lock is held waits and then
                     fails instead of taking; after a release the same take
                     succeeds.
  StaleTakeover      A lock older than the stale age is taken over, while a
                     fresh lock is waited out - so a dead session never
                     blocks others forever, and a live one is never robbed.
  IntentRoundTrip    What is written as the intent to change is what is read
                     back: session, file, plan, and the base hash and mtime
                     the re-verify step compares against.
  ChangedBaseDetected  Verifying after acquiring compares the plan-time base
                     against the lock-time file; any move - edited, deleted,
                     or newly appeared - raises instead of applying blind.
  TryLockGoesAway    A take that must not wait answers no while a live holder
                     has the lock, and yes once it is released or its holder
                     is dead.
  OnceADay           The daily guard answers yes to the first claim of a day
                     and no to every later one, and yes again on a new day.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_lock = import_module('modules-plugable.computer.filesystem.services.fs_lock')
fs_lock = _m_fs_lock
import contextlib
import hashlib
import io
import json
import os
import sys
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = TESTS.parents[3]
SCRIPTS = REPO / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True

class Fixture(unittest.TestCase):
    """A target file inside this folder and an explicit lock dir for tests."""

    def setUp(self) -> None:
        self.targets = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.targets.cleanup)
        self.locks = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.locks.cleanup)
        self.lock_dir = Path(self.locks.name)
        self.target = Path(self.targets.name) / 'notes.md'
        self.target.write_text('# Notes\n', encoding='utf-8', newline='\n')

    def lock_for(self, target: Path | None=None) -> Path:
        return fs_lock.edit_lock_path(self.target if target is None else target, self.lock_dir)

    def take(self, lock: Path, **kwargs) -> None:
        kwargs.setdefault('wait_seconds', 5)
        kwargs.setdefault('stale_seconds', 60)
        kwargs.setdefault('poll_seconds', 0.05)
        fs_lock.take_file_lock(lock, **kwargs)

class TakeAndRelease(Fixture):

    def test_take_creates_the_lock_file(self) -> None:
        lock = self.lock_for()
        self.assertFalse(lock.exists())
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        self.assertTrue(lock.is_file())

    def test_release_removes_the_lock_and_its_intent_note(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        base = fs_lock.file_snapshot(self.target)
        intent = fs_lock.edit_intent_path(lock)
        fs_lock.write_intent(intent, task_id='s-1', target=self.target, plan_summary='add a section', base=base)
        self.assertTrue(intent.is_file())
        fs_lock.release_file_lock(lock)
        self.assertFalse(lock.exists())
        self.assertFalse(intent.exists())

    def test_release_of_a_free_lock_is_silent(self) -> None:
        fs_lock.release_file_lock(self.lock_for())

    def test_one_target_maps_to_one_lock(self) -> None:
        self.assertEqual(self.lock_for(), self.lock_for())
        self.assertEqual(self.lock_for(), fs_lock.edit_lock_path(self.target, self.lock_dir))

    def test_two_targets_never_share_a_lock(self) -> None:
        other = Path(self.targets.name) / 'other.md'
        other.write_text('# Other\n', encoding='utf-8', newline='\n')
        self.assertNotEqual(self.lock_for(), self.lock_for(other))

class WaitAndTimeout(Fixture):

    def test_a_second_take_while_held_fails_rather_than_taking(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        with self.assertRaises(SystemExit):
            fs_lock.take_file_lock(lock, wait_seconds=0.3, stale_seconds=60, poll_seconds=0.05)
        self.assertTrue(lock.is_file())

    def test_a_zero_wait_fails_immediately_while_held(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        started = time.monotonic()
        with self.assertRaises(SystemExit):
            fs_lock.take_file_lock(lock, wait_seconds=0, stale_seconds=60, poll_seconds=0.05)
        self.assertLess(time.monotonic() - started, 5)

    def test_take_after_release_succeeds(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        fs_lock.release_file_lock(lock)
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        self.assertTrue(lock.is_file())

class StaleTakeover(Fixture):

    def backdate(self, lock: Path, seconds: float) -> None:
        old = time.time() - seconds
        os.utime(lock, (old, old))

    def test_a_stale_lock_is_taken_over(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        self.backdate(lock, 1000)
        fs_lock.take_file_lock(lock, wait_seconds=5, stale_seconds=1, poll_seconds=0.05)
        self.addCleanup(fs_lock.release_file_lock, lock)
        self.assertTrue(lock.is_file())
        self.assertLess(time.time() - lock.stat().st_mtime, 60)

    def test_a_fresh_lock_is_waited_out_not_taken(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        before = lock.stat().st_mtime
        with self.assertRaises(SystemExit):
            fs_lock.take_file_lock(lock, wait_seconds=0.3, stale_seconds=3600, poll_seconds=0.05)
        self.assertEqual(lock.stat().st_mtime, before)

class IntentRoundTrip(Fixture):

    def test_what_is_written_is_what_is_read(self) -> None:
        lock = self.lock_for()
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        base = fs_lock.file_snapshot(self.target)
        intent = fs_lock.edit_intent_path(lock)
        fs_lock.write_intent(intent, task_id='session-7', target=self.target, plan_summary='add a section on locks', base=base)
        found = fs_lock.read_intent(intent)
        self.assertEqual(found['task_id'], 'session-7')
        self.assertEqual(found['file'], str(self.target.absolute()))
        self.assertEqual(found['plan_summary'], 'add a section on locks')
        self.assertEqual(found['base_hash'], base['hash'])
        self.assertEqual(found['base_mtime_ns'], base['mtime_ns'])
        self.assertIn('created_at', found)

    def test_the_intent_lives_beside_the_lock(self) -> None:
        lock = self.lock_for()
        intent = fs_lock.edit_intent_path(lock)
        self.assertEqual(intent.parent, lock.parent)
        self.assertTrue(intent.name.startswith(lock.name))

class ChangedBaseDetected(Fixture):

    def test_an_unchanged_file_verifies_clean(self) -> None:
        base = fs_lock.file_snapshot(self.target)
        fs_lock.verify_base_unchanged(self.target, base)

    def test_edited_content_is_detected(self) -> None:
        base = fs_lock.file_snapshot(self.target)
        with self.target.open('a', encoding='utf-8', newline='\n') as handle:
            handle.write('\nA new section.\n')
        with self.assertRaises(fs_lock.BaseChangedError):
            fs_lock.verify_base_unchanged(self.target, base)

    def test_a_deleted_file_is_detected(self) -> None:
        base = fs_lock.file_snapshot(self.target)
        self.target.unlink()
        with self.assertRaises(fs_lock.BaseChangedError):
            fs_lock.verify_base_unchanged(self.target, base)

    def test_a_newly_appearing_file_is_detected(self) -> None:
        missing = Path(self.targets.name) / 'new.md'
        base = fs_lock.file_snapshot(missing)
        self.assertFalse(base['exists'])
        missing.write_text('# New\n', encoding='utf-8', newline='\n')
        with self.assertRaises(fs_lock.BaseChangedError):
            fs_lock.verify_base_unchanged(missing, base)

    def test_a_missing_file_that_stays_missing_verifies_clean(self) -> None:
        missing = Path(self.targets.name) / 'new.md'
        fs_lock.verify_base_unchanged(missing, fs_lock.file_snapshot(missing))

    def test_reverify_after_acquire_in_order(self) -> None:
        base = fs_lock.file_snapshot(self.target)
        lock = self.lock_for()
        self.take(lock)
        self.addCleanup(fs_lock.release_file_lock, lock)
        with self.target.open('a', encoding='utf-8', newline='\n') as handle:
            handle.write('\nA rival session wrote first.\n')
        with self.assertRaises(fs_lock.BaseChangedError):
            fs_lock.verify_base_unchanged(self.target, base)

    def test_edit_session_yields_then_releases(self) -> None:
        lock = self.lock_for()
        with fs_lock.edit_session(self.target, 'session-7', 'add a section', lock_dir=self.lock_dir, wait_seconds=5, stale_seconds=60, poll_seconds=0.05):
            self.assertTrue(lock.is_file())
        self.assertFalse(lock.exists())

    def test_edit_session_refuses_a_moved_base_without_yielding(self) -> None:
        lock = self.lock_for()

        def moved(target: Path, base: dict) -> None:
            raise fs_lock.BaseChangedError('moved under the plan')
        entered = []
        with unittest.mock.patch.object(fs_lock, 'verify_base_unchanged', moved):
            with self.assertRaises(fs_lock.BaseChangedError):
                with fs_lock.edit_session(self.target, 'session-7', 'add a section', lock_dir=self.lock_dir, wait_seconds=5, stale_seconds=60, poll_seconds=0.05):
                    entered.append(True)
        self.assertEqual(entered, [])
        self.assertFalse(lock.exists())

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
