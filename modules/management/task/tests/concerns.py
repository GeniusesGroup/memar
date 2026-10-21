#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what a session's plan gives away about finished-but-open and abandoned work, in `modules/management/task/services/concerns.py`.

    python modules/management/task/tests/concerns.py

The subject is the flags `list`, `gc`, and `digest` raise on a session that
looks finished or abandoned yet is not complete: named for the file that holds it
per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The expectations are those of session 20261013T041036Z-24948-0: the sweep moves
only `complete` sessions and never deletes anything new, so a session it keeps for
ever is flagged, not removed.

Nothing here writes outside its scratch folder.

What is pinned, and what each pin is for:

  FinishedButOpen    A plan whose Steps are all checked and at least one exists,
                     with Status active, is flagged; one with an unchecked step,
                     no steps, or Status other than active is not.
  AbandonedPlan      A plan with an empty Request that has been quiet for at
                     least a day is flagged; a fresh one and one with a
                     Request are not.
  NoStatus           A readable plan with front matter and no status is
                     flagged; a status outside the vocabulary is already
                     `session_report.disagreement`'s to name, so it is not
                     named twice.
  EarlierShape       A plan or a report in an earlier shape (lower-case keys, a
                     body status, a Stop line, an Outcome key, the old words)
                     is flagged once, with where today's shape is shown, and
                     the plan is not also flagged for having no status.
  DoneIsQuiet        A complete session raises no flag, however it looks.
  NothingDeleted     Flagging moves and writes nothing.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
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
import modules.management.task.services.concerns as session_concerns
from modules.management.task.services.folder import read_session
import modules.knowledge.documentation.plan.services.plan as session_plan
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME
DAY = 24 * 60 * 60

def plan_text(status: str | None='active', request: str='Do the thing.', steps: str='- [ ] 1. a') -> str:
    status_line = f'Status: {status.capitalize()}\n' if status is not None else ''
    return f'---\nTitle: T\n{status_line}Opened: 2026-10-01T00:00:00Z\nProject: P\n---\n# T\n\n## Request\n{request}\n\n## Why\nw\n\n## Steps\n{steps}\n\n## Next\nn\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def concerns(self, text: str, idle_days: float=3) -> list[str]:
        folder = self.root / '20261001T000000Z-1-0'
        folder.mkdir(exist_ok=True)
        plan = folder / PLAN_NAME
        plan.write_text(text, encoding='utf-8', newline='\n')
        when = time.time() - idle_days * DAY
        os.utime(plan, (when, when))
        os.utime(folder, (when, when))
        return session_concerns.concerns(read_session(folder))

class FinishedButOpen(Fixture):

    def test_every_step_checked_yet_open_is_flagged(self) -> None:
        found = self.concerns(plan_text(steps='- [x] 1. a\n- [X] 2. b'))
        self.assertEqual(found, ['every step is checked, yet the status is active'])

    def test_an_unchecked_step_is_not_flagged(self) -> None:
        self.assertEqual(self.concerns(plan_text(steps='- [x] 1. a\n- [ ] 2. b')), [])

    def test_no_steps_is_not_flagged_as_finished(self) -> None:
        self.assertEqual(self.concerns(plan_text(steps='')), [])

    def test_a_blocked_plan_with_every_step_checked_is_not_flagged(self) -> None:
        self.assertEqual(self.concerns(plan_text(status='blocked', steps='- [x] 1. a')), [])

class AbandonedPlan(Fixture):

    def test_an_empty_request_quiet_for_a_day_is_flagged(self) -> None:
        found = self.concerns(plan_text(request=''), idle_days=3)
        self.assertEqual(found, ['its Request is empty and nothing has changed for 3.0 days'])

    def test_a_queued_plan_with_an_empty_request_is_flagged_too(self) -> None:
        self.assertEqual(len(self.concerns(plan_text(status='queued', request=''), idle_days=3)), 1)

    def test_a_fresh_empty_request_is_not_flagged(self) -> None:
        self.assertEqual(self.concerns(plan_text(request=''), idle_days=0.1), [])

    def test_a_written_request_is_not_flagged(self) -> None:
        self.assertEqual(self.concerns(plan_text(), idle_days=30), [])

class NoStatus(Fixture):

    def test_a_plan_with_no_status_is_flagged(self) -> None:
        self.assertEqual(self.concerns(plan_text(status=None)), ['it has no status'])

    def test_a_status_outside_the_vocabulary_is_left_to_the_disagreement(self) -> None:
        self.assertEqual(self.concerns(plan_text(status='wip, nearly there')), [])

class EarlierShape(Fixture):

    def flagged(self, plan: str, report: str | None=None) -> list[str]:
        folder = self.root / '20261001T000000Z-1-0'
        found = self.concerns(plan)
        if report is not None:
            (folder / 'report.md').write_text(report, encoding='utf-8', newline='\n')
            return session_concerns.concerns(read_session(folder))
        return found

    def test_an_earlier_plan_is_flagged_once_with_the_remedy_and_not_for_having_no_status(self) -> None:
        old = '---\ntitle: T\nopened: x\nproject: P\n---\n# T\nStatus: open\n\n## Request\nr\n'
        found = self.flagged(old)
        self.assertEqual(len(found), 1)
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, found[0])
        self.assertIn('earlier shape', found[0])

    def test_an_earlier_complete_plan_is_flagged_too(self) -> None:
        old = '---\ntitle: T\nopened: x\nproject: P\n---\n# T\nStatus: done\n\n## Request\nr\n'
        self.assertEqual(len(self.flagged(old)), 1)

    def test_an_earlier_report_is_flagged_with_the_remedy(self) -> None:
        found = self.flagged(plan_text(status='complete'), '# Report\nStop: success\n')
        self.assertEqual(len(found), 1)
        self.assertIn('report.md is in an earlier shape', found[0])
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, found[0])

    def test_todays_shapes_raise_nothing(self) -> None:
        self.assertEqual(self.flagged(plan_text(), '---\nStatus: Active\n---\n# Report\n'), [])

class DoneIsQuiet(Fixture):

    def test_a_complete_session_raises_nothing(self) -> None:
        self.assertEqual(self.concerns(plan_text(status='complete', request='', steps='- [x] 1. a'), idle_days=30), [])

class NothingDeleted(Fixture):

    def test_flagging_leaves_the_folder_as_it_was(self) -> None:
        self.concerns(plan_text(request='', steps='- [x] 1. a'))
        folder = self.root / '20261001T000000Z-1-0'
        self.assertEqual(sorted((path.name for path in folder.iterdir())), [PLAN_NAME])
if __name__ == '__main__':
    unittest.main()
