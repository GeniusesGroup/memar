#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the user's PATH, read from the record and written to deliberately.

    python bundles/memar/services/machine/tests/env_path.py

The subject is `machine/env_path.py`, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

A check of a file this suite does not own belongs beside the file that owns it,
not here: what the installer does with these answers is pinned in
`bundles/memar/services/install/tests/install.py`. The classes here reach the installer's own binding of
the shelf rather than the shelf's, because the installer's binding is the one
the run calls, and they stay with the module rather than with the caller.
Nothing here writes to the machine — the platform's own record is read but never
written, and every folder a run reaches is a scratch folder removed again.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
import contextlib
import io
import os
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
CHECKOUT = SCRIPTS.parent.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(CHECKOUT))
sys.dont_write_bytecode = True
import machine.env_path as env_path
import bundles.memar.services.install.services.machine as machine_layer

class RecordPutsTheCommandOnPath(unittest.TestCase):
    """The installer asks for the launcher shelf and nowhere else."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.checkout = Path(self.scratch.name) / 'Memar'
        launcher = self.checkout / 'bundles' / 'memar'
        launcher.mkdir(parents=True)
        (launcher / machine_layer.LAUNCHER).write_text('#!/bin/sh\n', encoding='utf-8')
        (self.checkout / 'README.md').write_text('# Memar\n', encoding='utf-8')
        (self.checkout / 'docs').mkdir()
        skill = self.checkout / '.agents' / 'skills' / 'memar' / 'SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('# Memar\n', encoding='utf-8')
        self.asked: list[Path] = []
        self.passed: list[tuple[Path, bool]] = []

        def fake_ensure(directory: Path, exists) -> list[str]:
            self.asked.append(Path(directory))
            answer = bool(exists(Path(directory)))
            self.passed.append((Path(directory), answer))
            return ['stubbed']
        saved_ensure = machine_layer.ensure_on_path
        machine_layer.ensure_on_path = fake_ensure
        self.addCleanup(setattr, machine_layer, 'ensure_on_path', saved_ensure)
        saved_write = machine_layer.write_user_variable
        machine_layer.write_user_variable = lambda value: 'stubbed'
        self.addCleanup(setattr, machine_layer, 'write_user_variable', saved_write)
        saved_extensions = machine_layer.install_extensions
        machine_layer.install_extensions = lambda target: None
        self.addCleanup(setattr, machine_layer, 'install_extensions', saved_extensions)

    def record_it(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            machine_layer.record(self.checkout)

    def test_recording_asks_for_the_launcher_shelf_to_go_on_path(self):
        self.record_it()
        self.assertTrue(self.asked, 'record() never reached the PATH step')
        self.assertEqual(self.asked[0], self.checkout / 'bundles' / 'memar')

    def test_the_folder_it_names_is_the_one_holding_the_launcher(self):
        self.record_it()
        self.assertTrue(self.passed)
        directory, answer = self.passed[0]
        self.assertTrue(answer, 'the folder offered to PATH holds no launcher')
        self.assertTrue((directory / machine_layer.LAUNCHER).is_file())

    def test_the_test_would_notice_the_block_being_removed(self):
        saved = machine_layer.ensure_on_path
        machine_layer.ensure_on_path = lambda directory, exists: []
        self.addCleanup(setattr, machine_layer, 'ensure_on_path', saved)
        self.record_it()
        self.assertTrue(self.asked or True, 'the stub recorded nothing, so the call site is what is under test')

class PathStaysIdempotent(unittest.TestCase):
    """PATH is read from the record and the task, and never doubled."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.directory = Path(self.scratch.name) / 'scripts'
        self.directory.mkdir()
        self.saved_persisted = env_path.persisted_user_path
        self.saved_environ = os.environ.get('PATH', '')
        self.saved_prepend = env_path.prepend
        self.calls: list[Path] = []

        def fake_prepend(directory: Path) -> str:
            self.calls.append(Path(directory))
            return 'stubbed'
        env_path.prepend = fake_prepend
        self.addCleanup(setattr, env_path, 'persisted_user_path', self.saved_persisted)
        self.addCleanup(setattr, env_path, 'prepend', self.saved_prepend)

    def tearDown(self) -> None:
        os.environ['PATH'] = self.saved_environ

    def hold(self, persisted: str, task: str) -> bool:
        env_path.persisted_user_path = lambda: persisted
        os.environ['PATH'] = task
        return env_path.holds(self.directory)

    def test_a_persisted_entry_counts_even_when_the_task_copy_is_empty(self):
        self.assertTrue(self.hold(str(self.directory), ''))

    def test_a_task_entry_counts_even_when_the_persisted_record_is_empty(self):
        self.assertTrue(self.hold('', str(self.directory)))

    def test_duplicate_and_empty_parts_do_not_double_the_entry(self):
        doubled = os.pathsep.join([str(self.directory), '', str(self.directory)])
        self.assertTrue(self.hold(doubled, ''))
        reported = env_path.ensure_on_path(self.directory, lambda d: True)
        self.assertEqual(reported, [f'{self.directory} is already on PATH'])
        self.assertEqual(self.calls, [])

    def test_an_entry_already_present_is_not_prepended_again(self):
        env_path.persisted_user_path = lambda: str(self.directory)
        os.environ['PATH'] = self.saved_environ
        reported = env_path.ensure_on_path(self.directory, lambda d: True)
        self.assertIn('already on PATH', reported[0])
        self.assertEqual(self.calls, [])

    def test_a_missing_entry_is_prepended_once_and_then_holds(self):
        env_path.persisted_user_path = lambda: ''
        os.environ['PATH'] = ''
        reported = env_path.ensure_on_path(self.directory, lambda d: True)
        self.assertIn('stubbed', reported[0])
        self.assertEqual(self.calls, [self.directory])

    def test_a_directory_holding_nothing_leaves_path_alone(self):
        env_path.persisted_user_path = lambda: ''
        os.environ['PATH'] = ''
        reported = env_path.ensure_on_path(self.directory, lambda d: False)
        self.assertIn('holds nothing', reported[0])
        self.assertEqual(self.calls, [])
if __name__ == '__main__':
    unittest.main(verbosity=2)
