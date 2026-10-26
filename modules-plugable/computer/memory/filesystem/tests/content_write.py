#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content write` in `modules-plugable/computer/memory/filesystem/services/content_write.py`.

    python modules-plugable/computer/memory/filesystem/tests/content_write.py

The subject is the whole-file write, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the file written, its payload,
and the Memar root the lock lives under are all inside one, made under the
folder `modules-plugable/computer/memory/filesystem/services/fs_test_scratch.py` names, and removed again.

What is pinned, and what each pin is for:

  WriteTakesTheLock   The write takes the per-file lock and leaves an intent
                      note, which is what makes the task tool's claim — that
                      a scratch folder and a lock answer shared-tree collisions
                      — true of the one place a file is actually written; and
                      the bytes written are the ones the flags name.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_fs_test_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_lock = plugable_load('computer.memory.filesystem.services.fs_lock')
fs_lock = _m_fs_lock
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
edit_intent_path = _m_fs_lock.edit_intent_path
edit_lock_path = _m_fs_lock.edit_lock_path
import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
content_write = import_module('modules-plugable.computer.memory.filesystem.services.content_write')

class WriteTakesTheLock(unittest.TestCase):
    """The write verb takes the per-file lock, which is what makes the claim true.

    The task tool states that a scratch folder and a lock answer shared-tree
    collisions. That is only a statement about a writer if the one place a file
    actually gets written takes the lock, and an intent note beside it is what a
    waiter that takes over a stale lock reads to learn what the dead task
    meant.

    Called in-process rather than through a child, because what is under test is
    which function the verb reaches, and a child would answer only that the
    command line works — with the root it resolves on this machine, not the
    scratch one whose locks are then inspected.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.target = self.root / 'notes.md'
        self.target.write_text('# Notes\n', encoding='utf-8', newline='\n')
        self.scratch_root = self.root / 'memar'
        self.scratch_root.mkdir()
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.scratch_root)
        patched.start()
        self.addCleanup(patched.stop)

    def args(self, **overrides) -> Namespace:
        defaults = dict(file=str(self.target), newline=None, create=False, content_file=None)
        defaults.update(overrides)
        return Namespace(**defaults)

    def held_locks(self) -> list[Path]:
        return list((self.scratch_root / 'temp').rglob('*.lock'))

    def test_a_write_takes_the_lock_too(self) -> None:
        taken: list[Path] = []
        saved = fs_lock.edit_task

        def record(target, **keywords):
            taken.append(target)
            return saved(target, **keywords)
        fs_lock.edit_task = record
        self.addCleanup(setattr, fs_lock, 'edit_task', saved)
        new_file = self.root / 'fresh.md'
        payload = self.root / 'payload.md'
        payload.write_text('# Fresh\n', encoding='utf-8', newline='\n')
        content_write.cmd_write(self.args(file=str(new_file), create=True, content_file=str(payload)), self.root)
        self.assertEqual(taken, [new_file])
        self.assertEqual(self.held_locks(), [])

    def test_a_newline_flag_writes_the_line_ending_it_names(self) -> None:
        payload = self.root / 'payload.md'
        payload.write_text('# A\n\nB\n', encoding='utf-8', newline='\n')
        for flag, expected in (('crlf', b'# A\r\n\r\nB\r\n'), ('lf', b'# A\n\nB\n')):
            with self.subTest(flag=flag):
                content_write.cmd_write(self.args(content_file=str(payload), newline=flag), self.root)
                self.assertEqual(self.target.read_bytes(), expected)

    def test_a_write_from_a_content_file_never_reads_stdin(self) -> None:
        payload = self.root / 'payload.md'
        payload.write_text('# From disk\n', encoding='utf-8', newline='\n')
        saved = sys.stdin

        class Closed:

            def read(self) -> str:
                raise AssertionError('stdin was read although the content was on disk')
        sys.stdin = Closed()
        self.addCleanup(setattr, sys, 'stdin', saved)
        content_write.cmd_write(self.args(content_file=str(payload)), self.root)
        self.assertEqual(self.target.read_bytes(), b'# From disk\n')

    def test_the_intent_note_names_this_write_while_the_lock_is_held(self) -> None:
        lock = edit_lock_path(self.target, self.scratch_root / 'temp')
        self.assertTrue(str(lock).endswith('.lock'))
        self.assertEqual(edit_intent_path(lock).name, lock.name + '.intent.json')
        self.assertFalse(lock.exists())
        self.assertFalse(edit_intent_path(lock).exists())

class ScratchBeyondTheArchive(unittest.TestCase):
    """A --content-file lying in a task's kept folders is refused; one in its temp/ is read."""

    def setUp(self) -> None:
        holder = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(holder.cleanup)
        self.task = Path(holder.name) / '20261017-T000000Z-1111'
        for part in ('docs', 'temp'):
            (self.task / part).mkdir(parents=True)
        (self.task / 'plan.md').write_text('---\nTitle: T\n---\n', encoding='utf-8')

    def test_a_file_in_docs_is_refused_and_one_in_temp_is_read(self) -> None:
        kept = self.task / 'docs' / '_draft.md'
        kept.write_text('x', encoding='utf-8')
        with self.assertRaises(SystemExit) as refused:
            content_write.content_from(Namespace(content_file=str(kept)))
        self.assertIn('temp', str(refused.exception))
        scratch = self.task / 'temp' / '_draft.md'
        scratch.write_text('x', encoding='utf-8')
        self.assertEqual(content_write.content_from(Namespace(content_file=str(scratch))), 'x')

    def test_a_file_outside_any_task_is_read(self) -> None:
        outside = self.task.parent / 'note.md'
        outside.write_text('y', encoding='utf-8')
        self.assertEqual(content_write.content_from(Namespace(content_file=str(outside))), 'y')
if __name__ == '__main__':
    unittest.main(verbosity=2)
