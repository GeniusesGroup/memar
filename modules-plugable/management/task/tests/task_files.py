#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the file adapter of a task's contents and facts, `modules-plugable/management/task/services/task_files.py`.

    python modules-plugable/management/task/tests/task_files.py

The subject is the file adapter named by the rule a text of a task is added and never replaced
(`modules-plugable/management/task/rules/a-text-of-a-task-is-added-never-replaced/`), over the stores
of `modules-plugable/management/task/protocol/`.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import os
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
import earlier_shape
BUDGET_SECONDS = 30
files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
errors = import_module('modules-plugable.management.task.errors.errors')
_m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
from modules.knowledge.label.primitive.label import Labels

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name) / 'T-1'
        self.folder.mkdir()

    def made(self) -> None:
        files.create_task(self.folder, 'T-1', 'A: title', None, None, Path('/work'), 'queued', 7, None, None)

class Facts(Fixture):

    def test_a_task_made_new_has_task_yaml_and_no_content_and_no_plan_md(self) -> None:
        self.made()
        self.assertTrue((self.folder / 'task.yaml').is_file())
        self.assertEqual(timeline_files.read_contents(self.folder), [])
        self.assertFalse((self.folder / 'plan.md').exists())

    def test_a_folder_without_task_yaml_is_not_a_task_yet(self) -> None:
        timeline_files.write_content(self.folder, 'plan', 'x\n', 'agent')
        self.assertFalse(files.has_task(self.folder))
        self.assertIsNone(files.read_facts(self.folder))

    def test_the_facts_read_back_as_written_even_with_a_colon_in_the_title(self) -> None:
        self.made()
        facts = files.read_facts(self.folder)
        self.assertEqual(facts['title'], 'A: title')
        self.assertEqual(facts['status'], 'queued')
        self.assertEqual(facts['priority'], '7')

    def test_the_priority_is_replaced_against_the_version_read(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        priority, version = stores.read_priority(None, 'T-1')
        self.assertEqual(priority, 7)
        stores.replace_priority(None, 'T-1', 3, version)
        self.assertEqual(stores.read_priority(None, 'T-1')[0], 3)
        with self.assertRaises(errors.Task_Error_Changed):
            stores.replace_priority(None, 'T-1', 9, version)
        self.assertEqual(stores.read_priority(None, 'T-1')[0], 3)

    def test_changing_one_fact_keeps_the_others_and_a_stale_other_fact_does_not_conflict(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        _, priority_version = stores.read_priority(None, 'T-1')
        _, status_version = stores.read_status(None, 'T-1')
        stores.replace_status(None, 'T-1', 'active', status_version)
        stores.replace_priority(None, 'T-1', 2, priority_version)
        facts = files.read_facts(self.folder)
        self.assertEqual((facts['status'], facts['priority'], facts['title']), ('active', '2', 'A: title'))

    def test_labels_and_depends_on_round_trip(self) -> None:
        self.made()
        stores = files.stores_at(self.folder)
        labels, version = stores.read_labels(None, 'T-1')
        self.assertFalse(labels)
        wanted = Labels.read('implement(01a14a04-6533-7efe-98ac-0e9e47dc1376)')
        stores.replace_labels(None, 'T-1', wanted, version)
        self.assertEqual(list(stores.read_labels(None, 'T-1')[0]), list(wanted))
        cited, version = stores.read_depends_on(None, 'T-1')
        self.assertFalse(cited)

    def test_a_missing_task_is_not_found(self) -> None:
        with self.assertRaises(errors.Task_Error_NotFound):
            files.stores_at(self.folder).read_priority(None, 'T-1')

_m_report_file = import_module('modules-plugable.management.task.services.report_file')

class Reading(Fixture):

    def old(self, status: str = '') -> None:
        earlier_shape.create_plan_md(self.folder, 'T-1', 'Title', None, None, Path('/work'), 'active', None, None, None)
        status_line = f'Status: {status}\n' if status else ''
        (self.folder / 'report.md').write_text(f'---\nID: T-1\nTitle: Title\n{status_line}---\n# Report\n\n## What ran\n## Check\n## Result\n## Left open\n', encoding='utf-8', newline='\n')

    def other(self) -> Path:
        folder = self.folder.parent / 'T-2'
        folder.mkdir()
        files.create_task(folder, 'T-2', 'Title', None, None, Path('/work'), 'active', None, None, None)
        return folder

    def test_a_new_shape_report_has_no_status_channel_and_still_yields_its_body(self) -> None:
        self.made()
        self.assertEqual(_m_report_file.read_report_status(self.folder), '')
        timeline_files.add_text(self.folder, 'report', '# Report\n\n## Decisions needed\n- one\n', 'agent', fields={'status': 'Complete'})
        self.assertEqual(_m_report_file.read_report_status(self.folder), '')
        self.assertEqual(_m_report_file.decisions_needed(self.folder), ['- one'])

    def test_a_report_status_in_the_old_shape_is_read_from_its_front_matter(self) -> None:
        self.old('Complete')
        self.assertEqual(_m_report_file.read_report_status(self.folder), 'complete')

    def test_a_record_is_read_from_the_bytes_of_its_files(self) -> None:
        self.made()
        timeline_files.add_text(self.folder, 'report', '# Report\n', 'agent', fields={'status': 'complete'})
        held = {name: (self.folder / name).read_bytes() for name in files.record_names([p.name for p in self.folder.iterdir()])}
        front, plan_status = files.record_of(held)
        self.assertEqual((front['title'], plan_status), ('A: title', 'queued'))
        self.assertIsNone(files.record_of({'docs/a.md': b'x'}))

    def test_the_project_in_the_facts_is_replaced_by_its_name_and_every_other_byte_kept(self) -> None:
        self.made()
        data = (self.folder / 'task.yaml').read_bytes()
        line = b'project: ' + os.fspath(Path('/work')).encode() + b'\n'
        self.assertIn(line, data)
        named = files.facts_named_project(data, 'memar')
        self.assertEqual(named, data.replace(line, b'project: memar\n'))

if __name__ == '__main__':
    unittest.main()
