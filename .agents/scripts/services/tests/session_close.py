#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for closing a session in `services/session_close.py`.

    python .agents/scripts/services/tests/session_close.py

The subject is `close`, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder, and nothing reaches the
platform trash: the Memar root is patched onto a scratch folder and the trash
onto a stand-in inside it.

What is pinned, and what each pin is for:

  RecoverableClose  `close` hands the folder to recoverable storage instead of
                    destroying it, so a session closed by mistake costs one trip
                    to the trash; closing again says it is already closed; a
                    trash that fails leaves the folder where it was, because a
                    failed recovery is not a successful close. A session an
                    earlier Memar left in temp/, not moved yet, is closed there.
  OnlyItsFolder     Closing one session's folder reaches nothing beside it, the
                    lock directory included, and is recorded in the log.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_lock as fs_lock
import machine.fs_memar as memar_fs
import machine.fs_trash as fs_trash
import services.session_close as session_close
from services.session_log import log_path


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.bin = self.fake_root / "recycle-bin"
        self.bin.mkdir()

    def move_to_bin(self, source: Path) -> None:
        shutil.move(str(source), str(self.bin / Path(source).name))

    def session(self, sid: str) -> Path:
        path = memar_fs.session_dir(sid, create=True)
        (path / "notes.md").write_text("# Keep me\n", encoding="utf-8", newline="\n")
        return path


class RecoverableClose(Fixture):
    def test_close_moves_the_folder_with_its_contents_to_recoverable_storage(self) -> None:
        path = self.session("s-recover")
        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=self.move_to_bin) as trash:
            self.assertEqual(session_close.close_session("s-recover"), ("s-recover", path, True))
            trash.assert_called_once_with(path)
            self.assertFalse(path.exists())
            self.assertEqual((self.bin / "s-recover" / "notes.md").read_text(encoding="utf-8"), "# Keep me\n")
            self.assertEqual(session_close.close_session("s-recover"), ("s-recover", path, False))
            trash.assert_called_once()

    def test_close_says_what_it_did(self) -> None:
        self.session("s-said")
        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=self.move_to_bin):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                session_close.close("s-said")
                session_close.close("s-said")
        self.assertIn("closed: s-said", out.getvalue())
        self.assertIn("already closed: s-said", out.getvalue())

    def test_failed_trash_leaves_the_folder_in_place(self) -> None:
        path = self.session("s-failed")
        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=OSError("trash unavailable")):
            with self.assertRaises(OSError):
                session_close.close_session("s-failed")
        self.assertTrue(path.is_dir())

    def test_a_session_still_in_temp_is_closed_where_it_is(self) -> None:
        left = memar_fs.scratch_root() / "20261009T120000Z-42-0"
        left.mkdir()
        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=self.move_to_bin) as trash:
            self.assertEqual(session_close.close_session(left.name), (left.name, left, True))
        trash.assert_called_once_with(left)
        self.assertFalse(memar_fs.session_dir(left.name).exists())

    def test_a_path_is_refused_as_an_id(self) -> None:
        for bad in ("a/b", "..", ""):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    session_close.close_session(bad)


class OnlyItsFolder(Fixture):
    def test_closing_leaves_the_lock_root_alone_and_is_recorded(self) -> None:
        path = self.session("s-3")
        lock_dir = memar_fs.scratch_root() / fs_lock.EDIT_LOCK_DIR_NAME
        lock_dir.mkdir()
        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=self.move_to_bin) as trash:
            session_close.close_session("s-3")
        trash.assert_called_once_with(path)
        self.assertTrue(lock_dir.is_dir())
        events = [line.split("\t")[1:3] for line in log_path().read_text(encoding="utf-8").splitlines()]
        self.assertIn(["closed", "s-3"], events)


if __name__ == "__main__":
    unittest.main(verbosity=2)
