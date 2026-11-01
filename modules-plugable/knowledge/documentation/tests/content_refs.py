#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
content_refs = import_module('modules-plugable.knowledge.documentation.services.content_refs')
Content = import_module('modules.management.timeline.services.timeline_files').Content


class RefsOf(unittest.TestCase):

    def test_a_content_with_no_refs_refers_to_nothing(self) -> None:
        self.assertEqual(content_refs.refs_of('T-1', Content(2, {'kind': 'report'}, 'x')), set())

    def test_a_timeline_and_number_names_that_timelines_content(self) -> None:
        content = Content(2, {'refs': 'T-9:4'}, 'x')
        self.assertEqual(content_refs.refs_of('T-1', content), {('T-9', 4)})

    def test_a_bare_number_names_a_content_of_the_same_task(self) -> None:
        content = Content(2, {'refs': '1'}, 'x')
        self.assertEqual(content_refs.refs_of('T-1', content), {('T-1', 1)})

    def test_several_refs_are_one_per_line(self) -> None:
        content = Content(5, {'refs': 'T-9:4\nT-1:2\n3'}, 'x')
        self.assertEqual(content_refs.refs_of('T-1', content), {('T-9', 4), ('T-1', 2), ('T-1', 3)})


if __name__ == '__main__':
    unittest.main(verbosity=2)
