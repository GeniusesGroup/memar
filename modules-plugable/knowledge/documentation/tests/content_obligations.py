#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import argparse
import contextlib
import io
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
verb = import_module('modules-plugable.knowledge.documentation.services.content_list_undischarged_propagations')
task_records = import_module('modules-plugable.management.task.services.task_records')
CHANGELOG = '---\nkind: changelog\n---\n### A change\n- Propagates to:\n  - {artifact}: {state} - why\n'


class ListUndischargedPropagations(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.elsewhere = self.root / 'memar-tasks'
        self.elsewhere.mkdir()
        patched = unittest.mock.patch.object(task_records, 'tasks_root', return_value=self.elsewhere)
        patched.start()
        self.addCleanup(patched.stop)

    def content(self, task_id: str, number: int, artifact: str, state: str) -> None:
        folder = self.root / '.agents' / 'tasks' / task_id
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'task.yaml').write_text('title: t\n', encoding='utf-8', newline='\n')
        (folder / f'content.{number:05d}.md').write_text(CHANGELOG.format(artifact=artifact, state=state), encoding='utf-8', newline='\n')

    def printed(self) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            verb.list_undischarged(self.root)
        return out.getvalue()

    def test_a_pending_item_prints_as_task_number_line_and_item(self) -> None:
        self.content('T-1', 2, 'modeling.md', 'Pending')
        self.assertEqual(self.printed(), 'T-1#2:3: modeling.md: Pending - why\n')

    def test_an_item_closed_by_a_later_content_prints_nothing_outstanding(self) -> None:
        self.content('T-1', 1, 'modeling.md', 'Pending')
        self.content('T-2', 1, 'modeling.md', 'Done')
        self.assertEqual(self.printed(), '(no undischarged propagations)\n')

    def test_the_verb_takes_no_files(self) -> None:
        parser = argparse.ArgumentParser()
        verb.describe(parser.add_subparsers())
        self.assertEqual(vars(parser.parse_args(['list-undischarged-propagations'])), {})

    def test_the_other_verb_is_gone(self) -> None:
        with self.assertRaises(ModuleNotFoundError):
            import_module('modules-plugable.knowledge.documentation.services.content_obligations')


if __name__ == '__main__':
    unittest.main(verbosity=2)
