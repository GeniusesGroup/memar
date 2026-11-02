#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from machine.plugable_import import load as plugable_load
Label_DocumentKind = plugable_load('knowledge.documentation.labels.Label_DocumentKind').Label_DocumentKind
Label_Explanation = plugable_load('knowledge.documentation.explanation.labels.Label_Explanation').Label_Explanation
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Label_Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Label_Report').Label_Report
Label_Handoff = plugable_load('knowledge.documentation.handoff.labels.Label_Handoff').Label_Handoff
Label_Research = plugable_load('knowledge.documentation.research.labels.Label_Research').Label_Research
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Complete import Label_Complete
from modules.identity.thing.labels.Label_Blocked import Label_Blocked
from modules.identity.thing.labels.Label_Active import Label_Active
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
SCRIPTS = TOP / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(TOP))
sys.dont_write_bytecode = True
_m_record = import_module('modules-plugable.knowledge.documentation.primitive.record')
PLAN = _m_record.PLAN
REPORT = _m_record.REPORT
_m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
PlanKey = _m_plan_key.PlanKey
_m_report_key = import_module('modules-plugable.knowledge.documentation.report.primitive.report_key')
ReportKey = _m_report_key.ReportKey
from modules.knowledge.content.primitive.record_key import ID_FIELD

class PlanRecord(unittest.TestCase):

    def test_the_file_and_the_parts(self) -> None:
        self.assertEqual(PLAN.file_name, 'plan.md')
        self.assertEqual(PLAN.parts, ('Request', 'Why', 'Steps', 'Next'))

    def test_the_keys_in_the_order_a_new_plan_writes_them(self) -> None:
        self.assertEqual([key.key for key in PLAN.keys], ['id', 'title', 'start date', 'project', 'parent', 'conversation', 'priority', 'labels', 'depends_on'])
        self.assertFalse(hasattr(PlanKey, 'STATUS'))

    def test_every_key_says_what_it_holds(self) -> None:
        for key in PLAN.keys:
            with self.subTest(key=key.key):
                self.assertTrue(key.description)

    def test_the_statuses_are_those_of_a_task_plan(self) -> None:
        self.assertEqual(PLAN.kind, Label_Plan)
        self.assertEqual(PLAN.statuses, (Label_Queued, Label_Active, Label_Blocked, Label_Complete))

    def test_a_key_is_written_in_pascal_case(self) -> None:
        self.assertEqual(PlanKey.PARENT.written, 'Parent')

    def test_the_start_date_is_named_for_what_it_is(self) -> None:
        self.assertEqual(PlanKey.START_DATE.key, 'start date')
        self.assertEqual(PlanKey.START_DATE.written, 'Start Date')
        self.assertFalse(hasattr(PlanKey, 'OPENED'))

    def test_an_earlier_name_of_a_key_is_still_read(self) -> None:
        front = {'task': 's-1', 'title': 'T', 'opened': '2026-10-01T00:00:00Z', 'project': '/work'}
        read = PLAN.current(front)
        self.assertEqual(read['id'], 's-1')
        self.assertEqual(read['start date'], '2026-10-01T00:00:00Z')
        self.assertEqual(front['task'], 's-1')

    def test_a_current_name_wins_over_an_earlier_one(self) -> None:
        read = PLAN.current({'id': 'new', 'task': 'old'})
        self.assertEqual(read['id'], 'new')

class ReportRecord(unittest.TestCase):

    def test_the_file_and_the_parts(self) -> None:
        self.assertEqual(REPORT.file_name, 'report.md')
        self.assertEqual(REPORT.parts, ('What ran', 'Check', 'Result', 'Left open'))

    def test_the_keys(self) -> None:
        self.assertEqual([key.key for key in REPORT.keys], ['id', 'title'])
        self.assertFalse(hasattr(ReportKey, 'STATUS'))

    def test_the_hand_back_part_and_its_limit(self) -> None:
        self.assertEqual(REPORT.hand_back_part, 'Decisions needed')
        self.assertEqual(REPORT.hand_back_max_lines, 10)

    def test_the_plan_has_no_hand_back_part(self) -> None:
        self.assertIsNone(PLAN.hand_back_part)

    def test_the_statuses_are_those_of_a_task_report(self) -> None:
        self.assertEqual(REPORT.kind, Label_Report)
        self.assertEqual(REPORT.statuses, (Label_Active, Label_Blocked, Label_Complete))

class TheId(unittest.TestCase):

    def test_both_records_open_with_the_id_of_the_record_they_belong_to(self) -> None:
        self.assertIs(PLAN.keys[0], PlanKey.ID)
        self.assertIs(REPORT.keys[0], ReportKey.ID)

    def test_the_field_is_declared_once_and_written_ID(self) -> None:
        self.assertIs(PlanKey.ID, ID_FIELD)
        self.assertIs(ReportKey.ID, ID_FIELD)
        self.assertEqual(PlanKey.ID.written, 'ID')
        self.assertEqual(ReportKey.ID.written, 'ID')
        self.assertFalse(hasattr(PlanKey, 'TASK'))
        self.assertFalse(hasattr(ReportKey, 'TASK'))

    def test_the_task_is_the_earlier_name(self) -> None:
        self.assertIn('task', PlanKey.ID.earlier)

class Outline(unittest.TestCase):

    def test_the_outline_names_every_key_and_part(self) -> None:
        for record in (PLAN, REPORT):
            text = record.outline()
            for key in record.keys:
                self.assertIn(f'{key.written}:', text)
            for part in record.parts:
                self.assertIn(f'## {part}', text)

    def test_the_outline_starts_and_ends_the_front_matter(self) -> None:
        lines = PLAN.outline().splitlines()
        self.assertEqual(lines[0], '---')
        self.assertIn('---', lines[1:])
if __name__ == '__main__':
    unittest.main(verbosity=2)
