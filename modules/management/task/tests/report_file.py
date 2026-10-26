#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a task's report.md in `modules/management/task/services/report_file.py`.

    python modules/management/task/tests/report_file.py

The subject is the report format the task services read and write, named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: reports are written under the
folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names and removed with it.

What is pinned, and what each pin is for:

Skeleton          A new report names the task it belongs to, then front
                     matter with an empty Status (and the Title when known),
                     its heading, and the four parts; one that is there is
                     never overwritten.
  ReadsTodaysShape  The Status is the front matter's `Status`, lowercased; an
                    unknown word is returned as written; nothing else gives a
                    report a status: not a lower-case key, an `Outcome` key, a
                    `Stop:` line, and the old words open and done are not
                    translated.
  ShapeProblem      A report in an earlier shape (a `Stop:` line, an `Outcome`
                    key, lower-case keys, the words open or done) is named with
                    where today's shape is shown (`memar task ensure --help`)
                    and no conversion script; today's shape, and prose with no
                    mark, are not.
  Agreement         A plan's status and a report's Status agree when they are
                    equal; an empty report status or an empty plan status
                    checks nothing.
  HandBack          A report is a hand-back when it states a Status that agrees
                    with its plan and holds at most ten lines of decisions.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.management.task.services.report_file as task_report
from modules.knowledge.status.primitive.status import DocumentKind, Status
NEW_PARTS = '# Report\n\n## What ran\nx\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)

    def report(self, text: str) -> Path:
        (self.folder / task_report.REPORT_NAME).write_text(text, encoding='utf-8', newline='\n')
        return self.folder

    def new(self, status: str) -> Path:
        return self.report(f'---\nStatus: {status}\n---\n{NEW_PARTS}')

    def outcome(self, outcome: str) -> Path:
        """A report of the shape that kept an `Outcome` beside an empty Status."""
        return self.report(f'---\nStatus:\nOutcome: {outcome}\n---\n{NEW_PARTS}')

    def old(self, stop: str) -> Path:
        return self.report(f'# Report\nStop: {stop}\n\n## What ran\nx\n')

class Skeleton(Fixture):

    def test_a_new_report_names_its_task_then_has_an_empty_status_and_the_parts(self) -> None:
        self.assertEqual(task_report.report_skeleton('s-1', 'The task'), '---\nID: s-1\nTitle: The task\nStatus:\n---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n')
        self.assertEqual(task_report.report_skeleton('s-1'), '---\nID: s-1\nStatus:\n---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n')

    def test_an_empty_skeleton_says_nothing(self) -> None:
        task_report.write_report(self.folder, 's-1', 'The task')
        self.assertEqual(task_report.read_report_status(self.folder), '')
        self.assertIsNone(task_report.disagreement('active', task_report.read_report_status(self.folder)))
        self.assertIsNone(task_report.report_shape_problem(self.folder))

    def test_a_report_that_is_there_is_never_overwritten(self) -> None:
        self.new('Complete')
        task_report.write_report(self.folder, 's-1', 'The task')
        self.assertEqual(task_report.read_report_status(self.folder), 'complete')

    def test_a_report_may_state_the_statuses_the_table_gives_a_task_report(self) -> None:
        self.assertEqual(Status.keys(DocumentKind.REPORT), ('active', 'blocked', 'complete'))

class ReadsTodaysShape(Fixture):

    def test_the_status_is_read_from_the_front_matter_in_any_value_case(self) -> None:
        self.assertEqual(task_report.read_report_status(self.new('Complete')), 'complete')
        self.assertEqual(task_report.read_report_status(self.new('blocked')), 'blocked')
        self.assertEqual(task_report.read_report_status(self.new('Finished')), 'finished')

    def test_nothing_else_gives_a_report_a_status(self) -> None:
        self.assertEqual(task_report.read_report_status(self.report('---\nstatus: Complete\n---\n' + NEW_PARTS)), '')
        for word in ('success', 'blocked', 'exhausted'):
            with self.subTest(word=word):
                self.assertEqual(task_report.read_report_status(self.outcome(word)), '')
                self.assertEqual(task_report.read_report_status(self.old(word)), '')
        self.report('---\nStatus: Blocked\nOutcome: success\n---\n# Report\nStop: success\n')
        self.assertEqual(task_report.read_report_status(self.folder), 'blocked')

    def test_the_old_status_words_are_not_translated(self) -> None:
        self.assertEqual(task_report.read_report_status(self.new('done')), 'done')
        self.assertEqual(task_report.read_report_status(self.new('open')), 'open')

    def test_no_report_or_an_unreadable_one_says_nothing(self) -> None:
        self.assertEqual(task_report.read_report_status(self.folder), '')
        (self.folder / task_report.REPORT_NAME).write_bytes(b'---\nStatus: \xff\xfe\n---\n')
        self.assertEqual(task_report.read_report_status(self.folder), '')

    def test_the_decisions_are_found_below_front_matter_too(self) -> None:
        self.report('---\nStatus: Blocked\n---\n# Report\n\n## Decisions needed\n- Q?\n')
        self.assertEqual(task_report.decisions_needed(self.folder), ['- Q?'])

