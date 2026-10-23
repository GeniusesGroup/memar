#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the day a review is asked for, in `modules/management/task/services/day.py`.

    python modules/management/task/tests/day.py

The subject is how a day is named on the command line and which day a task
belongs to, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The expectations are those of task 20261012T163252Z-11472-0: the owner asks
for "only today".

What is pinned, and what each pin is for:

  DayNamed       `today`, `yesterday`, and an ISO date `YYYY-MM-DD` name a
                 day, in any case; anything else is refused, saying what is
                 accepted, since a guessed day would review the wrong tasks.
  DayOfTask   A task belongs to the local day of the latest change
                 anywhere in its folder: a task opened yesterday and
                 finished today is today's. A folder that cannot be read
                 belongs to no day.
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
from datetime import date, timedelta
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parents[3] / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
import modules.management.task.services.day as task_day

class DayNamed(unittest.TestCase):

    def test_today_yesterday_and_a_date_name_a_day(self) -> None:
        today = date(2026, 10, 13)
        self.assertEqual(task_day.parse_day('today', today), today)
        self.assertEqual(task_day.parse_day('Yesterday', today), today - timedelta(days=1))
        self.assertEqual(task_day.parse_day('2026-10-01', today), date(2026, 10, 1))

    def test_anything_else_is_refused_saying_what_is_accepted(self) -> None:
        for text in ('lately', '2026-13-01', '13/10/2026', ''):
            with self.subTest(text=text), self.assertRaises(SystemExit):
                task_day.parse_day(text, date(2026, 10, 13))

class DayOfTask(unittest.TestCase):

    def test_a_task_belongs_to_the_day_of_its_latest_change(self) -> None:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            folder = Path(scratch)
            note = folder / 'note.md'
            note.write_text('x', encoding='utf-8')
            earlier = time.time() - 5 * 24 * 60 * 60
            os.utime(folder, (earlier, earlier))
            self.assertEqual(task_day.day_of(folder), date.today())
            os.utime(note, (earlier, earlier))
            self.assertEqual(task_day.day_of(folder), date.fromtimestamp(earlier))

    def test_a_folder_that_cannot_be_read_belongs_to_no_day(self) -> None:
        self.assertIsNone(task_day.day_of(Path('this') / 'does' / 'not' / 'exist'))
if __name__ == '__main__':
    unittest.main()
