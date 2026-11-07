#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import io
import sys
import unittest
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True

BUDGET_SECONDS = 30

Memory = import_module('modules-plugable.management.task.tests.plan_cores').Memory
service = import_module('modules.process.service.service')
composition = import_module('modules.process.services.composition')
faces = import_module('modules-plugable.knowledge.label.status.services.register_services')
SET = import_module('modules-plugable.knowledge.label.status.services.set_status').SERVICE_SET
READ = import_module('modules-plugable.knowledge.label.status.services.read_status').SERVICE_READ


def arguments(service_id: str) -> argparse.Namespace:
    return argparse.Namespace(service_id=service_id, thing='T', word=None, only_from=None)


class Handlers(unittest.TestCase):

    def setUp(self) -> None:
        composition.reset_for_tests()
        self.facts = Memory(status='active')
        self.saved = (faces.is_task_folder, faces.has_plan, faces.stores_at)
        faces.is_task_folder = lambda task: task == 'T'
        faces.has_plan = lambda task: task == 'T'
        faces.stores_at = lambda task: self.facts

    def tearDown(self) -> None:
        faces.is_task_folder, faces.has_plan, faces.stores_at = self.saved
        composition.reset_for_tests()

    def run_service(self, args: argparse.Namespace) -> str:
        out = io.StringIO()
        with redirect_stdout(out):
            service.run(args)
        return out.getvalue()

    def test_set_status_sets_and_prints_the_line(self) -> None:
        said = self.run_service(argparse.Namespace(service_id=SET, thing='T', word='Complete', only_from=None))
        self.assertEqual(said.strip(), 'T  status complete, was active')
        self.assertEqual(self.facts.facts['status'], 'complete')

    def test_read_status_prints_the_status_and_the_allowed_words(self) -> None:
        said = self.run_service(arguments(READ))
        self.assertTrue(said.startswith('T  status active, was active'))
        self.assertIn('Complete', said)
        self.assertEqual(self.facts.writes, [])

    def test_only_from_takes_repeats_and_commas(self) -> None:
        args = argparse.Namespace(service_id=SET, thing='T', word='complete', only_from=['queued,active', 'blocked'])
        self.assertEqual(service._only_from(args), ('queued', 'active', 'blocked'))
        self.assertEqual(self.run_service(args).strip(), 'T  status complete, was active')

    def test_only_from_refuses_when_the_status_is_not_among_them(self) -> None:
        args = argparse.Namespace(service_id=SET, thing='T', word='complete', only_from=['queued'])
        with self.assertRaises(SystemExit):
            self.run_service(args)
        self.assertEqual(self.facts.writes, [])

    def test_a_task_that_is_not_there_is_refused(self) -> None:
        args = argparse.Namespace(service_id=SET, thing='U', word='complete', only_from=None)
        with self.assertRaises(SystemExit) as missing:
            self.run_service(args)
        self.assertIn('no task U', str(missing.exception.code))

    def test_set_status_needs_a_word(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_service(arguments(SET))

    def test_describe_names_both_services_with_their_uuids(self) -> None:
        parser = argparse.ArgumentParser()
        service.describe(parser.add_subparsers())
        sub = parser._subparsers._group_actions[0].choices['service']
        text = sub.description
        self.assertIn(SET, text)
        self.assertIn(READ, text)
        self.assertTrue(any(option.option_strings == ['--only-from'] for option in sub._actions))


if __name__ == '__main__':
    unittest.main()
