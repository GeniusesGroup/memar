#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for report content shape in `modules-plugable/knowledge/documentation/report/services/report_text.py`.

    python modules-plugable/knowledge/documentation/report/tests/report_text.py

The subject is the report template readers of a timeline content of kind
report. Facts of the task live in `task.yaml`; the report is the latest
content of kind report.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
from modules.knowledge.label.labels.Status import Label_Status
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
TASK_TESTS = TOP / 'modules-plugable' / 'management' / 'task' / 'tests'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.path.insert(2, str(TASK_TESTS))
sys.dont_write_bytecode = True
Label_Plan = plugable_load('knowledge.documentation.plan.labels.Plan').Label_Plan
Label_Report = plugable_load('knowledge.documentation.report.labels.Report').Label_Report
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
import shape
timeline_files = import_module('modules.management.timeline.services.timeline_files')
task_report = import_module('modules-plugable.knowledge.documentation.report.services.report_text')
NEW_PARTS = '# Report\n\n## What ran\nx\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)

    def _facts(self) -> None:
        if not (self.folder / shape.FACTS_NAME).exists():
            shape.from_plan_text(self.folder, '---\nTitle: T\nStatus: Active\nOpened: 2026-10-01T00:00:00Z\nProject: P\n---\n# T\n\n## Request\nx\n')

    def report(self, text: str) -> Path:
        stripped = text.lstrip()
        front = ''
        body = text
        if stripped.startswith('---'):
            parts = stripped.split('---\n', 2)
            front = parts[1] if len(parts) > 1 else ''
            body = parts[2] if len(parts) > 2 else ''
        status = next((line.split(':', 1)[1].strip().lower() for line in front.splitlines() if line.lower().startswith('status:')), '')
        self._facts()
        # Earlier-shape markers (Stop/Outcome/lower-case/open/done) stay in the body/front of timeline content.
        timeline_files.add_text(self.folder, 'report', body if stripped.startswith('---') else text, 'agent', fields={'status': status} if status else None)
        return self.folder

    def new(self, status: str) -> Path:
        return self.report(f'---\nStatus: {status}\n---\n{NEW_PARTS}')

class Skeleton(Fixture):

    def test_a_new_report_names_its_task_and_the_parts_without_a_status(self) -> None:
        self.assertEqual(task_report.report_skeleton('s-1', 'The task'), '---\nID: s-1\nTitle: The task\n---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n')
        self.assertEqual(task_report.report_skeleton('s-1'), '---\nID: s-1\n---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n')

    def test_an_empty_folder_says_nothing(self) -> None:
        self.assertEqual(task_report.read_report_status(self.folder), '')
        self.assertIsNone(task_report.disagreement('active', task_report.read_report_status(self.folder)))
        self.assertIsNone(task_report.report_shape_problem(self.folder))

    def test_a_report_may_state_the_statuses_the_table_gives_a_task_report(self) -> None:
        self.assertEqual(Label_Status.keys(Label_Report), ('active', 'blocked', 'complete'))

class ReadsTodaysShape(Fixture):

    def test_a_new_shape_report_carries_no_status_field(self) -> None:
        self.assertEqual(task_report.read_report_status(self.new('Complete')), '')
        self.assertEqual(task_report.read_report_status(self.new('blocked')), '')

    def test_the_decisions_are_found_below_front_matter_too(self) -> None:
        self.report('---\nStatus: Blocked\n---\n# Report\n\n## Decisions needed\n- Q?\n')
        self.assertEqual(task_report.decisions_needed(self.folder), ['- Q?'])

    def test_no_report_or_an_unreadable_one_says_nothing(self) -> None:
        self.assertEqual(task_report.read_report_status(self.folder), '')
        self._facts()
        (self.folder / 'content.00001.md').write_bytes(b'---\nkind: report\nauthor: agent\nplaced_at: 2026-10-01T00:00:00Z\n---\n\xff\xfe')
        self.assertEqual(task_report.read_report_status(self.folder), '')

class ShapeProblem(Fixture):

    def test_a_stop_line_in_the_body_is_an_earlier_shape(self) -> None:
        self._facts()
        timeline_files.add_text(self.folder, 'report', '# Report\nStop: success\n\n## What ran\nx\n', 'agent')
        found = task_report.report_shape_problem(self.folder)
        self.assertIsNotNone(found)
        self.assertIn(task_report.EARLIER_SHAPE_REMEDY, found)

    def test_todays_shape_prose_and_no_report_have_none(self) -> None:
        self.assertIsNone(task_report.report_shape_problem(self.new('Complete')))
        self.assertIsNone(task_report.report_shape_problem(self.report('# Prose only\nno marks\n')))
        self.assertIsNone(task_report.report_shape_problem(self.folder / 'elsewhere'))

class Agreement(unittest.TestCase):

    def test_a_task_status_in_the_vocabulary_is_fine(self) -> None:
        for status in Label_Status.keys(Label_Plan):
            with self.subTest(status=status):
                self.assertIsNone(task_report.disagreement(status, 'ignored'))

    def test_case_does_not_matter(self) -> None:
        self.assertIsNone(task_report.disagreement('Complete', 'complete'))
        self.assertIsNone(task_report.disagreement('active', 'Active'))

    def test_a_report_status_is_ignored(self) -> None:
        self.assertIsNone(task_report.disagreement('active', 'complete'))
        self.assertIsNone(task_report.disagreement('complete', 'blocked'))
        self.assertIsNone(task_report.disagreement('complete', 'finished'))

    def test_a_status_outside_the_vocabulary_is_named(self) -> None:
        self.assertEqual(task_report.disagreement('archived', 'complete'), 'status archived is not one of queued, active, blocked, complete')
        self.assertEqual(task_report.disagreement('open', 'complete'), 'status open is not one of queued, active, blocked, complete')

    def test_an_empty_task_status_checks_nothing(self) -> None:
        self.assertIsNone(task_report.disagreement('', 'complete'))
        self.assertIsNone(task_report.disagreement('complete', ''))

class HandBack(Fixture):

    def test_a_report_is_a_hand_back_without_a_status_field(self) -> None:
        self.assertIsNone(task_report.handback_problem(self.new('Complete'), 'complete'))
        self.assertIsNone(task_report.handback_problem(self.new('Blocked'), 'Blocked'))
        self.report('---\nID: t\n---\n# Report\n')
        self.assertIsNone(task_report.handback_problem(self.folder, 'active'))

    def test_a_missing_report_is_named(self) -> None:
        self.assertEqual(task_report.handback_problem(self.folder, 'active'), 'report is missing')

    def test_more_than_ten_decision_lines_are_not_a_hand_back(self) -> None:
        lines = ''.join((f'- Q{index}?\n' for index in range(11)))
        self.report(f'---\nID: t\n---\n# Report\n\n## Decisions needed\n{lines}')
        self.assertEqual(task_report.handback_problem(self.folder, 'blocked'), '11 lines under Decisions needed, more than 10')

if __name__ == '__main__':
    unittest.main(verbosity=2)
