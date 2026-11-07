#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the few lines that say what a task came to, in `modules-plugable/knowledge/documentation/report/services/report_summary.py`.

    python modules-plugable/knowledge/documentation/report/tests/report_summary.py

The subject is the summary a day's review shows beside each task, named for
the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

What is pinned, and what each pin is for:

  ResultFirst    The summary is the first lines of the report's Result, the
                 first labelled `result:`; without a Result it is What ran,
                 labelled `ran:`; with neither it says there is no summary.
  Bounded        At most three lines, each cut to a terminal's width.
"""
from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_summary = import_module('modules-plugable.knowledge.documentation.report.services.report_summary')
_tl = import_module('modules.management.timeline.services.timeline_files')

class Fixture(unittest.TestCase):

    def summary(self, report: str | None) -> list[str]:
        with tempfile.TemporaryDirectory(dir=suite_scratch()) as scratch:
            folder = Path(scratch)
            if report is not None:
                _tl.add_text(folder, 'report', report, 'agent')
            return task_summary.summary_lines(folder)

class ResultFirst(Fixture):

    def test_the_result_is_the_summary(self) -> None:
        found = self.summary('# Report\nStop: success\n\n## What ran\nran it\n\n## Result\nOne.\nTwo.\n')
        self.assertEqual(found, ['result: One.', 'Two.'])

    def test_without_a_result_what_ran_is(self) -> None:
        self.assertEqual(self.summary('# Report\nStop: success\n\n## What ran\nran it\n'), ['ran: ran it'])

    def test_with_neither_it_says_there_is_no_summary(self) -> None:
        for report in ('# Report\nStop:\n\n## Result\n\n', None):
            with self.subTest(report=report):
                self.assertTrue(self.summary(report)[0].startswith('no summary:'))

class Bounded(Fixture):

    def test_at_most_three_lines_each_cut_to_the_width(self) -> None:
        long = 'x' * (task_summary.LINE_WIDTH + 10)
        found = self.summary(f'# Report\n\n## Result\n1\n2\n3\n4\n{long}\n')
        self.assertEqual(len(found), 3)
        self.assertTrue(found[0].startswith('result: '))
if __name__ == '__main__':
    unittest.main()
