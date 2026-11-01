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
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
adapter = import_module('modules-plugable.knowledge.documentation.services.contents_of_tasks')
task_records = import_module('modules-plugable.management.task.services.task_records')


class ContentsOfTasks(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.elsewhere = self.root / 'memar-tasks'
        self.elsewhere.mkdir()
        patched = unittest.mock.patch.object(task_records, 'tasks_root', return_value=self.elsewhere)
        patched.start()
        self.addCleanup(patched.stop)

    def task(self, task_id: str, *contents: tuple) -> None:
        folder = self.root / '.agents' / 'tasks' / task_id
        folder.mkdir(parents=True)
        (folder / 'task.yaml').write_text('title: t\n', encoding='utf-8', newline='\n')
        for number, text in contents:
            (folder / f'content.{number:05d}.md').write_text(text, encoding='utf-8', newline='\n')

    def test_every_content_of_every_task_is_yielded_with_its_task_id(self) -> None:
        self.task('T-A', (1, '---\nkind: plan\n---\nplan\n'), (2, '---\nkind: changelog\n---\nchange\n'))
        self.task('T-B', (1, '---\nkind: message\n---\nhello\n'))
        found = list(adapter.contents_of_tasks(self.root))
        self.assertEqual([(task, content.number, content.header['kind'], content.body) for task, content in found], [('T-A', 1, 'plan', 'plan\n'), ('T-A', 2, 'changelog', 'change\n'), ('T-B', 1, 'message', 'hello\n')])

    def test_files_that_are_not_contents_are_left_out(self) -> None:
        self.task('T-A', (1, '---\nkind: plan\n---\nplan\n'))
        (self.root / '.agents' / 'tasks' / 'T-A' / 'notes.md').write_text('---\nkind: changelog\n---\nx\n', encoding='utf-8', newline='\n')
        self.assertEqual([content.number for _, content in adapter.contents_of_tasks(self.root)], [1])

    def test_a_project_with_no_task_yields_nothing(self) -> None:
        self.assertEqual(list(adapter.contents_of_tasks(self.root)), [])

    def test_the_notes_of_what_could_not_be_read_are_given_to_the_caller(self) -> None:
        self.task('T-A', (1, '---\nkind: plan\n---\nplan\n'))
        notes: list = []
        list(adapter.contents_of_tasks(self.root, notes))
        self.assertTrue(notes)


if __name__ == '__main__':
    unittest.main(verbosity=2)
