#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a task's identity in `modules/management/task/primitive/task_id.py`.

    python modules/management/task/tests/task_id.py

The subject is the id a task's folder and intent notes carry, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes anything: an id is minted and read back.

What is pinned, and what each pin is for:

  MintedIdUnique     Two ids minted by one process differ, also within one
                     second, so two tasks opening a shared scratch root
                     cannot land on one folder; the form is the date, a dash,
                     the time, and the process id, so a person reads it and a
                     name sort is creation order; only that form is a task
                     id, so a person's folder named by a date is not one, and
                     neither is a name in a form minted before (a folder so
                     named is a task by its plan, `task_folder`, as
                     long as it keeps that name).

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import os
import sys
import time
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.management.task.primitive.task_id as task_id

class MintedIdUnique(unittest.TestCase):
    """The id a task gets when it does not bring one.

    Minting happens in a module of its own rather than in the task command,
    so a caller that needs an id without running a task can have one; what
    makes it an identity rather than a label is that no two calls agree, which is
    the one property a shared scratch root depends on.
    """

    def test_two_minted_ids_differ_even_within_one_second(self) -> None:
        first, second = (task_id.TaskId.new(), task_id.TaskId.new())
        self.assertNotEqual(first, second)
        self.assertTrue(task_id.TaskId.is_form(first) and task_id.TaskId.is_form(second))

    def test_the_form_is_the_date_a_dash_the_time_and_the_process_id(self) -> None:
        minted = task_id.TaskId.new()
        self.assertRegex(minted, '^\\d{8}-T\\d{6}Z-\\d+$')
        self.assertTrue(minted.startswith(time.strftime('%Y%m%d-T', time.gmtime())))
        self.assertTrue(minted.endswith(f'-{os.getpid()}'))

    def test_a_name_sort_is_creation_order(self) -> None:
        self.assertLess('20261008-T082722Z-99999', '20261008-T082723Z-1')
        self.assertLess('20261008-T235959Z-1', '20261009-T000000Z-1')

    def test_only_the_minted_form_is_a_task_id(self) -> None:
        for name in ('20261013-T190845Z-23368', '20261010-T054304Z-1'):
            with self.subTest(name=name):
                self.assertTrue(task_id.TaskId.is_form(name))
        for name in ('20261013T190845Z-23368-0', '34852-18dc8080b906c944-0', '2024-01-01', '20261013-T190845Z-', '20261013-T190845Z-23368-0', 'repo_tree.md'):
            with self.subTest(name=name):
                self.assertFalse(task_id.TaskId.is_form(name))
if __name__ == '__main__':
    unittest.main(verbosity=2)
