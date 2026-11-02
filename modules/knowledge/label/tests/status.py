#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the Status type in `primitive/status.py`.

    python modules/knowledge/status/tests/status.py

The subject is the one vocabulary of Status every Memar document and record
draws on, named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

Nothing here reads or writes a file.

What is pinned, and what each pin is for:

  Values         The type holds the eleven values of the vocabulary,
                 each with its meaning, the kinds that may use it, and what is
                 safe to depend on; a word is read in any case, and a word that
                 is no value is None, never a guess.
  Kinds          A kind's values are those that list it, in table order; a
                 task plan may be Queued, Active, Blocked or Complete, and a
                 task report Active, Blocked or Complete.
  ReportEnding   Each value a task report may state says how a run that
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
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
SCRIPTS = TOP / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
from modules.knowledge.status.primitive.status import DocumentKind, Status

class Values(unittest.TestCase):

    def test_the_type_holds_the_eleven_values_in_order(self) -> None:
        self.assertEqual([status.word for status in Status], ['Draft', 'Proposed', 'Final', 'Superseded', 'Rejected', 'Queued', 'Active', 'Paused', 'Blocked', 'Complete', 'Withdrawn'])

    def test_each_value_has_a_meaning_a_kind_and_a_safety(self) -> None:
        for status in Status:
            with self.subTest(status=status.word):
                self.assertTrue(status.meaning)
                self.assertTrue(status.kinds)
                self.assertTrue(status.safe)

    def test_the_key_is_the_word_lower_case(self) -> None:
        self.assertEqual(Status.COMPLETE.key, 'complete')

    def test_a_word_is_read_in_any_case_and_stripped(self) -> None:
        self.assertIs(Status.read('  Complete '), Status.COMPLETE)
        self.assertIs(Status.read('queued'), Status.QUEUED)

    def test_a_word_that_is_no_value_is_none_the_old_words_included(self) -> None:
        for word in ('', 'open', 'done', 'Finished'):
            with self.subTest(word=word):
                self.assertIsNone(Status.read(word))

class StatusIsALabel(unittest.TestCase):
    """Status is a field of its own, and its values are labels of the Status label (owner, 2026-10-16)."""

    def test_every_value_is_a_label_whose_definition_takes_the_status_label(self) -> None:
        from modules.knowledge.status.primitive.status import STATUS_LABEL
        definitions = Status.definitions()
        self.assertEqual([d.label.word for d in definitions], [s.word for s in Status])
        for definition in definitions:
            with self.subTest(label=definition.label.word):
                self.assertTrue(definition.is_a(STATUS_LABEL))

    def test_the_identifiers_are_distinct_uuid_version_7(self) -> None:
        import re
        ids = [status.label.id for status in Status]
        self.assertEqual(len(set(ids)), len(ids))
        for one in ids:
            self.assertRegex(one, '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_the_registry_knows_them_as_statuses(self) -> None:
        from modules.knowledge.label.primitive.label import LabelKind, LabelRegistry, Labels
        from modules.knowledge.status.primitive.status import STATUS_LABEL
        kind = LabelKind(STATUS_LABEL, 'where a document stands', 'everything that reads a Status', str, Status.definitions())
        registry = LabelRegistry([kind])
        self.assertEqual(registry.words(Labels((Status.QUEUED.label, Status.DONE.label if hasattr(Status, 'DONE') else Status.COMPLETE.label)), 'Status'), ('Queued', 'Complete'))

class Kinds(unittest.TestCase):

    def test_the_kind_of_document_is_not_named_kind(self) -> None:
        import modules.knowledge.status.primitive.status as declared
        self.assertFalse(hasattr(declared, 'Kind'))

    def test_a_task_plan_may_be_queued_active_blocked_or_complete(self) -> None:
        self.assertEqual(Status.for_kind(DocumentKind.PLAN), (Status.QUEUED, Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

    def test_a_task_report_may_be_active_blocked_or_complete(self) -> None:
        self.assertEqual(Status.for_kind(DocumentKind.REPORT), (Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

    def test_the_other_kinds_take_the_values_the_table_gives_them(self) -> None:
        self.assertEqual(Status.for_kind(DocumentKind.EXPLANATION), (Status.DRAFT, Status.PROPOSED, Status.FINAL, Status.SUPERSEDED, Status.REJECTED))
        self.assertEqual(Status.for_kind(DocumentKind.HANDOFF), (Status.ACTIVE, Status.PAUSED, Status.BLOCKED, Status.COMPLETE))
        self.assertEqual(Status.for_kind(DocumentKind.RESEARCH), (Status.ACTIVE, Status.PAUSED, Status.COMPLETE, Status.WITHDRAWN))

    def test_every_kind_has_values(self) -> None:
        for kind in DocumentKind:
            with self.subTest(kind=kind.value):
                self.assertTrue(Status.for_kind(kind))

class ReportEnding(unittest.TestCase):

    def test_each_status_a_report_may_state_says_how_a_run_ended(self) -> None:
        for status in Status.for_kind(DocumentKind.REPORT):
            with self.subTest(status=status.word):
                self.assertTrue(status.report_ending)

    def test_no_other_status_has_one(self) -> None:
        for status in Status:
            if DocumentKind.REPORT not in status.kinds:
                with self.subTest(status=status.word):
                    self.assertIsNone(status.report_ending)

class Listing(unittest.TestCase):

    def test_the_words_of_a_kind_read_as_a_sentence(self) -> None:
        self.assertEqual(Status.listing(DocumentKind.PLAN), 'Queued, Active, Blocked, or Complete')
        self.assertEqual(Status.listing(DocumentKind.REPORT), 'Active, Blocked, or Complete')

    def test_the_words_of_a_kind_as_keys(self) -> None:
        self.assertEqual(Status.keys(DocumentKind.PLAN), ('queued', 'active', 'blocked', 'complete'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
