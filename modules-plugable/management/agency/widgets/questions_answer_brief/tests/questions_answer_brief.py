#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for agency Questions_Answer_Brief, realized in
`modules-plugable/management/agency/widgets/questions_answer_brief/questions_answer_brief.py`.

    python modules-plugable/management/agency/widgets/questions_answer_brief/tests/questions_answer_brief.py

The stable command face remains `memar ai_get_task_questions_answer_brief`.

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `modules/process/test/services/test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneText          The text is one line: it hands over the questions of ID to
                   answer, not its task, names
                   `memar agency_get_task_answer_context --task-id ID` as
                   the first command and never `start`, and carries nothing of
                   the questions.
  Printed          It is printed alone for a task with a line under its
                   report's `Decisions needed`; a task with none, or with
                   no plan, has no questions and is refused.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
plan_brief = import_module('modules-plugable.management.agency.widgets.plan_carry_out_brief.plan_carry_out_brief')
questions_brief = import_module('modules-plugable.management.agency.widgets.questions_answer_brief.questions_answer_brief')
import shape
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
plan_skeleton = _m_plan_text.plan_skeleton
SID = '20261011-T000000Z-1'
QUESTIONS_BRIEF = f'Your task is to answer the questions of task {SID}, not to take it up. Run `memar agency_get_task_answer_context --task-id {SID}` first, before anything else, and follow what it prints. Where Memar\'s MCP tools are listed, call the tool `agency_get_task_answer_context` with the same arguments instead of running the command.'
REPORT_WITH_QUESTIONS = '---\nTitle: R\nStatus: Blocked\n---\n# Report\n\n## Decisions needed\n- Q1: which name?\n'
REPORT_WITHOUT = '---\nTitle: R\nStatus: Complete\n---\n# Report\n\n## Decisions needed\n\n## Result\nDone.\n'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, report: str | None=None) -> Path:
        folder = memar_fs.task_dir(SID, create=True)
        shape.from_plan_text(folder, plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', self.fake_root))
        if report is not None:
            shape.add_report(folder, 'blocked' if 'Blocked' in report else 'complete', report.split('---\n', 2)[2])
        return folder

class OneText(Fixture):

    def test_the_text_is_one_line_naming_the_answering_command_and_not_start(self) -> None:
        text = questions_brief.questions_brief_text(SID)
        self.assertEqual(text, QUESTIONS_BRIEF)
        self.assertNotIn('\n', text)
        self.assertNotIn('task start', text)
        self.assertNotEqual(text, plan_brief.brief_text(SID))

class Printed(Fixture):

    def test_it_prints_the_text_alone_for_a_task_with_questions(self) -> None:
        self.task(REPORT_WITH_QUESTIONS)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            questions_brief.get_task_questions_answer_brief(SID)
        self.assertEqual(out.getvalue(), QUESTIONS_BRIEF + '\n')

    def test_a_task_with_no_question_under_decisions_needed_is_refused(self) -> None:
        for report in (None, REPORT_WITHOUT):
            with self.subTest(report=report):
                self.task(report)
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as refused:
                    questions_brief.get_task_questions_answer_brief(SID)
                self.assertEqual(out.getvalue(), '')
                self.assertIn(f'no questions to answer in {SID}', str(refused.exception.code))
                self.assertIn('Decisions needed', str(refused.exception.code))

    def test_a_task_with_no_plan_is_refused(self) -> None:
        for bad in (SID, 'a/b'):
            with self.subTest(bad=bad):
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                    questions_brief.get_task_questions_answer_brief(bad)
                self.assertEqual(out.getvalue(), '')
if __name__ == '__main__':
    unittest.main(verbosity=2)
