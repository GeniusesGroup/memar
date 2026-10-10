#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for moving session folders into temp/sessions/ in `services/session_migrate.py`.

    python .agents/scripts/services/tests/session_migrate.py

The subject is the one-time move of the folders an earlier Memar left directly
in temp/, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  SessionsMoved     Every folder named as a session, and every folder holding a
                    plan `new` wrote, moves whole into temp/sessions/ with its
                    contents, and each move is printed and logged; the session
                    log and the sweep marker move with them.
  OthersStay        The lock folder, the test scratch, the sessions folder, a
                    folder whose plan.md `new` did not write, files, and links
                    stay where they are.
  Once              The move is recorded once nothing is left, and a later run
                    looks no further; a folder the system refuses is reported
                    and tried again next time; a folder whose name is taken in
                    temp/sessions/ is set beside it, never merged or
                    overwritten, and reported once.
  AtWorkWaits       A folder in which anything changed within a day is left
                    where it is, silently, and the move is not recorded while
                    it is there; once quiet, a later run moves it.
  NoticeLeft        What moved is also left as the once-shown notice the next
                    `memar` command prints; a run that moved nothing leaves none.
  TakenUp           A session continued by its id is moved as it is continued,
                    whatever its age, and goes on in temp/ when the system will
                    not move it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
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
import services.session_migrate as session_migrate
import services.update_daily as update_daily
from services.session_log import SESSION_LOG_NAME, log_path
from services.session_plan import PLAN_NAME, plan_skeleton

DATED = "20261009T120000Z-42-0"
EARLIER_FORM = "1111-18dc000000000001-0"
NAMED = "my-work"
DAY = 24 * 60 * 60


def make_idle(path: Path, days: float) -> None:
    """Set every time inside PATH, and PATH's own, to DAYS ago."""
    when = time.time() - days * DAY
    for entry in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        os.utime(entry, (when, when))
    os.utime(path, (when, when))


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.temp = memar_fs.scratch_root()
        self.sessions = self.temp / memar_fs.SESSIONS_DIRNAME

    def left_session(self, name: str, plan: str | None = None, idle_days: float = 2) -> Path:
        path = self.temp / name
        (path / "work").mkdir(parents=True)
        (path / "work" / "notes.md").write_text("# Notes\n", encoding="utf-8", newline="\n")
        if plan is not None:
            (path / PLAN_NAME).write_text(plan, encoding="utf-8", newline="\n")
        make_idle(path, idle_days)
        return path

    def notice(self) -> str | None:
        return update_daily.take_notice(self.temp / update_daily.UPDATE_DIRNAME)

    def migrate(self) -> str:
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            session_migrate.migrate()
        return err.getvalue()


class SessionsMoved(Fixture):
    def test_session_folders_move_whole_and_each_move_is_printed_and_logged(self) -> None:
        self.left_session(DATED, plan_skeleton("T", "x", Path("/w")))
        self.left_session(EARLIER_FORM)
        self.left_session(NAMED, plan_skeleton("Named", "2026-10-01T00:00:00Z", Path("/w")))
        printed = self.migrate()
        for name in (DATED, EARLIER_FORM, NAMED):
            with self.subTest(name=name):
                self.assertFalse((self.temp / name).exists())
                moved = self.sessions / name
                self.assertEqual((moved / "work" / "notes.md").read_text(encoding="utf-8"), "# Notes\n")
                self.assertIn(f"{name}  ->  {moved}", printed)
        events = [line.split("\t")[1:3] for line in log_path().read_text(encoding="utf-8").splitlines()]
        self.assertEqual(sorted(event[1] for event in events if event[0] == "moved"), sorted((DATED, EARLIER_FORM, NAMED)))

    def test_the_log_and_the_sweep_marker_move_before_the_folders(self) -> None:
        (self.temp / SESSION_LOG_NAME).write_text("2026-10-01T00:00:00+00:00\topened\tx\t\n", encoding="utf-8", newline="\n")
        (self.temp / "sessions.swept").write_text("2026-10-09\n", encoding="utf-8", newline="\n")
        self.left_session(DATED)
        self.migrate()
        self.assertFalse((self.temp / SESSION_LOG_NAME).exists())
        self.assertFalse((self.temp / "sessions.swept").exists())
        log = (self.sessions / SESSION_LOG_NAME).read_text(encoding="utf-8")
        self.assertTrue(log.startswith("2026-10-01T00:00:00+00:00\topened\tx"))
        self.assertIn(f"\tmoved\t{DATED}\t", log)
        self.assertEqual((self.sessions / "sessions.swept").read_text(encoding="utf-8"), "2026-10-09\n")


class OthersStay(Fixture):
    def test_nothing_but_session_folders_moves(self) -> None:
        stays = ["memar-edit-locks", "test-scratch", "images"]
        for name in stays:
            (self.temp / name).mkdir()
        foreign = self.temp / "notes"
        foreign.mkdir()
        (foreign / PLAN_NAME).write_text("# A plan of someone else's\n", encoding="utf-8", newline="\n")
        (self.temp / "20261009T120000Z-1-0.md").write_text("a file\n", encoding="utf-8", newline="\n")
        printed = self.migrate()
        self.assertEqual(printed, "")
        for name in [*stays, "notes", "20261009T120000Z-1-0.md", memar_fs.SESSIONS_DIRNAME]:
            self.assertTrue((self.temp / name).exists(), name)
        self.assertEqual(sorted(path.name for path in self.sessions.iterdir()), [session_migrate.MIGRATED_MARKER_NAME])

    def test_a_link_named_as_a_session_stays(self) -> None:
        target = self.fake_root / "elsewhere"
        target.mkdir()
        link = self.temp / DATED
        try:
            os.symlink(target, link, target_is_directory=True)
        except OSError:
            self.skipTest("this machine does not let a test make a directory link")
        self.migrate()
        self.assertTrue(link.is_symlink())
        self.assertFalse((self.sessions / DATED).exists())


