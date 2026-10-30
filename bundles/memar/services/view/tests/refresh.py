#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
import ast
import enum
import io
import tokenize
import unittest.mock
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
            each.close()
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
def bare(path):
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

def own_error_types(module):
    return sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and (issubclass(each, (BaseException, enum.Enum)) or 'Refus' in name)))

def errors_module():
    return import_module('bundles.memar.services.view.errors.errors')

class Answers(unittest.TestCase):
    setUp = Refresh.setUp
    tearDown = Refresh.tearDown
    with_block = Refresh.with_block

    def test_the_errors_are_declared_in_the_errors_folder(self) -> None:
        errors = errors_module()
        self.assertEqual([each.name for each in errors.RefreshRefusal], ['NO_PROJECT', 'NO_VIEW', 'NO_PRESENTATION'])
        self.assertTrue(all((each.summary() for each in errors.RefreshRefusal)))
        self.assertEqual(errors.RefreshRefused(errors.RefreshRefusal.NO_VIEW, 'a'), errors.RefreshRefused(errors.RefreshRefusal.NO_VIEW, 'b'))

    def test_refresh_defines_no_error_type_of_its_own(self) -> None:
        self.assertEqual(own_error_types(_m_refresh), [])

    def test_each_refusal_is_answered_by_its_declared_error(self) -> None:
        errors = errors_module()
        view_errors = import_module('modules-plugable.computer.memory.store.view.errors.errors')
        memory_errors = import_module('bundles.memar.services.memory.errors.errors')
        answer = _m_refresh.refresh(None)
        self.assertEqual((type(answer), answer.reason), (errors.RefreshRefused, errors.RefreshRefusal.NO_PROJECT))
        self.with_block('memar:\n  memory: notes=git-store\n')
        answer = _m_refresh.refresh(self.project)
        self.assertEqual((type(answer), answer.reason), (errors.RefreshRefused, errors.RefreshRefusal.NO_VIEW))
        self.with_block('memar:\n  view: one\n')
        self.assertIsInstance(_m_refresh.refresh(self.project), view_errors.BadPreference)
        self.with_block('memar:\n  memory: unshown=git-store\n  view: unshown=view\n')
        answer = _m_refresh.refresh(self.project)
        self.assertEqual((type(answer), answer.reason), (errors.RefreshRefused, errors.RefreshRefusal.NO_PRESENTATION))
        self.with_block('memar:\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        self.assertIsInstance(_m_refresh.refresh(self.project), memory_errors.OpenRefused)

    def test_a_refresh_that_builds_answers_built(self) -> None:
        self.with_block('memar:\n  memory: notes=git-store\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        opened = _m_memory.open(self.project, 'notes', _m_record.Needs())
        self.opened.append(opened)
        opened.batch([], [(_m_record.key(NODE, 'alpha'), b'alpha\n')])
        answer = _m_refresh.refresh(self.project)
        self.assertIsInstance(answer, _m_view.Built)
        self.assertEqual(answer.written, 1)

class Closes(unittest.TestCase):
    setUp = Refresh.setUp
    tearDown = Refresh.tearDown
    with_block = Refresh.with_block

    def closing(self):
        return unittest.mock.patch.object(_m_record.Record, 'close', autospec=True, side_effect=_m_record.Record.close)

    def test_a_refresh_closes_the_class_it_opened(self) -> None:
        self.with_block('memar:\n  memory: notes=git-store\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        with self.closing() as closed:
            self.assertIsInstance(_m_refresh.refresh(self.project), _m_view.Built)
        self.assertEqual(closed.call_count, 1)

    def test_a_refused_build_closes_it_too(self) -> None:
        self.with_block('memar:\n  memory: notes=git-store\n  view: notes=view\n')
        _m_view.register('notes', _m_view_tests.present)
        (self.project / 'view').mkdir()
        (self.project / 'view' / 'foreign.txt').write_bytes(b'mine')
        with self.closing() as closed:
            self.assertIsInstance(_m_refresh.refresh(self.project), _m_view.ViewRefused)
        self.assertEqual(closed.call_count, 1)

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        for path in (_m_refresh.__file__, errors_module().__file__, import_module('bundles.memar.services.view.view').__file__, __file__):
            with self.subTest(path=Path(path).name):
                self.assertEqual(bare(path), ([], []))
if __name__ == '__main__':
    unittest.main()
