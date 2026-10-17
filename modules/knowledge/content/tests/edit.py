#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for `memar content edit` in `modules/knowledge/content/services/edit.py`.

    python modules/knowledge/content/tests/edit.py

The subject is the exact-text replacement, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the file edited and the Memar
root the lock lives under are both inside one, made under the folder
`machine/fs_test_scratch.py` names, and removed again.

What is pinned, and what each pin is for:

  EditTakesTheLock    The read, the match, and the write happen under the
                      per-file lock, the lock is gone once the edit ends, a
                      refused edit changes nothing, and the bytes written are
                      the ones the newline flag names.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
import unittest.mock
from argparse import Namespace
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_lock as fs_lock
import machine.fs_memar as memar_fs
import modules.knowledge.content.services.edit as content_edit


class EditTakesTheLock(unittest.TestCase):
    """The edit verb takes the per-file lock around the read and the write.

    The caller believes the file contains exactly `--old`, and that belief is
    checked against the file as it is at the moment of the write; the lock is
    what keeps the copy read and the bytes written one interval.

    Called in-process rather than through a child, because what is under test is
    which function the verb reaches, and a child would answer only that the
    command line works — with the root it resolves on this machine, not the
    scratch one whose locks are then inspected.
    """

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.target = self.root / "notes.md"
        self.target.write_text("# Notes\n", encoding="utf-8", newline="\n")
        self.scratch_root = self.root / "memar"
        self.scratch_root.mkdir()
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.scratch_root)
        patched.start()
        self.addCleanup(patched.stop)

    def args(self, **overrides) -> Namespace:
        defaults = dict(
            file=str(self.target),
            old=None,
            old_file=None,
            new=None,
            new_file=None,
            all=False,
            newline=None,
        )
        defaults.update(overrides)
        return Namespace(**defaults)

    def held_locks(self) -> list[Path]:
        return list((self.scratch_root / "temp").rglob("*.lock"))

    def test_an_edit_takes_the_lock_around_the_read_and_the_write(self) -> None:
        taken: list[Path] = []
        saved = fs_lock.edit_session

        def record(target, **keywords):
            taken.append(target)
            return saved(target, **keywords)

        fs_lock.edit_session = record
        self.addCleanup(setattr, fs_lock, "edit_session", saved)
        content_edit.cmd_edit(self.args(old="# Notes", new="# Renamed"), self.root)
        self.assertEqual(taken, [self.target])
        self.assertEqual(self.target.read_text(encoding="utf-8"), "# Renamed\n")

    def test_an_edit_leaves_the_lock_behind_it(self) -> None:
        content_edit.cmd_edit(self.args(old="# Notes", new="# Renamed"), self.root)
        self.assertEqual(self.held_locks(), [])

    def test_a_refused_edit_leaves_no_lock_and_no_change(self) -> None:
        with self.assertRaises(SystemExit):
            content_edit.cmd_edit(self.args(old="# Absent", new="x"), self.root)
        self.assertEqual(self.held_locks(), [])
        self.assertEqual(self.target.read_text(encoding="utf-8"), "# Notes\n")

    def test_an_edit_with_a_newline_flag_writes_the_line_ending_it_names(self) -> None:
        self.target.write_text("# Notes\n\nBody\n", encoding="utf-8", newline="\n")
        content_edit.cmd_edit(
            self.args(old="Body", new="Text", newline="crlf"), self.root
        )
        self.assertEqual(self.target.read_bytes(), b"# Notes\r\n\r\nText\r\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
