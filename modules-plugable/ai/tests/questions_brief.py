#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the prompt that hands a task's questions to an agent to answer, in `modules-plugable/ai/services/questions_brief.py`.

    python modules-plugable/ai/tests/questions_brief.py

The subject is the one text a coordinating task hands to an agent that
answers its questions, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneText          The text is one line: it hands over the questions of ID to
                   answer, not its task, names
                   `memar ai get-task-answer-context --task-id ID` as
                   the first command and never `start`, and carries nothing of
                   the questions.
  Printed          It is printed alone for a task with a line under its
                   report's `Decisions needed`; a task with none, or with
                   no plan, has no questions and is refused.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
plan_brief = import_module('modules-plugable.ai.services.get_task_plan_carry_out_brief')
questions_brief = import_module('modules-plugable.ai.services.get_task_questions_answer_brief')
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
PLAN_NAME = _m_plan_file.PLAN_NAME
plan_skeleton = _m_plan_file.plan_skeleton
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
REPORT_NAME = _m_report_file.REPORT_NAME
SID = '20261011-T000000Z-1'
QUESTIONS_BRIEF = f'Your task is to answer the questions of task {SID}, not to take it up. Run `memar ai get-task-answer-context --task-id {SID}` first, before anything else, and follow what it prints.'
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
        (folder / PLAN_NAME).write_text(plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', self.fake_root), encoding='utf-8', newline='\n')
        if report is not None:
            (folder / REPORT_NAME).write_text(report, encoding='utf-8', newline='\n')
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