class ShapeProblem(Fixture):

    def test_each_earlier_shape_is_named_with_where_todays_shape_is_shown(self) -> None:
        shapes = {'a Stop line': self.old('success'), 'an Outcome key': self.outcome('success'), 'an Outcome key beside a Status': self.report('---\nStatus: Complete\nOutcome: success\n---\n' + NEW_PARTS), 'lower-case keys': self.report('---\nstatus: Complete\n---\n' + NEW_PARTS), 'the old word done': self.new('done'), 'the old word open': self.new('open')}
        for name, folder in shapes.items():
            with self.subTest(shape=name):
                found = task_report.report_shape_problem(folder)
                self.assertIsNotNone(found)
                self.assertIn(task_report.EARLIER_SHAPE_REMEDY, found)
                self.assertIn('memar task ensure --help', found)
                self.assertNotIn('.py', found)

    def test_todays_shape_prose_and_no_report_have_none(self) -> None:
        self.assertIsNone(task_report.report_shape_problem(self.new('Complete')))
        self.assertIsNone(task_report.report_shape_problem(self.report('---\nStatus:\n---\n' + NEW_PARTS)))
        self.assertIsNone(task_report.report_shape_problem(self.report('# Prose only\nno marks\n')))
        self.assertIsNone(task_report.report_shape_problem(self.folder / 'elsewhere'))

    def test_a_hand_back_in_an_earlier_shape_names_it(self) -> None:
        self.assertIn(task_report.EARLIER_SHAPE_REMEDY, task_report.handback_problem(self.old('success'), 'complete'))

class Agreement(unittest.TestCase):

    def test_equal_statuses_agree(self) -> None:
        for status in Status.keys(DocumentKind.REPORT):
            with self.subTest(status=status):
                self.assertIsNone(task_report.disagreement(status, status))

    def test_case_does_not_matter(self) -> None:
        self.assertIsNone(task_report.disagreement('Complete', 'complete'))
        self.assertIsNone(task_report.disagreement('active', 'Active'))

    def test_a_report_status_that_is_not_the_plans_is_named(self) -> None:
        self.assertEqual(task_report.disagreement('active', 'complete'), "report.md Status complete is not the plan's active")
        self.assertEqual(task_report.disagreement('complete', 'blocked'), "report.md Status blocked is not the plan's complete")

    def test_a_status_outside_the_vocabulary_is_named_first_and_an_unknown_report_status_after(self) -> None:
        self.assertEqual(task_report.disagreement('archived', 'complete'), 'status archived is not one of queued, active, blocked, complete')
        self.assertEqual(task_report.disagreement('open', 'complete'), 'status open is not one of queued, active, blocked, complete')
        self.assertEqual(task_report.disagreement('complete', 'finished'), 'report.md Status finished is not one of active, blocked, complete')

    def test_an_empty_report_status_or_an_empty_plan_status_checks_nothing(self) -> None:
        self.assertIsNone(task_report.disagreement('complete', ''))
        self.assertIsNone(task_report.disagreement('queued', ''))
        self.assertIsNone(task_report.disagreement('', 'complete'))

class HandBack(Fixture):

    def test_a_report_that_agrees_is_a_hand_back(self) -> None:
        self.assertIsNone(task_report.handback_problem(self.new('Complete'), 'complete'))
        self.assertIsNone(task_report.handback_problem(self.new('Blocked'), 'Blocked'))

    def test_no_status_is_named_as_such(self) -> None:
        self.report('---\nStatus:\n---\n# Report\n')
        self.assertEqual(task_report.handback_problem(self.folder, 'active'), 'report.md has no Status')

    def test_a_disagreeing_status_is_named(self) -> None:
        self.assertIn("Status complete is not the plan's blocked", task_report.handback_problem(self.new('Complete'), 'blocked'))
        self.assertIn("Status complete is not the plan's active", task_report.handback_problem(self.new('Complete'), 'active'))

    def test_more_than_ten_decision_lines_are_not_a_hand_back(self) -> None:
        lines = ''.join((f'- Q{index}?\n' for index in range(11)))
        self.report(f'---\nStatus: Blocked\n---\n# Report\n\n## Decisions needed\n{lines}')
        self.assertEqual(task_report.handback_problem(self.folder, 'blocked'), '11 lines under Decisions needed, more than 10')
if __name__ == '__main__':
    unittest.main(verbosity=2)
