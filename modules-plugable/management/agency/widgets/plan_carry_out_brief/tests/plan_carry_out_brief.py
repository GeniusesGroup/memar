#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for agency Plan_Carry_Out_Brief, realized in
`modules-plugable/management/agency/widgets/plan_carry_out_brief/plan_carry_out_brief.py`.

    python modules-plugable/management/agency/widgets/plan_carry_out_brief/tests/plan_carry_out_brief.py

The stable command face remains `memar agency_get_task_plan_carry_out_brief`.
That `new --parent` prints it is pinned in `task_new`'s suite.

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `modules/process/test/services/test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneText          The brief is one line holding the task's id and naming
                   `memar agency_get_task_init_context --task-id ID` as the first command;
                   it carries nothing of the task itself.
  Printed          The verb prints that text alone for a task that is there with
                   its plan, in Memar's own root or a project's location, and
                   refuses an id with no task or no plan, naming
                   `ensure --title T --parent ID` as the way to open one.

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
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
register = _m_task_location.register
import shape
_m_plan_text = import_module('modules-plugable.knowledge.documentation.plan.services.plan_text')
plan_skeleton = _m_plan_text.plan_skeleton
SID = '20261011-T000000Z-1'
BRIEF = f'Your task is task {SID}. Run `memar agency_get_task_init_context --task-id {SID}` first, before anything else, and follow what it prints. Where Memar\'s MCP tools are listed, call the tool `agency_get_task_init_context` with the same arguments instead of running the command.'

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
        shape.from_plan_text(folder, plan_skeleton('20261011T000000Z-1-0', 'Delegated', '2026-10-11T00:00:00Z', self.fake_root))
        self.assertEqual(self.printed(SID), BRIEF + '\n')

    def test_a_task_with_no_plan_is_refused_naming_how_to_open_one(self) -> None:
        memar_fs.task_dir(SID, create=True)
        with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as refused:
            plan_brief.get_task_plan_carry_out_brief(SID)
        self.assertEqual(out.getvalue(), '')
        self.assertIn(f'no task to hand over in {SID}', str(refused.exception.code))
        self.assertIn('`memar task_ensure --title T --parent ID --project NAME` (or `--project-path PATH`)', str(refused.exception.code))

    def test_it_finds_a_task_in_a_project_location(self) -> None:
        location = self.fake_root / 'project' / 'tasks'
        folder = location / 'my-task'
        folder.mkdir(parents=True)
        shape.from_plan_text(folder, plan_skeleton('20261011T000000Z-1-0', 'Named', '2026-10-11T00:00:00Z', self.fake_root / 'project'))
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
