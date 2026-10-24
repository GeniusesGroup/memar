#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the prompt that hands a task's plan to a sub-agent to carry out, in `modules-plugable/ai/services/plan_brief.py`.

    python modules/management/task/tests/plan_brief.py

The subject is the one text a delegating task hands over, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
That `new --parent` prints it is pinned in `task_new`'s suite.

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneText          The brief is one line holding the task's id and naming
                   `memar ai get-task-init-context --task-id ID` as the first command;
                   it carries nothing of the task itself.
  Printed          `memar ai get-task-plan-carry-out-brief ID` prints
                   that text alone for a task folder that is there with
                   its plan, in Memar's own root or a project's location, and
                   refuses an id with no task folder or shaped like a path,
                   and a folder with no plan.md, naming
                   `new --title T --parent ID` as the way to open one.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[2] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
plan_brief = import_module('modules-plugable.ai.services.get_task_plan_carry_out_brief')
from modules.process.project.services.task_location import register
from modules.management.task.services.plan_file import PLAN_NAME, plan_skeleton
SID = '20261011-T000000Z-1'
BRIEF = f'Your task is task {SID}. Run `memar ai get-task-init-context --task-id {SID}` first, before anything else, and follow what it prints.'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def printed(self, task_id: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            plan_brief.get_task_plan_carry_out_brief(task_id)
        return out.getvalue()

class OneText(Fixture):

    def test_the_brief_is_one_line_naming_the_task_and_nothing_of_its_task(self) -> None:
        self.assertEqual(plan_brief.brief_text(SID), BRIEF)
        self.assertNotIn('\n', plan_brief.brief_text(SID))

class Printed(Fixture):

    def test_it_prints_the_text_alone_for_a_task_that_is_there(self) -> None:
        folder = memar_fs.task_dir(SID, create=True)
        (folder / PLAN_NAME).write_text(plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', self.fake_root), encoding='utf-8', newline='\n')
        self.assertEqual(self.printed(SID), BRIEF + '\n')

    def test_a_task_with_no_plan_is_refused_naming_how_to_open_one(self) -> None:
        memar_fs.task_dir(SID, create=True)
        with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as refused:
            plan_brief.get_task_plan_carry_out_brief(SID)
        self.assertEqual(out.getvalue(), '')
        self.assertIn(f'no task to hand over in {SID}', str(refused.exception.code))
        self.assertIn('`memar task ensure --title T --parent ID --project NAME` (or `--project-path PATH`)', str(refused.exception.code))

    def test_it_finds_a_task_in_a_project_location(self) -> None:
        location = self.fake_root / 'project' / 'tasks'
        folder = location / 'my-task'
        folder.mkdir(parents=True)
        (folder / PLAN_NAME).write_text(plan_skeleton('20261011T000000Z-1-0', 'Named', '2026-10-11T00:00:00Z', self.fake_root / 'project'), encoding='utf-8', newline='\n')
        register(location)
        self.assertEqual(self.printed('my-task'), plan_brief.brief_text('my-task') + '\n')

    def test_an_id_with_no_task_folder_or_shaped_like_a_path_is_refused(self) -> None:
        for bad in (SID, 'a/b', '..'):
            with self.subTest(bad=bad):
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                    plan_brief.get_task_plan_carry_out_brief(bad)
                self.assertEqual(out.getvalue(), '')
if __name__ == '__main__':
    unittest.main(verbosity=2)
