#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.path.insert(2, str(TESTS))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
files = import_module('modules-plugable.management.task.services.task_files')
memory = import_module('modules-plugable.management.task.services.task_memory')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
errors = import_module('modules-plugable.management.task.errors.errors')
generation = import_module('modules-plugable.management.task.services.task_generation')
_m_report_file = import_module('modules-plugable.management.task.services.report_file')
import earlier_shape


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)

    def old(self, status: str = '') -> Path:
        folder = self.root / 'T-1'
        folder.mkdir()
        earlier_shape.create_plan_md(folder, 'T-1', 'Title', None, None, Path('/work'), 'active', 7, None, None)
        text = _m_report_file.report_skeleton('T-1', 'Title')
        (folder / 'report.md').write_text(text.replace('Status:\n', f'Status: {status}\n'), encoding='utf-8', newline='\n')
        return folder

    def new(self) -> Path:
        folder = self.root / 'T-2'
        folder.mkdir()
        files.create_task(folder, 'T-2', 'Title', None, None, Path('/work'), 'active', 7, None, None)
        return folder


class Core(Fixture):

    def test_the_core_serves_one_shape_and_holds_no_writer_of_the_other(self) -> None:
        for name in ('is_new', 'create_plan_md', 'create_report_md', '_plan_write', '_plan_read', 'rewrite', 'shape_problem'):
            with self.subTest(name=name):
                self.assertFalse(hasattr(files, name))
        self.assertFalse(hasattr(files.FileTaskStores, 'shape_problem'))


class Reading(Fixture):

    def test_the_paths_of_a_plan_and_a_report_are_the_files_of_the_old_shape_and_the_latest_contents_of_the_new(self) -> None:
        old = self.old()
        self.assertEqual((memory.plan_path(old), memory.report_path(old)), (old / 'plan.md', old / 'report.md'))
        new = self.new()
        timeline_files.add_text(new, 'plan', 'first\n', 'agent')
        timeline_files.add_text(new, 'report', 'done\n', 'agent')
        self.assertEqual((memory.plan_path(new), memory.report_path(new)), (new / 'content.00001.md', new / 'content.00002.md'))

    def test_the_text_of_a_plan_and_a_report_comes_from_the_adapter_for_the_old_and_the_contents_for_the_new(self) -> None:
        old = self.old('Complete')
        self.assertIn('## Request', memory.plan_text(old))
        self.assertTrue(memory.has_report(old))
        new = self.new()
        self.assertFalse(memory.has_report(new))
        timeline_files.add_text(new, 'report', '# Report\n\n## Result\ndone\n', 'agent', fields={'status': 'complete'})
        self.assertEqual(memory.report_text(new), '# Report\n\n## Result\ndone\n')
        self.assertTrue(memory.has_report(new))

    def test_a_task_is_known_by_either_shape_and_a_folder_with_neither_is_not_one(self) -> None:
        empty = self.root / 'E'
        empty.mkdir()
        self.assertEqual((memory.has_task(self.old()), memory.has_task(self.new()), memory.has_task(empty)), (True, True, False))
        self.assertTrue(memory.has_plan(self.root / 'T-1'))

    def test_the_names_a_record_is_read_from_are_the_old_pair_or_the_facts_and_every_content(self) -> None:
        self.assertEqual(memory.record_names(['plan.md', 'report.md', 'docs/a.md']), ['plan.md', 'report.md'])
        self.assertEqual(memory.record_names(['content.00002.md', 'task.yaml', 'content.00001.md', 'docs/a.md']), ['task.yaml', 'content.00001.md', 'content.00002.md'])

    def test_contents_are_accepted_by_a_task_in_the_new_shape_alone(self) -> None:
        self.assertEqual((memory.accepts_contents(self.old()), memory.accepts_contents(self.new())), (False, True))


class Stores(Fixture):

    def test_the_facts_of_an_old_task_are_read_through_the_adapter(self) -> None:
        folder = self.old()
        stores = memory.stores_at(folder)
        self.assertEqual(stores.read_status(None, 'T-1')[0], 'active')
        self.assertEqual(str(stores.read_priority(None, 'T-1')[0]), '7')

    def test_a_write_on_an_old_task_is_refused_with_the_error_of_its_writer(self) -> None:
        folder = self.old()
        stores = memory.stores_at(folder)
        with self.assertRaises(errors.Task_Error_WrittenByPredecessor) as held:
            stores.replace_status(None, 'T-1', 'queued', stores.read_status(None, 'T-1')[1])
        self.assertEqual((held.exception.writer, held.exception.successor), (generation.FIRST_GENERATION_TYPE_UUID, generation.TASK_TYPE_UUID))
        self.assertEqual(stores.read_status(None, 'T-1')[0], 'active')

    def test_a_write_on_a_new_task_is_made(self) -> None:
        folder = self.new()
        stores = memory.stores_at(folder)
        stores.replace_status(None, 'T-2', 'queued', stores.read_status(None, 'T-2')[1])
        self.assertEqual(stores.read_status(None, 'T-2')[0], 'queued')

    def test_a_task_that_is_not_there_is_not_found(self) -> None:
        with self.assertRaises(errors.Task_Error_NotFound):
            memory.stores_at(self.root / 'none').read_status(None, 'none')


if __name__ == '__main__':
    unittest.main()
