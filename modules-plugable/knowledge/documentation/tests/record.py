#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the task record types in `record.py`.

    python modules-plugable/management/task/tests/record.py

The subject is the shape of a task's plan.md and report.md, declared once,
named for the file that holds it per
[Test Naming](../../../process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../process/test/rules/test-placement/test-placement.md).

Nothing here writes.

What is pinned, and what each pin is for:

PlanRecord    plan.md: the front-matter keys in the order a new plan
                 writes them, each with a description, and the four parts; its
                 Statuses are those the table gives a task plan.
  ReportRecord  report.md: the task's id, the Title and Status keys, the
                 four parts, the `Decisions needed` hand-back part and its
                 ten-line limit; its Statuses are those the table gives a
                 task report.
  TheId         Both records open with one field, ID (the Explanation's ID and
                 a task's `Task` are one), from the one declaration;
                 the plan's Start Date replaces `Opened`, and a file written
                 with an earlier name is still read as the current key.
  Outline       The shape rendered for a help text names every key and every
                 part, produced from the record and kept nowhere else.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
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
from modules.knowledge.status.primitive.status import DocumentKind, Status

class PlanRecord(unittest.TestCase):

    def test_the_file_and_the_parts(self) -> None:
        self.assertEqual(PLAN.file_name, 'plan.md')
        self.assertEqual(PLAN.parts, ('Request', 'Why', 'Steps', 'Next'))

    def test_the_keys_in_the_order_a_new_plan_writes_them(self) -> None:
        self.assertEqual([key.key for key in PLAN.keys], ['id', 'title', 'status', 'start date', 'project', 'parent', 'conversation', 'priority', 'labels', 'depends_on'])
        self.assertIs(PlanKey.STATUS, PLAN.keys[2])

    def test_every_key_says_what_it_holds(self) -> None:
        for key in PLAN.keys:
            with self.subTest(key=key.key):
                self.assertTrue(key.description)

    def test_the_statuses_are_those_of_a_task_plan(self) -> None:
        self.assertEqual(PLAN.kind, DocumentKind.PLAN)
        self.assertEqual(PLAN.statuses, (Status.QUEUED, Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

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
        self.assertEqual([key.key for key in REPORT.keys], ['id', 'title', 'status'])
        self.assertIs(ReportKey.STATUS, REPORT.keys[2])

    def test_the_hand_back_part_and_its_limit(self) -> None:
        self.assertEqual(REPORT.hand_back_part, 'Decisions needed')
        self.assertEqual(REPORT.hand_back_max_lines, 10)

    def test_the_plan_has_no_hand_back_part(self) -> None:
        self.assertIsNone(PLAN.hand_back_part)

    def test_the_statuses_are_those_of_a_task_report(self) -> None:
        self.assertEqual(REPORT.kind, DocumentKind.REPORT)
        self.assertEqual(REPORT.statuses, (Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

class TheId(unittest.TestCase):
    """Task (plan, report) and ID (Explanation) are one field, named ID (owner, 2026-10-16)."""

    def test_both_records_open_with_the_id_of_the_record_they_belong_to(self) -> None:
        self.assertIs(PLAN.keys[0], PlanKey.ID)
        self.assertIs(REPORT.keys[0], ReportKey.ID)

    def test_the_field_is_declared_once_and_written_ID(self) -> None:
        self.assertEqual(PlanKey.ID.value, ID_FIELD)
        self.assertEqual(ReportKey.ID.value, ID_FIELD)
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
