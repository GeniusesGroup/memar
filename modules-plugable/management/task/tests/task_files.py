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
import stat
import sys
import tempfile
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
files = import_module('modules-plugable.management.task.services.task_files')
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

class Contents(Fixture):

    def test_the_first_content_is_numbered_one_in_five_digits(self) -> None:
        number = files.write_content(self.folder, 'plan', 'hello\n', 'agent')
        self.assertEqual(number, 1)
        self.assertTrue((self.folder / 'content.00001.md').is_file())

    def test_the_header_holds_kind_author_placed_at_follows_refs_and_the_body_is_the_text(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent', placed_at='2026-10-31T00:00:00Z')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1, refs=['a.md'], fields={'type': 'x'})
        second = files.read_contents(self.folder)[1]
        self.assertEqual(second.number, 2)
        self.assertEqual(second.header['kind'], 'plan')
        self.assertEqual(second.header['follows'], '1')
        self.assertEqual(second.header['refs'], 'a.md')
        self.assertEqual(second.header['type'], 'x')
        self.assertEqual(second.header['author'], 'agent')
        self.assertEqual(second.body, 'two\n')

    def test_a_content_is_read_only_and_never_opened_for_writing_again(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        path = self.folder / 'content.00001.md'
        self.assertFalse(os.stat(path).st_mode & stat.S_IWRITE)
        with self.assertRaises(OSError):
            path.open('w')

    def test_numbers_never_repeat_even_when_a_file_is_present_already(self) -> None:
        (self.folder / 'content.00001.md').write_text('---\nkind: plan\n---\nx')
        self.assertEqual(files.write_content(self.folder, 'critique', 'c\n', 'agent'), 2)

    def test_a_write_that_follows_an_older_content_than_the_highest_of_its_kind_is_refused(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1)
        with self.assertRaises(errors.Task_Error_Changed):
            files.write_content(self.folder, 'plan', 'late\n', 'agent', follows=1)
        self.assertEqual([c.number for c in files.read_contents(self.folder)], [1, 2])

    def test_a_content_of_another_kind_does_not_make_a_follow_stale(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        files.write_content(self.folder, 'critique', 'c\n', 'agent')
        self.assertEqual(files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1), 3)

    def test_the_latest_of_a_kind_is_its_highest_number(self) -> None:
        files.write_content(self.folder, 'plan', 'one\n', 'agent')
        files.write_content(self.folder, 'plan', 'two\n', 'agent', follows=1)
        self.assertEqual(files.latest_content(self.folder, 'plan').number, 2)
        self.assertIsNone(files.latest_content(self.folder, 'report'))

    def test_a_content_file_is_recognised_by_name(self) -> None:
        self.assertTrue(files.is_content_file(Path('x/content.00128.md')))
        self.assertFalse(files.is_content_file(Path('x/content.128.md')))
        self.assertFalse(files.is_content_file(Path('x/plan.md')))

class Facts(Fixture):

    def test_a_task_made_new_has_task_yaml_and_two_contents_and_no_plan_md(self) -> None:
        self.made()
        self.assertTrue((self.folder / 'task.yaml').is_file())
        self.assertEqual([c.header['kind'] for c in files.read_contents(self.folder)], ['plan', 'report'])
        self.assertFalse((self.folder / 'plan.md').exists())

    def test_a_folder_without_task_yaml_is_not_a_task_yet(self) -> None:
        files.write_content(self.folder, 'plan', 'x\n', 'agent')
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

class TodaysShape(Fixture):

    def plan(self) -> Path:
        text = _m_plan_file.plan_skeleton('T-1', 'Title', '2026-10-01T00:00:00Z', Path('/work'), priority=4)
        path = self.folder / 'plan.md'
        path.write_text(text, encoding='utf-8', newline='\n')
        return path

    def test_a_plan_md_task_is_read_and_one_field_is_rewritten_with_every_other_line_kept(self) -> None:
        path = self.plan()
        before = path.read_text(encoding='utf-8')
        stores = files.stores_at(self.folder)
        priority, version = stores.read_priority(None, 'T-1')
        self.assertEqual(priority, 4)
        stores.replace_priority(None, 'T-1', 9, version)
        self.assertEqual(path.read_text(encoding='utf-8'), before.replace('Priority: 4', 'Priority: 9'))
        with self.assertRaises(errors.Task_Error_Changed):
            stores.replace_priority(None, 'T-1', 1, version)

    def test_a_status_is_read_and_written_in_the_front_matter(self) -> None:
        path = self.plan()
        stores = files.stores_at(self.folder)
        status, version = stores.read_status(None, 'T-1')
        self.assertEqual(status, 'active')
        stores.replace_status(None, 'T-1', 'queued', version)
        self.assertIn('Status: Queued', path.read_text(encoding='utf-8'))

    def test_creating_a_plan_in_todays_shape_writes_plan_md_and_never_over_one(self) -> None:
        files.create_plan_md(self.folder, 'T-1', 'Title', None, None, Path('/work'), 'active', None, None, None)
        first = (self.folder / 'plan.md').read_text(encoding='utf-8')
        files.create_plan_md(self.folder, 'T-1', 'Other', None, None, Path('/work'), 'active', None, None, None)
        self.assertEqual((self.folder / 'plan.md').read_text(encoding='utf-8'), first)

if __name__ == '__main__':
    unittest.main()