class Once(Fixture):
    def test_a_later_run_looks_no_further(self) -> None:
        self.left_session(DATED)
        self.migrate()
        self.assertTrue((self.sessions / session_migrate.MIGRATED_MARKER_NAME).is_file())
        late = self.left_session(EARLIER_FORM)
        self.assertEqual(self.migrate(), "")
        self.assertTrue(late.is_dir())

    def test_a_name_already_taken_is_set_beside_it_and_reported_once(self) -> None:
        left = self.left_session(DATED)
        (self.sessions / DATED).mkdir(parents=True)
        (self.sessions / DATED / "theirs.md").write_text("theirs\n", encoding="utf-8", newline="\n")
        printed = self.migrate()
        aside = self.sessions / f"{DATED}{session_migrate.SET_ASIDE_SUFFIX}"
        self.assertIn(f"not merged: {left}  ->  {aside}", printed)
        self.assertFalse(left.exists())
        self.assertTrue((aside / "work" / "notes.md").is_file())
        self.assertEqual(sorted(path.name for path in (self.sessions / DATED).iterdir()), ["theirs.md"])
        self.assertTrue((self.sessions / session_migrate.MIGRATED_MARKER_NAME).is_file())
        self.assertIn("compare the two by hand", self.notice())
        self.assertEqual(self.migrate(), "")
        self.assertIsNone(self.notice())

    def test_a_folder_the_system_will_not_move_is_left_and_reported(self) -> None:
        left = self.left_session(DATED)
        refused = PermissionError(13, "The process cannot access the file")
        with unittest.mock.patch.object(session_migrate.os, "rename", side_effect=refused):
            printed = self.migrate()
        self.assertIn("The process cannot access the file", printed)
        self.assertTrue(left.is_dir())
        self.assertFalse((self.sessions / session_migrate.MIGRATED_MARKER_NAME).exists())
        self.assertIn(DATED, self.migrate())
        self.assertTrue((self.sessions / session_migrate.MIGRATED_MARKER_NAME).is_file())


class AtWorkWaits(Fixture):
    def test_a_folder_changed_within_a_day_waits_and_moves_once_quiet(self) -> None:
        quiet = self.left_session(EARLIER_FORM)
        busy = self.left_session(DATED, idle_days=0.5)
        printed = self.migrate()
        self.assertFalse(quiet.exists())
        self.assertTrue((busy / "work" / "notes.md").is_file())
        self.assertNotIn(DATED, printed)
        self.assertFalse((self.sessions / DATED).exists())
        self.assertFalse((self.sessions / session_migrate.MIGRATED_MARKER_NAME).exists())
        make_idle(busy, 1.5)
        self.assertIn(DATED, self.migrate())
        self.assertFalse(busy.exists())
        self.assertTrue((self.sessions / DATED / "work" / "notes.md").is_file())
        self.assertTrue((self.sessions / session_migrate.MIGRATED_MARKER_NAME).is_file())

    def test_one_file_changed_deep_inside_keeps_the_folder_waiting(self) -> None:
        busy = self.left_session(DATED)
        os.utime(busy / "work" / "notes.md", None)
        self.assertEqual(self.migrate(), "")
        self.assertTrue(busy.is_dir())
        self.assertFalse((self.sessions / session_migrate.MIGRATED_MARKER_NAME).exists())


class NoticeLeft(Fixture):
    def test_what_moved_is_left_for_the_next_command_once(self) -> None:
        self.left_session(DATED)
        self.left_session(EARLIER_FORM)
        self.migrate()
        notice = self.notice()
        self.assertIn("2 session folder(s)", notice)
        self.assertIn(str(self.sessions), notice)
        self.assertIn(session_migrate.LIST_HINT, notice)
        self.assertIsNone(self.notice())

    def test_a_later_move_adds_to_a_notice_not_yet_printed(self) -> None:
        self.left_session(DATED)
        busy = self.left_session(EARLIER_FORM, idle_days=0)
        self.migrate()
        make_idle(busy, 2)
        self.migrate()
        self.assertEqual(self.notice().count("1 session folder(s)"), 2)

    def test_a_run_that_moved_nothing_leaves_none(self) -> None:
        self.left_session(DATED, idle_days=0)
        self.migrate()
        self.assertIsNone(self.notice())


class TakenUp(Fixture):
    def test_a_session_at_work_is_moved_as_it_is_continued(self) -> None:
        left = self.left_session(DATED, idle_days=0)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            folder = session_migrate.take_up(DATED)
        self.assertEqual(folder, self.sessions / DATED)
        self.assertFalse(left.exists())
        self.assertTrue((folder / "work" / "notes.md").is_file())
        self.assertIn(f"{left}  ->  {folder}", err.getvalue())

    def test_a_session_the_system_will_not_move_goes_on_in_temp(self) -> None:
        left = self.left_session(DATED, idle_days=0)
        refused = PermissionError(13, "The process cannot access the file")
        with unittest.mock.patch.object(session_migrate.os, "rename", side_effect=refused), \
                contextlib.redirect_stderr(io.StringIO()) as err:
            folder = session_migrate.take_up(DATED)
        self.assertEqual(folder, left)
        self.assertFalse((self.sessions / DATED).exists())
        self.assertIn("goes on in it", err.getvalue())

    def test_nothing_in_temp_is_nothing_to_take_up(self) -> None:
        (self.temp / "notes").mkdir()
        self.assertIsNone(session_migrate.take_up(DATED))
        self.assertIsNone(session_migrate.take_up("notes"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
