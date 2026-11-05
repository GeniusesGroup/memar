#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import hashlib
import json
import os
import sys
import threading
import time
import unittest
from importlib import import_module
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchFolder, bundle


def text_errors():
    return import_module('modules.knowledge.text.errors.edit')


class Limits:

    def __init__(self, wait: float = 0.3, stale: float = 60.0, poll: float = 0.05) -> None:
        self.wait = wait
        self.stale = stale
        self.poll = poll

    def get_wait_seconds(self) -> float:
        return self.wait

    def get_stale_seconds(self) -> float:
        return self.stale

    def get_poll_seconds(self) -> float:
        return self.poll


class Fixture(ScratchFolder):

    def setUp(self) -> None:
        super().setUp()
        self.target = self.root / 'notes.md'
        self.target.write_bytes(b'one\n')
        self.locks = self.root / 'locks'
        self.lock = bundle('services.text_edit_lock').Text_Edit_Lock_Held(self.locks)

    def store(self, path: Path | None = None):
        return bundle('services.text_edit_store').Text_Edit_Store_Held(path or self.target)

    def lock_files(self) -> list[Path]:
        return sorted(self.locks.glob('*.lock')) if self.locks.is_dir() else []

    def intent_files(self) -> list[Path]:
        return sorted(self.locks.glob('*.intent.json')) if self.locks.is_dir() else []


class TakeAndRelease(Fixture):

    def test_taking_a_free_lock_makes_it_and_releasing_removes_it_and_its_note(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'replace 3 chars', Limits())
        self.assertEqual(len(self.lock_files()), 1)
        self.assertEqual(len(self.intent_files()), 1)
        held.release()
        self.assertEqual(self.lock_files(), [])
        self.assertEqual(self.intent_files(), [])

    def test_releasing_answers_no_error_even_when_the_lock_is_already_gone(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        for leftover in self.lock_files() + self.intent_files():
            leftover.unlink()
        held.release()

    def test_one_text_has_one_lock_and_two_texts_never_share_one(self) -> None:
        other = self.root / 'other.md'
        other.write_bytes(b'x\n')
        first = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        second = self.lock.take(self.store(other), 'writer-2', 'y', Limits())
        self.assertEqual(len(self.lock_files()), 2)
        first.release()
        second.release()

    def test_a_lock_is_taken_again_after_it_is_released(self) -> None:
        self.lock.take(self.store(), 'writer-1', 'x', Limits()).release()
        self.lock.take(self.store(), 'writer-2', 'y', Limits()).release()


class IntentNote(Fixture):

    def test_the_note_records_the_target_the_writer_the_summary_and_the_base(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'replace 3 chars with 4', Limits())
        note = json.loads(self.intent_files()[0].read_text(encoding='utf-8'))
        values = list(note.values())
        stat = self.target.stat()
        self.assertTrue(any(str(self.target.name) in str(value) for value in values))
        self.assertIn('writer-1', values)
        self.assertIn('replace 3 chars with 4', values)
        self.assertIn(hashlib.sha256(b'one\n').hexdigest(), values)
        self.assertIn(stat.st_mtime_ns, values)
        self.assertIn(stat.st_size, values)
        self.assertTrue(any(isinstance(value, float) and abs(value - time.time()) < 60 for value in values))
        held.release()


class LockedWhileHeld(Fixture):

    def test_a_live_holder_past_the_wait_is_a_failure_and_its_lock_is_kept(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        with self.assertRaises(text_errors().Text_Error_Edit_Locked) as failed:
            self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=0.2))
        self.assertNotIsInstance(failed.exception, text_errors().Text_Error_Edit_Refusal)
        self.assertEqual(len(self.lock_files()), 1)
        held.release()
        self.assertEqual(self.lock_files(), [])

    def test_a_zero_wait_fails_at_once(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        began = time.monotonic()
        with self.assertRaises(text_errors().Text_Error_Edit_Locked):
            self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=0.0))
        self.assertLess(time.monotonic() - began, 5)
        held.release()

    def test_a_lock_older_than_the_stale_limit_is_a_dead_holders_and_is_taken_over(self) -> None:
        self.lock.take(self.store(), 'dead-writer', 'x', Limits())
        old = time.time() - 3600
        for lock_file in self.lock_files():
            os.utime(lock_file, (old, old))
        taken = self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=0.2, stale=10.0))
        taken.release()
        self.assertEqual(self.lock_files(), [])

    def test_a_fresh_lock_is_waited_out_and_not_taken(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        with self.assertRaises(text_errors().Text_Error_Edit_Locked):
            self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=0.2, stale=3600.0))
        held.release()

    def test_a_waiter_takes_the_lock_once_the_holder_releases_it(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        outcome: dict = {}

        def waiter() -> None:
            try:
                outcome['held'] = self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=10.0))
            except BaseException as error:
                outcome['error'] = error
        worker = threading.Thread(target=waiter)
        worker.start()
        time.sleep(0.4)
        self.assertTrue(worker.is_alive())
        held.release()
        worker.join(30)
        self.assertNotIn('error', outcome)
        outcome['held'].release()


