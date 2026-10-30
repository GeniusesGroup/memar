#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for changing a task's priority, in `modules-plugable/management/task/services/priority.py`.

    python modules-plugable/management/task/tests/priority.py

The subject is `memar task priority ID N` — anyone, a person or an agent,
moving a task up or down the line `claims` takes from — named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The ruling it holds is the owner's of 2026-10-12, recorded in task
20261012T153414Z-28656-0: a priority is 1 to 10, 5 when absent, higher sooner,
and anyone may change it.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  SetPriority     The verb writes N into the task's plan and says what it
                  was and is now, whatever the task's status; the plan's
                  status and the rest of it are kept; N outside 1 to 10, or a
                  task that is not there, is refused and nothing changes.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import contextlib
import io
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_plan = import_module('modules-plugable.management.task.services.plan_file')
task_plan_priority = import_module('modules-plugable.management.task.services.plan_priority')
task_priority = import_module('modules-plugable.management.task.services.priority')
_m_priority = import_module('modules-plugable.knowledge.documentation.plan.primitive.priority')
Priority = _m_priority.Priority

class SetPriority(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=Path(self.scratch.name))
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, sid: str, status: str) -> Path:
        folder = memar_fs.task_dir(sid)
        folder.mkdir(parents=True)
        (folder / task_plan.PLAN_NAME).write_text(f'---\nTitle: T\nStatus: {status.capitalize()}\nOpened: 2026-10-12T00:00:00Z\nProject: P\n---\n# T\n\n## Request\nx\n', encoding='utf-8', newline='\n')
        return folder

    def plan(self, folder: Path) -> task_plan.Plan:
        return task_plan.read_plan(folder / task_plan.PLAN_NAME)

    def test_the_verb_writes_the_priority_and_says_what_it_was(self) -> None:
        for index, status in enumerate(('queued', 'active', 'blocked')):
            with self.subTest(status=status):
                folder = self.task(f'20261012T06000{index}Z-1-0', status)
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    task_priority.set_task_priority(folder.name, '8')
                self.assertIn(f'{folder.name}  priority 8, was 5', out.getvalue())
                plan = self.plan(folder)
                self.assertEqual(Priority.of(plan.front), 8)
                self.assertEqual(plan.status, status)
                self.assertEqual(plan.front['title'], 'T')

    def test_a_priority_outside_1_to_10_or_a_missing_task_is_refused(self) -> None:
        folder = self.task('20261012T060010Z-1-0', 'queued')
        before = (folder / task_plan.PLAN_NAME).read_bytes()
        for value in ('0', '11', 'soon'):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit):
                    task_priority.set_task_priority(folder.name, value)
        self.assertEqual((folder / task_plan.PLAN_NAME).read_bytes(), before)
        with self.assertRaises(SystemExit):
            task_priority.set_task_priority('20261012T060011Z-1-0', '3')
if __name__ == '__main__':
    unittest.main()
