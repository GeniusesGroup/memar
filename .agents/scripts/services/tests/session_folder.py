#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for how a session folder is read in `services/session_folder.py`.

    python .agents/scripts/services/tests/session_folder.py

The subject is the reading every session service shares, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  SessionRead     A folder with no plan, one whose plan cannot be read, and one
                  with a plan are each told apart; a session's conversation is
                  the one its plan records, else the session itself.
  FoldersFound    Only session folders are found, newest first: a minted name,
                  or a plan `new` wrote under any other name (a form minted
                  before among them), listed after every minted one; one an
                  earlier Memar
                  left directly in temp/ is found there, by the list and by
                  its id.
  IdleMeasured    Idle is the latest change anywhere inside, so a file edited
                  deep inside keeps a folder from counting as idle.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import os
import sys
import tempfile
import time
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

import machine.fs_memar as memar_fs
import services.session_folder as session_folder
from services.session_plan import PLAN_NAME, plan_skeleton

OLDEST = "20261001-T000000Z-1"
NEWEST = "20261003-T000000Z-1"
# Names in forms minted before; a folder so named is a session only by its plan.
EARLIER_FORM = "1111-18dc000000000001-0"
EARLIER_DATED = "20261002T000000Z-1-0"
DAY = 24 * 60 * 60


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def session(self, sid: str, plan: str | bytes | None = None) -> Path:
        path = memar_fs.session_dir(sid, create=True)
        if isinstance(plan, bytes):
            (path / PLAN_NAME).write_bytes(plan)
        elif plan is not None:
            (path / PLAN_NAME).write_text(plan, encoding="utf-8", newline="\n")
        return path


class SessionRead(Fixture):
    def test_no_plan_unreadable_and_planned_are_told_apart(self) -> None:
        bare = session_folder.read_session(self.session(OLDEST))
        self.assertEqual((bare.has_plan, bare.readable, bare.status), (False, True, ""))
        broken = session_folder.read_session(self.session(NEWEST, b"\xff\xfe"))
        self.assertEqual((broken.has_plan, broken.readable), (True, False))
        planned = session_folder.read_session(
            self.session(EARLIER_FORM, plan_skeleton("T", "2026-10-01T00:00:00Z", Path("/work")))
        )
        self.assertEqual((planned.has_plan, planned.readable, planned.status), (True, True, "active"))
        self.assertEqual(planned.front["title"], "T")

    def test_the_conversation_is_recorded_else_the_session_itself(self) -> None:
        first = session_folder.read_session(self.session(OLDEST, plan_skeleton("T", "x", Path("/w"))))
        self.assertEqual((first.parent, first.conversation), ("", OLDEST))
        linked = session_folder.read_session(
            self.session(NEWEST, plan_skeleton("T", "x", Path("/w"), parent=OLDEST, conversation=OLDEST))
        )
        self.assertEqual((linked.parent, linked.conversation), (OLDEST, OLDEST))


class FoldersFound(Fixture):
    def test_only_sessions_newest_first(self) -> None:
        for sid in (OLDEST, NEWEST):
            self.session(sid)
        # A name minted before is a session by the plan `new` wrote, and is
        # listed after every minted name; without such a plan it is not one.
        self.session(EARLIER_DATED, plan_skeleton("T", "x", Path("/w")))
        self.session(EARLIER_FORM)
        for name in ("images", "memar-edit-locks", "s-old"):
            (memar_fs.sessions_root() / name).mkdir()
        (memar_fs.sessions_root() / "sessions.log").write_text("", encoding="utf-8")
        self.assertEqual([path.name for path in session_folder.session_folders()], [NEWEST, OLDEST, EARLIER_DATED])

    def test_a_session_left_in_temp_is_found_there_until_it_moves(self) -> None:
        self.session(OLDEST)
        left = memar_fs.scratch_root() / NEWEST
        left.mkdir()
        (memar_fs.scratch_root() / "2024-01-01").mkdir()
        self.assertEqual(session_folder.session_folders(), [left, memar_fs.session_dir(OLDEST)])
        self.assertEqual(session_folder.folder_of(NEWEST), left)
        self.assertEqual(session_folder.folder_of(OLDEST), memar_fs.session_dir(OLDEST))
        self.assertEqual(session_folder.folder_of("2024-01-01"), memar_fs.session_dir("2024-01-01"))
        with self.assertRaises(SystemExit):
            session_folder.folder_of("../elsewhere")

    def test_a_folder_in_temp_is_a_left_session_by_its_name_or_by_a_plan_new_wrote(self) -> None:
        temp = memar_fs.scratch_root()
        named, foreign = temp / "my-work", temp / "notes"
        for folder in (named, foreign):
            folder.mkdir()
        (named / PLAN_NAME).write_text(plan_skeleton("T", "x", Path("/w")), encoding="utf-8", newline="\n")
        (foreign / PLAN_NAME).write_text("# Someone else's plan\n", encoding="utf-8", newline="\n")
        (temp / NEWEST).mkdir()
        self.assertTrue(session_folder.is_left_session(temp / NEWEST))
        self.assertTrue(session_folder.is_left_session(named))
        self.assertFalse(session_folder.is_left_session(foreign))
        self.assertFalse(session_folder.is_left_session(memar_fs.sessions_root()))


class IdleMeasured(Fixture):
    def test_a_file_changed_deep_inside_is_the_latest_change(self) -> None:
        path = self.session(OLDEST)
        (path / "work").mkdir()
        notes = path / "work" / "notes.md"
        notes.write_text("# Notes\n", encoding="utf-8", newline="\n")
        old = time.time() - 9 * DAY
        for entry in (notes, path / "work", path):
            os.utime(entry, (old, old))
        self.assertGreater(session_folder.measured_idle(path), 8.9)
        os.utime(notes, None)
        self.assertLess(session_folder.measured_idle(path), 0.1)

    def test_an_age_that_cannot_be_read_is_none(self) -> None:
        self.assertIsNone(session_folder.measured_idle(self.fake_root / "gone"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
