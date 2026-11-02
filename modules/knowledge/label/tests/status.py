#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for Status-kind Label_* words queried through status_words / taking.

    python modules/knowledge/label/tests/status.py
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
from modules.knowledge.label.primitive.label import LabelKind, LabelRegistry, Labels
from modules.knowledge.label.services.status_words import (
    STATUS_LABEL, document_kinds, statuses, statuses_for, status_keys, status_listing,
    status_definitions, read_status, Label_Plan, Label_Report, Label_Explanation,
    Label_Handoff, Label_Research,
)
from modules.identity.thing.labels.Label_Active import Label_Active
from modules.identity.thing.labels.Label_Blocked import Label_Blocked
from modules.identity.thing.labels.Label_Complete import Label_Complete
from modules.identity.thing.labels.Label_Draft import Label_Draft
from modules.identity.thing.labels.Label_Final import Label_Final
from modules.identity.thing.labels.Label_Paused import Label_Paused
from modules.identity.thing.labels.Label_Proposed import Label_Proposed
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Rejected import Label_Rejected
from modules.identity.thing.labels.Label_Superseded import Label_Superseded
from modules.identity.thing.labels.Label_Withdrawn import Label_Withdrawn

class Values(unittest.TestCase):

    def test_the_type_holds_the_eleven_values_in_order(self) -> None:
        self.assertEqual([s.word for s in statuses()], [
            'Draft', 'Proposed', 'Final', 'Superseded', 'Rejected',
            'Queued', 'Active', 'Paused', 'Blocked', 'Complete', 'Withdrawn',
        ])

    def test_each_value_has_a_meaning_a_kind_and_a_safety(self) -> None:
        for status in statuses():
            with self.subTest(status=status.word):
                self.assertTrue(status.meaning)
                self.assertTrue(status.kinds)
                self.assertTrue(status.safe)

    def test_the_key_is_the_word_lower_case(self) -> None:
        self.assertEqual(Label_Complete.key, 'complete')

    def test_a_word_is_read_in_any_case_and_stripped(self) -> None:
        self.assertIs(read_status('  Complete '), Label_Complete)
        self.assertIs(read_status('queued'), Label_Queued)

    def test_a_word_that_is_no_value_is_none_the_old_words_included(self) -> None:
        for word in ('', 'open', 'done', 'Finished'):
            with self.subTest(word=word):
                self.assertIsNone(read_status(word))

class StatusIsALabel(unittest.TestCase):

    def test_every_value_is_a_label_whose_definition_takes_the_status_label(self) -> None:
        definitions = status_definitions()
        self.assertEqual([d.label.word for d in definitions], [s.word for s in statuses()])
        for definition in definitions:
            with self.subTest(label=definition.label.word):
                self.assertTrue(definition.is_a(STATUS_LABEL))

    def test_the_identifiers_are_distinct_uuid_version_7(self) -> None:
        import re
        ids = [status.label.id for status in statuses()]
        self.assertEqual(len(set(ids)), len(ids))
        for one in ids:
            self.assertRegex(one, '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_the_registry_knows_them_as_statuses(self) -> None:
        kind = LabelKind(STATUS_LABEL, 'where a document stands', 'everything that reads a Status', str, status_definitions())
        registry = LabelRegistry([kind])
        self.assertEqual(
            registry.words(Labels((Label_Queued.label, Label_Complete.label)), 'Status'),
            ('Queued', 'Complete'),
        )

class Kinds(unittest.TestCase):

    def test_the_kind_of_document_is_not_named_kind(self) -> None:
        import modules.knowledge.label.services.status_words as declared
        self.assertFalse(hasattr(declared, 'Kind'))
        self.assertFalse(hasattr(declared, 'Status'))
        self.assertFalse(hasattr(declared, 'DocumentKind'))

    def test_a_task_plan_may_be_queued_active_blocked_or_complete(self) -> None:
        self.assertEqual(statuses_for(Label_Plan), (Label_Queued, Label_Active, Label_Blocked, Label_Complete))

    def test_a_task_report_may_be_active_blocked_or_complete(self) -> None:
        self.assertEqual(statuses_for(Label_Report), (Label_Active, Label_Blocked, Label_Complete))

    def test_the_other_kinds_take_the_values_the_table_gives_them(self) -> None:
        self.assertEqual(statuses_for(Label_Explanation), (Label_Draft, Label_Proposed, Label_Final, Label_Superseded, Label_Rejected))
        self.assertEqual(statuses_for(Label_Handoff), (Label_Active, Label_Paused, Label_Blocked, Label_Complete))
        self.assertEqual(statuses_for(Label_Research), (Label_Active, Label_Paused, Label_Complete, Label_Withdrawn))

    def test_every_kind_has_values(self) -> None:
        for kind in document_kinds():
            with self.subTest(kind=kind.word):
                self.assertTrue(statuses_for(kind))

class ReportEnding(unittest.TestCase):

    def test_each_status_a_report_may_state_says_how_a_run_ended(self) -> None:
        for status in statuses_for(Label_Report):
            with self.subTest(status=status.word):
                self.assertTrue(status.report_ending)

    def test_no_other_status_has_one(self) -> None:
        for status in statuses():
            if Label_Report.word not in status.kinds:
                with self.subTest(status=status.word):
                    self.assertIsNone(status.report_ending)

class Listing(unittest.TestCase):

    def test_the_words_of_a_kind_read_as_a_sentence(self) -> None:
        self.assertEqual(status_listing(Label_Plan), 'Queued, Active, Blocked, or Complete')
        self.assertEqual(status_listing(Label_Report), 'Active, Blocked, or Complete')

    def test_the_words_of_a_kind_as_keys(self) -> None:
        self.assertEqual(status_keys(Label_Plan), ('queued', 'active', 'blocked', 'complete'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
