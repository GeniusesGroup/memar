#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for where Memar lives on disk in `modules-plugable/computer/filesystem/services/fs_memar.py`.

    python modules-plugable/computer/filesystem/tests/fs_memar.py

The subject is the location surface of `modules-plugable/computer/filesystem/services/fs_memar.py`, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the module that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes to the machine. Roots are patched onto a scratch folder
inside this one; the one test that touches the real checkout only reads
constant properties of it. Task folders are created under a scratch
folder and removed again.

What is pinned, and what each pin is for:

  DefaultLocation    Locks, intents, and task folders default under
                     <memar-root>/temp/, the ONE scratch root, so they can
                     only ever occupy the ignored temp entry and no ignore
                     rule is owed; an unresolvable root errors rather than
                     guessing.
  TaskDir         A task id names one folder segment under the tasks
                     root, .agents/tasks/, and nothing else; anything shaped
                     like a path is refused, and readers never create.
  ProjectTasksRegistry
                     The record of project task locations is Memar's own
                     state, a file beside the task folders, and asking
                     where it is creates nothing.
  ProjectsLog        The registry of projects and their names is a file at the
                     root of temp, not inside the tasks folder, and asking
                     where it is creates nothing but the temp folder.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
REPO = TESTS.parents[3]
SCRIPTS = REPO / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(REPO))
sys.dont_write_bytecode = True

class DefaultLocation(unittest.TestCase):

    def test_scratch_defaults_under_the_memar_temp_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                self.assertEqual(memar_fs.scratch_root(), fake_root / memar_fs.TEMP_DIRNAME)

    def test_recorded_root_wins_over_the_checkout(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'recorded_root', return_value=fake_root):
                self.assertEqual(memar_fs.memar_root(), fake_root)

    def test_checkout_is_used_when_nothing_is_recorded(self) -> None:
        with unittest.mock.patch.object(memar_fs, 'recorded_root', return_value=None):
            with unittest.mock.patch.object(memar_fs, 'is_memar_repository', return_value=True):
                self.assertEqual(memar_fs.memar_root(), memar_fs.checkout_root())

    def test_unresolvable_root_errors_rather_than_guessing(self) -> None:
        with unittest.mock.patch.object(memar_fs, 'recorded_root', return_value=None):
            with unittest.mock.patch.object(memar_fs, 'checkout_root', return_value=Path('/no-such-checkout')):
                with unittest.mock.patch.object(memar_fs, 'is_memar_repository', return_value=False):
                    with self.assertRaises(SystemExit):
                        memar_fs.memar_root()

    def test_checkout_root_is_this_checkout(self) -> None:
        self.assertEqual(memar_fs.checkout_root(), CHECKOUT)

class TaskDir(unittest.TestCase):

    def test_task_dir_is_one_segment_under_the_tasks_root(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                path = memar_fs.task_dir('s-1')
                self.assertEqual(path, fake_root / '.agents' / 'tasks' / 's-1')
                self.assertEqual(path.parent, memar_fs.tasks_root())
                self.assertFalse(path.exists())

    def test_task_dir_creates_only_when_asked(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                path = memar_fs.task_dir('s-2', create=True)
                self.assertTrue(path.is_dir())

    def test_task_dir_refuses_anything_shaped_like_a_path(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                for bad in ('', '.', '..', 'a/b', 'a\\b'):
                    with self.subTest(bad=bad):
                        with self.assertRaises(SystemExit):
                            memar_fs.task_dir(bad)

class ProjectTasksRegistry(unittest.TestCase):

    def test_the_registry_is_memar_state_beside_the_task_folders_and_not_a_task(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                registry = memar_fs.project_tasks_registry()
                self.assertEqual(registry, fake_root / '.agents' / 'tasks' / memar_fs.PROJECT_TASKS_NAME)
                self.assertFalse(registry.exists())

class ProjectsLog(unittest.TestCase):

    def test_the_projects_log_is_at_the_root_of_temp_not_inside_tasks(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            fake_root = Path(scratch)
            with unittest.mock.patch.object(memar_fs, 'memar_root', return_value=fake_root):
                log = memar_fs.projects_log()
                self.assertEqual(log, fake_root / 'temp' / 'projects.log')
                self.assertFalse(log.exists())
                self.assertFalse((fake_root / '.agents' / 'tasks').exists())
if __name__ == '__main__':
    unittest.main(verbosity=2)
