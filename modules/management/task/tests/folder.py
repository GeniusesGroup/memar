#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for how a task folder is read in `modules/management/task/services/folder.py`.

    python modules/management/task/tests/folder.py

The subject is the reading every task service shares, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `modules-plugable/computer/filesystem/services/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  TaskRead     A folder with no plan, one whose plan cannot be read, and one
                  with a plan are each told apart; a task's conversation is
                  the one its plan records, else the task itself.
  FoldersFound    Only task folders are found, newest first: a minted name,
                  or a plan `ensure` wrote under any other name (a form minted
                  before among them), listed after every minted one; one an
                  earlier Memar
                  left directly in temp/ is found there, by the list and by
                  its id.
  IdleMeasured    Idle is the latest change anywhere inside, so a file edited
                  deep inside keeps a folder from counting as idle.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import os
import sys
import tempfile
import time
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.management.task.services.folder as task_folder
from modules.management.task.services.plan_file import PLAN_NAME, plan_skeleton
OLDEST = '20261001-T000000Z-1'
NEWEST = '20261003-T000000Z-1'
EARLIER_FORM = '1111-18dc000000000001-0'
EARLIER_DATED = '20261002T000000Z-1-0'
DAY = 24 * 60 * 60

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, sid: str, plan: str | bytes | None=None) -> Path:
        path = memar_fs.task_dir(sid, create=True)
        if isinstance(plan, bytes):
            (path / PLAN_NAME).write_bytes(plan)
        elif plan is not None:
            (path / PLAN_NAME).write_text(plan, encoding='utf-8', newline='\n')
        return path

class TaskRead(Fixture):

    def test_no_plan_unreadable_and_planned_are_told_apart(self) -> None:
        bare = task_folder.read_task(self.task(OLDEST))
        self.assertEqual((bare.has_plan, bare.readable, bare.status), (False, True, ''))
        broken = task_folder.read_task(self.task(NEWEST, b'\xff\xfe'))
        self.assertEqual((broken.has_plan, broken.readable), (True, False))
        planned = task_folder.read_task(self.task(EARLIER_FORM, plan_skeleton('20261001T000000Z-1-0', 'T', '2026-10-01T00:00:00Z', Path('/work'))))
        self.assertEqual((planned.has_plan, planned.readable, planned.status), (True, True, 'active'))
        self.assertEqual(planned.front['title'], 'T')

    def test_the_conversation_is_recorded_else_the_task_itself(self) -> None:
        first = task_folder.read_task(self.task(OLDEST, plan_skeleton('20261001T000000Z-1-0', 'T', 'x', Path('/w'))))
        self.assertEqual((first.parent, first.conversation), ('', OLDEST))
        linked = task_folder.read_task(self.task(NEWEST, plan_skeleton('20261001T000000Z-1-0', 'T', 'x', Path('/w'), parent=OLDEST, conversation=OLDEST)))
        self.assertEqual((linked.parent, linked.conversation), (OLDEST, OLDEST))

class FoldersFound(Fixture):

    def test_only_tasks_newest_first(self) -> None:
        for sid in (OLDEST, NEWEST):
            self.task(sid)
        self.task(EARLIER_DATED, plan_skeleton('20261001T000000Z-1-0', 'T', 'x', Path('/w')))
        self.task(EARLIER_FORM)
        for name in ('images', 'memar-edit-locks', 's-old'):
            (memar_fs.tasks_root() / name).mkdir()
        (memar_fs.tasks_root() / 'tasks.log').write_text('', encoding='utf-8')
        self.assertEqual([path.name for path in task_folder.task_folders()], [NEWEST, OLDEST, EARLIER_DATED])

    def test_a_task_left_in_temp_is_not_read(self) -> None:
        self.task(OLDEST)
        left = memar_fs.scratch_root() / NEWEST
        left.mkdir()
        self.assertEqual(task_folder.task_folders(), [memar_fs.task_dir(OLDEST)])
        self.assertEqual(task_folder.folder_of(NEWEST), memar_fs.task_dir(NEWEST))
        self.assertFalse(hasattr(task_folder, 'is_left_task'))
        self.assertFalse(hasattr(task_folder, 'left_folder_of'))
        with self.assertRaises(SystemExit):
            task_folder.folder_of('../elsewhere')

class IdleMeasured(Fixture):

    def test_a_file_changed_deep_inside_is_the_latest_change(self) -> None:
        path = self.task(OLDEST)
        (path / 'work').mkdir()
        notes = path / 'work' / 'notes.md'
        notes.write_text('# Notes\n', encoding='utf-8', newline='\n')
        old = time.time() - 9 * DAY
        for entry in (notes, path / 'work', path):
            os.utime(entry, (old, old))
        self.assertGreater(task_folder.measured_idle(path), 8.9)
        os.utime(notes, None)
        self.assertLess(task_folder.measured_idle(path), 0.1)

    def test_an_age_that_cannot_be_read_is_none(self) -> None:
        self.assertIsNone(task_folder.measured_idle(self.fake_root / 'gone'))
if __name__ == '__main__':
    unittest.main(verbosity=2)
