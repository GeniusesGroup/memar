#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the claim type in `modules/management/task/primitive/claim.py`.

    python modules/management/task/tests/primitive_claim.py

The subject is the claim an agent leaves in a session's folder while it holds
the task: the file's name, the name of the guard held while a stale claim is
replaced, how long a claim lives, and what the file says. Named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)):
the services that take, keep, lay out and describe a claim call the type.

Writes only in a scratch folder this suite makes and removes.

What is pinned, and what each pin is for:

  Names      The claim file and its takeover guard are two names, held with
             the other names a session folder's top may hold.
  Staleness  A claim is fresh for a day and then a dead agent's; the hours a
             help says come from the same number.
  Content    The file says when it was taken, by which host and process.
  Folder     A folder's claim is found by the type, fresh or not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.management.task.primitive.claim import Claim

class Names(unittest.TestCase):

    def test_the_claim_file_and_its_takeover_guard(self) -> None:
        self.assertEqual(Claim.NAME, 'claim')
        self.assertEqual(Claim.TAKEOVER_NAME, 'claim.takeover')
        self.assertEqual(Claim.NAMES, (Claim.NAME, Claim.TAKEOVER_NAME))

    def test_the_paths_are_in_the_folder_given(self) -> None:
        folder = Path('/work/20261013-T161701Z-2296')
        claim = Claim(folder)
        self.assertEqual(claim.path, folder / Claim.NAME)
        self.assertEqual(claim.takeover_path, folder / Claim.TAKEOVER_NAME)

class Staleness(unittest.TestCase):

    def test_a_claim_lives_a_day(self) -> None:
        self.assertEqual(Claim.STALE_SECONDS, 24 * 60 * 60)
        self.assertEqual(Claim.stale_hours(), 24)

    def test_a_folder_without_a_claim_holds_no_fresh_one(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            self.assertFalse(Claim(Path(scratch)).is_fresh())

    def test_a_claim_made_now_is_fresh_and_one_past_the_day_is_not(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            claim = Claim(Path(scratch))
            claim.path.write_text('claimed: now\n', encoding='utf-8')
            self.assertTrue(claim.is_fresh())
            old = time.time() - Claim.STALE_SECONDS - 60
            os.utime(claim.path, (old, old))
            self.assertFalse(claim.is_fresh())

class Content(unittest.TestCase):

    def test_the_file_says_when_where_and_by_which_process(self) -> None:
        text = Claim.body('2026-10-16T09:00:00Z', 'a-host', 4242)
        self.assertEqual(text, 'claimed: 2026-10-16T09:00:00Z\nhost: a-host\npid: 4242\n')

class Folder(unittest.TestCase):

    def test_the_type_knows_whether_the_folder_holds_a_claim_at_all(self) -> None:
        with tempfile.TemporaryDirectory() as scratch:
            claim = Claim(Path(scratch))
            self.assertFalse(claim.exists())
            claim.path.write_text('claimed: now\n', encoding='utf-8')
            self.assertTrue(claim.exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
