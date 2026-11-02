#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for Status-kind Label_* words queried through Label_Status / DeclaredLabel.

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
from machine.plugable_import import load as plugable_load
from modules.knowledge.label.labels.Status import Label_Status
from modules.knowledge.label.primitive.label import LabelKind, LabelRegistry, Labels
from modules.identity.thing.labels.Active import Label_Active
from modules.identity.thing.labels.Blocked import Label_Blocked
from modules.identity.thing.labels.Complete import Label_Complete
from modules.identity.thing.labels.Draft import Label_Draft
from modules.identity.thing.labels.Final import Label_Final
from modules.identity.thing.labels.Paused import Label_Paused
from modules.identity.thing.labels.Proposed import Label_Proposed
from modules.identity.thing.labels.Queued import Label_Queued
from modules.identity.thing.labels.Rejected import Label_Rejected
from modules.identity.thing.labels.Superseded import Label_Superseded
from modules.identity.thing.labels.Withdrawn import Label_Withdrawn
Label_DocumentKind = plugable_load('knowledge.documentation.labels.DocumentKind').Label_DocumentKind
Label_Explanation = plugable_load('knowledge.documentation.explanation.labels.Explanation').Label_Explanation
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Report').Label_Report
Label_Handoff = plugable_load('knowledge.documentation.handoff.labels.Handoff').Label_Handoff
Label_Research = plugable_load('knowledge.documentation.research.labels.Research').Label_Research

class Values(unittest.TestCase):

    def test_the_type_holds_the_eleven_values_in_order(self) -> None:
        self.assertEqual([s.word for s in Label_Status.members()], [
            'Draft', 'Proposed', 'Final', 'Superseded', 'Rejected',
            'Queued', 'Active', 'Paused', 'Blocked', 'Complete', 'Withdrawn',
        ])

    def test_each_value_has_a_meaning_and_a_safety(self) -> None:
        for status in Label_Status.members():
            with self.subTest(status=status.word):
                self.assertTrue(status.meaning)
                self.assertTrue(status.safe)
                self.assertIn(Label_Status, status.labels)

    def test_the_key_is_the_word_lower_case(self) -> None:
        self.assertEqual(Label_Complete.key, 'complete')

    def test_a_word_is_read_in_any_case_and_stripped(self) -> None:
        self.assertIs(Label_Status.read('  Complete '), Label_Complete)
        self.assertIs(Label_Status.read('queued'), Label_Queued)

    def test_a_word_that_is_no_value_is_none_the_old_words_included(self) -> None:
        for word in ('', 'open', 'done', 'Finished'):
            with self.subTest(word=word):
                self.assertIsNone(Label_Status.read(word))

class StatusIsALabel(unittest.TestCase):

    def test_every_value_is_a_label_whose_definition_takes_the_status_label(self) -> None:
        definitions = Label_Status.definitions()
        self.assertEqual([d.label.word for d in definitions], [s.word for s in Label_Status.members()])
        for definition in definitions:
            with self.subTest(label=definition.label.word):
                self.assertTrue(definition.is_a(Label_Status.as_label))

    def test_the_identifiers_are_distinct_uuid_version_7(self) -> None:
        import re
        ids = [status.label.id for status in Label_Status.members()]
        self.assertEqual(len(set(ids)), len(ids))
        for one in ids:
            self.assertRegex(one, '^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')

    def test_the_registry_knows_them_as_statuses(self) -> None:
        kind = LabelKind(Label_Status.as_label, 'where a document stands', 'everything that reads a Status', str, Label_Status.definitions())
        registry = LabelRegistry([kind])
        self.assertEqual(
            registry.words(Labels((Label_Queued.label, Label_Complete.label)), 'Status'),
            ('Queued', 'Complete'),
        )

class Kinds(unittest.TestCase):

    def test_no_bag_types_remain_for_status_or_document_kind(self) -> None:
        from modules.knowledge.label import services as label_services
        self.assertFalse(hasattr(label_services, 'status_words'))
        self.assertFalse(hasattr(Label_Status, 'Kind'))
        self.assertFalse(hasattr(Label_DocumentKind, 'DocumentKind'))

    def test_a_task_plan_may_be_queued_active_blocked_or_complete(self) -> None:
        self.assertEqual(Label_Status.for_document(Label_Plan), (Label_Queued, Label_Active, Label_Blocked, Label_Complete))
        self.assertEqual(Label_Plan.statuses(), (Label_Queued, Label_Active, Label_Blocked, Label_Complete))

    def test_a_task_report_may_be_active_blocked_or_complete(self) -> None:
        self.assertEqual(Label_Status.for_document(Label_Report), (Label_Active, Label_Blocked, Label_Complete))

    def test_the_other_kinds_take_the_values_the_table_gives_them(self) -> None:
        self.assertEqual(Label_Status.for_document(Label_Explanation), (Label_Draft, Label_Proposed, Label_Final, Label_Superseded, Label_Rejected))
        self.assertEqual(Label_Status.for_document(Label_Handoff), (Label_Active, Label_Paused, Label_Blocked, Label_Complete))
        self.assertEqual(Label_Status.for_document(Label_Research), (Label_Active, Label_Paused, Label_Complete, Label_Withdrawn))

    def test_every_kind_has_values(self) -> None:
        for kind in Label_DocumentKind.members():
            with self.subTest(kind=kind.word):
                self.assertTrue(Label_Status.for_document(kind))

class ReportEnding(unittest.TestCase):

    def test_each_status_a_report_may_state_says_how_a_run_ended(self) -> None:
        for status in Label_Status.for_document(Label_Report):
            with self.subTest(status=status.word):
                self.assertTrue(status.report_ending)

    def test_no_other_document_life_status_outside_report_has_one(self) -> None:
        report = set(Label_Status.for_document(Label_Report))
        for status in Label_Status.members():
            if status not in report:
                with self.subTest(status=status.word):
                    self.assertIsNone(status.report_ending)

class Listing(unittest.TestCase):

    def test_the_words_of_a_kind_read_as_a_sentence(self) -> None:
        self.assertEqual(Label_Status.listing(Label_Plan), 'Queued, Active, Blocked, or Complete')
        self.assertEqual(Label_Status.listing(Label_Report), 'Active, Blocked, or Complete')

    def test_the_words_of_a_kind_as_keys(self) -> None:
        self.assertEqual(Label_Status.keys(Label_Plan), ('queued', 'active', 'blocked', 'complete'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