class ChangedWhileWaiting(Fixture):

    def test_a_text_changed_while_the_lock_was_waited_for_ends_the_take_and_releases_nothing_held(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        outcome: dict = {}

        def waiter() -> None:
            try:
                outcome['held'] = self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=10.0))
            except BaseException as error:
                outcome['error'] = error
        worker = threading.Thread(target=waiter)
        worker.start()
        time.sleep(0.4)
        self.target.write_bytes(b'moved under the plan\n')
        held.release()
        worker.join(30)
        self.assertIsInstance(outcome.get('error'), text_errors().Text_Error_Edit_ChangedWhileWaiting)
        self.assertNotIsInstance(outcome['error'], text_errors().Text_Error_Edit_Refusal)
        self.assertEqual(self.lock_files(), [])
        self.assertEqual(self.intent_files(), [])

    def test_a_text_that_appeared_while_waiting_counts_as_changed(self) -> None:
        self.target.unlink()
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        outcome: dict = {}

        def waiter() -> None:
            try:
                outcome['held'] = self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=10.0))
            except BaseException as error:
                outcome['error'] = error
        worker = threading.Thread(target=waiter)
        worker.start()
        time.sleep(0.4)
        self.target.write_bytes(b'appeared\n')
        held.release()
        worker.join(30)
        self.assertIsInstance(outcome.get('error'), text_errors().Text_Error_Edit_ChangedWhileWaiting)

    def test_a_text_that_disappeared_while_waiting_counts_as_changed(self) -> None:
        held = self.lock.take(self.store(), 'writer-1', 'x', Limits())
        outcome: dict = {}

        def waiter() -> None:
            try:
                outcome['held'] = self.lock.take(self.store(), 'writer-2', 'y', Limits(wait=10.0))
            except BaseException as error:
                outcome['error'] = error
        worker = threading.Thread(target=waiter)
        worker.start()
        time.sleep(0.4)
        self.target.unlink()
        held.release()
        worker.join(30)
        self.assertIsInstance(outcome.get('error'), text_errors().Text_Error_Edit_ChangedWhileWaiting)


class LockUnwritable(Fixture):

    def test_a_lock_that_cannot_be_made_is_a_failure_and_not_an_operating_system_error(self) -> None:
        blocker = self.root / 'blocker'
        blocker.write_bytes(b'a file where the lock folder should be\n')
        lock = bundle('services.text_edit_lock').Text_Edit_Lock_Held(blocker / 'locks')
        with self.assertRaises(text_errors().Text_Error_Edit_LockUnwritable) as failed:
            lock.take(self.store(), 'writer-1', 'x', Limits())
        self.assertNotIsInstance(failed.exception, text_errors().Text_Error_Edit_Refusal)
        self.assertNotIsInstance(failed.exception, OSError)


if __name__ == '__main__':
    unittest.main(verbosity=2)
