#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the Status type in `services/status.py`.

    python .agents/scripts/services/tests/status.py

The subject is the one vocabulary of Status every Memar document and record
draws on, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here reads or writes a file.

What is pinned, and what each pin is for:

  Values         The type holds the eleven values of the vocabulary,
                 each with its meaning, the kinds that may use it, and what is
                 safe to depend on; a word is read in any case, and a word that
                 is no value is None, never a guess.
  Kinds          A kind's values are those that list it, in table order; a
                 session plan may be Queued, Active, Blocked or Complete, and a
                 session report Active, Blocked or Complete.
  ReportEnding   Each value a session report may state says how a run that
                 stated it ended; no other value does.
  Listing        The words of a kind as a sentence, so help and messages obtain
                 them from the type.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# The scripts folder is two levels up from this suite's folder; running a file
# puts its own folder on the module search path, not its parent's.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from services.status import Kind, Status


class Values(unittest.TestCase):
    def test_the_type_holds_the_eleven_values_in_order(self) -> None:
        self.assertEqual(
            [status.word for status in Status],
            ["Draft", "Proposed", "Final", "Superseded", "Rejected", "Queued", "Active", "Paused", "Blocked", "Complete", "Withdrawn"],
        )

    def test_each_value_has_a_meaning_a_kind_and_a_safety(self) -> None:
        for status in Status:
            with self.subTest(status=status.word):
                self.assertTrue(status.meaning)
                self.assertTrue(status.kinds)
                self.assertTrue(status.safe)

    def test_the_key_is_the_word_lower_case(self) -> None:
        self.assertEqual(Status.COMPLETE.key, "complete")

    def test_a_word_is_read_in_any_case_and_stripped(self) -> None:
        self.assertIs(Status.read("  Complete "), Status.COMPLETE)
        self.assertIs(Status.read("queued"), Status.QUEUED)

    def test_a_word_that_is_no_value_is_none_the_old_words_included(self) -> None:
        for word in ("", "open", "done", "Finished"):
            with self.subTest(word=word):
                self.assertIsNone(Status.read(word))


class Kinds(unittest.TestCase):
    def test_a_session_plan_may_be_queued_active_blocked_or_complete(self) -> None:
        self.assertEqual(
            Status.for_kind(Kind.SESSION_PLAN),
            (Status.QUEUED, Status.ACTIVE, Status.BLOCKED, Status.COMPLETE),
        )

    def test_a_session_report_may_be_active_blocked_or_complete(self) -> None:
        self.assertEqual(Status.for_kind(Kind.SESSION_REPORT), (Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

    def test_the_other_kinds_take_the_values_the_table_gives_them(self) -> None:
        self.assertEqual(
            Status.for_kind(Kind.EXPLANATION),
            (Status.DRAFT, Status.PROPOSED, Status.FINAL, Status.SUPERSEDED, Status.REJECTED),
        )
        self.assertEqual(Status.for_kind(Kind.HANDOFF), (Status.ACTIVE, Status.PAUSED, Status.BLOCKED, Status.COMPLETE))
        self.assertEqual(Status.for_kind(Kind.RESEARCH), (Status.ACTIVE, Status.PAUSED, Status.COMPLETE, Status.WITHDRAWN))

    def test_every_kind_has_values(self) -> None:
        for kind in Kind:
            with self.subTest(kind=kind.value):
                self.assertTrue(Status.for_kind(kind))


class ReportEnding(unittest.TestCase):
    def test_each_status_a_report_may_state_says_how_a_run_ended(self) -> None:
        for status in Status.for_kind(Kind.SESSION_REPORT):
            with self.subTest(status=status.word):
                self.assertTrue(status.report_ending)

    def test_no_other_status_has_one(self) -> None:
        for status in Status:
            if Kind.SESSION_REPORT not in status.kinds:
                with self.subTest(status=status.word):
                    self.assertIsNone(status.report_ending)


class Listing(unittest.TestCase):
    def test_the_words_of_a_kind_read_as_a_sentence(self) -> None:
        self.assertEqual(Status.listing(Kind.SESSION_PLAN), "Queued, Active, Blocked, or Complete")
        self.assertEqual(Status.listing(Kind.SESSION_REPORT), "Active, Blocked, or Complete")

    def test_the_words_of_a_kind_as_keys(self) -> None:
        self.assertEqual(Status.keys(Kind.SESSION_PLAN), ("queued", "active", "blocked", "complete"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
