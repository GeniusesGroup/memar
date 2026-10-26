#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that `memar view refresh` builds a project's one view from the class its `view` key names.

    python bundles/memar/services/view/tests/refresh.py

The subject is `services/refresh.py`, named for the file that holds it per
[Test Naming](../../../../../modules/process/test/rules/test-naming/test-naming.md). Its expectations are
[Memory View → What a view is](../../../../../modules-plugable/computer/memory/store/view/view.md#what-a-view-is): the verb
opens the class through `open`, builds it with the presentation registered for it, and refuses, building nothing, a
project with no view, a class with no presentation, and a class `open` refuses. The presentation is the test's own; the
Task's is not built yet. The project is a scratch repository whose class is bound to `git-store`, with the user's data
area pointed into the scratch folder, made under the suite's scratch folder (`fs_test_scratch`) and removed after.
"""
from __future__ import annotations
import argparse
import contextlib
import io
import os
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_view = import_module('modules-plugable.computer.memory.store.view.view')
_m_memory = import_module('bundles.memar.services.memory.memory')
_m_refresh = import_module('bundles.memar.services.view.services.refresh')
_m_view_tests = import_module('modules-plugable.computer.memory.store.view.tests.view')
NODE = bytes.fromhex('0190000000007000800000000000000a')

def parse(*words: str) -> tuple[argparse.Namespace, object]:
    """The verb's own parser, as `memar` builds it, and the run it declared."""
    parser = argparse.ArgumentParser(prog='memar view')
    run = _m_refresh.describe(parser.add_subparsers())
    return (parser.parse_args([_m_refresh.COMMAND, *words]), run)

class Refresh(unittest.TestCase):

    def setUp(self) -> None:
        self.folder = _m_scratch.suite_scratch() / f'view-refresh-{uuid.uuid4().hex[:12]}'
        self.folder.mkdir()
        self.saved = {name: os.environ.get(name) for name in ('LOCALAPPDATA', 'XDG_DATA_HOME')}
        os.environ['LOCALAPPDATA'] = os.environ['XDG_DATA_HOME'] = str(self.folder / 'data')
        self.project = _m_view_tests.scratch_repository()
        self.opened: list = []

    def tearDown(self) -> None:
        for each in self.opened:
            each.store.close()
        for name, was in self.saved.items():
            if was is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = was
        _m_scratch.remove_tree(self.project)
        _m_scratch.remove_tree(self.folder)

    def with_block(self, block: str) -> None:
        (self.project / 'manifest.yaml').write_text(block, encoding='utf-8')

    def run_verb(self) -> tuple[int, str]:
        args, run = parse('--project-path', str(self.project))
        said = io.StringIO()
        with contextlib.redirect_stdout(said), contextlib.redirect_stderr(said):
            status = run(args)
        return (status or 0, said.getvalue())

    def test_builds_the_class_the_key_names_with_its_presentation(self) -> None:
        self.with_block('memar:\n  memory: notes=git-store\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        opened = _m_memory.open(self.project, 'notes', _m_record.Needs())
        self.opened.append(opened)
        self.assertEqual(opened.batch([], [(_m_record.key(NODE, 'alpha'), b'alpha\n')]).__class__.__name__, 'Committed')
        status, said = self.run_verb()
        self.assertEqual(status, 0, said)
        self.assertEqual((self.project / 'view' / NODE.hex() / 'alpha.txt').read_bytes(), b'alpha\n')
        self.assertIn('1 file(s) written', said)
        status, said = self.run_verb()
        self.assertEqual(status, 0, said)
        self.assertIn('0 file(s) written', said)

    def test_a_project_without_a_view_is_refused(self) -> None:
        self.with_block('memar:\n  memory: notes=git-store\n')
        status, said = self.run_verb()
        self.assertEqual(status, 1)
        self.assertIn(_m_view.VIEW_KEY, said)
        self.assertFalse((self.project / 'view').exists())

    def test_a_class_without_a_presentation_is_refused(self) -> None:
        self.with_block('memar:\n  memory: unshown=git-store\n  view: unshown=view\n')
        status, said = self.run_verb()
        self.assertEqual(status, 1)
        self.assertIn('presentation', said)
        self.assertFalse((self.project / 'view').exists())

    def test_a_class_open_refuses_is_refused(self) -> None:
        self.with_block('memar:\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        status, said = self.run_verb()
        self.assertEqual(status, 1)
        self.assertIn('bound to no adapter', said)
        self.assertFalse((self.project / 'view').exists())
if __name__ == '__main__':
    unittest.main()
