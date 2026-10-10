#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for opening a session in `services/session_new.py`.

    python .agents/scripts/services/tests/session_new.py

The subject is how one session's folder and plan come to exist, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again; session folders, locks, and intent notes land there and are removed
with it. The only subprocess is git's top-level, which writes nothing.

What is pinned, and what each pin is for:

  CreatesFolder      `new` ensures the session's folder and prints its id,
                     path, and plan, so every session works inside its own
                     folder and nothing lands in git by accident; an id shaped
                     like a path is refused.
  RerunIsIdempotent  Reusing one session id keeps the folder as is and reports
                     the same id and path again.
  ContinuedFromTemp  A session an earlier Memar left directly in temp/ is moved
                     as its id continues it, or goes on in temp/ when it cannot
                     move, and no second folder is made beside it; a parent
                     still in temp/ is found there.
  TitleRequired      A folder gets its plan.md from `--title`, so a session is
                     not minted, nor a folder with no plan.md taken up, without
                     one; a folder that has a plan is continued without one.
  PlanWritten        The plan is written in UTF-8 with LF and no BOM, records
                     the project as the git top-level else the current folder,
                     and is never overwritten: it is the record the next
                     session continues from.
  ParentLinked       `--parent` records the session a task came from and the
                     first session of its conversation, read off the parent's
                     own plan; a parent that is not there, or the session
                     itself, is refused, and a plan keeps the link it was
                     written with.
  OpeningRecorded    Opening a folder is one line in the session log, naming
                     the parent when there is one.
  LockSharesTheRoot  Locks and intent notes land under the same temp root the
                     session folders are under. How a lock behaves is pinned in
                     `machine/tests/fs_lock.py`, which owns it.
  UnresolvableRoot   With no root to resolve, opening errors rather than
                     guessing a folder.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import re
import subprocess
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
import services.session_new as session_new
from services.session_folder import read_session
from services.session_id import is_session_id
from services.session_log import log_path
from services.session_plan import PLAN_NAME

TITLE = "Test the session services"
OPENED = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        # One patch, applied once: the locks resolve through the same root
        # lookup the session folders do, so the shared-root claim is proved by
        # pointing at one place rather than by patching it twice.
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def minted_folders(self) -> list[str]:
        root = memar_fs.session_dir("probe").parent
        return [entry.name for entry in root.iterdir() if is_session_id(entry.name)] if root.is_dir() else []


class CreatesFolder(Fixture):
    def test_creates_the_folder_and_returns_its_id_and_path(self) -> None:
        sid, path = session_new.ensure_session("s-1", TITLE)
        self.assertEqual(sid, "s-1")
        self.assertTrue(path.is_dir())
        self.assertEqual(path, memar_fs.session_dir("s-1"))

    def test_open_prints_the_id_path_and_plan(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_new.open_session("s-2", TITLE, None)
        text = out.getvalue()
        path = memar_fs.session_dir("s-2")
        self.assertIn("session_id: s-2", text)
        self.assertIn(f"path: {path}", text)
        self.assertIn(f"plan: {path / PLAN_NAME}", text)

    def test_mints_an_id_when_none_is_given(self) -> None:
        sid, path = session_new.ensure_session(title=TITLE)
        self.assertTrue(is_session_id(sid))
        self.assertEqual(path, memar_fs.session_dir(sid))

    def test_refuses_a_path_as_a_session_id(self) -> None:
        for bad in ("a/b", "a\\b", "..", ".", ""):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    session_new.ensure_session(bad, TITLE)


class RerunIsIdempotent(Fixture):
    def test_rerun_keeps_the_folder_and_reports_the_same_path(self) -> None:
        first_id, first_path = session_new.ensure_session("s-9", TITLE)
        marker = first_path / "notes.md"
        marker.write_text("# Notes\n", encoding="utf-8", newline="\n")
        self.assertEqual(session_new.ensure_session("s-9"), (first_id, first_path))
        self.assertTrue(marker.is_file())


class ContinuedFromTemp(Fixture):
    """A session an earlier Memar left directly in temp/, continued by its id."""

    LEFT = "20261009T120000Z-42-0"

    def left_in_temp(self) -> Path:
        left = memar_fs.scratch_root() / self.LEFT
        left.mkdir()
        (left / PLAN_NAME).write_text("---\ntitle: Old\nopened: x\n---\n# Old\nStatus: open\n", encoding="utf-8", newline="\n")
        return left

    def test_it_is_moved_as_it_is_continued_and_keeps_its_plan(self) -> None:
        left = self.left_in_temp()
        with contextlib.redirect_stderr(io.StringIO()):
            sid, path = session_new.ensure_session(self.LEFT)
        self.assertEqual((sid, path), (self.LEFT, memar_fs.session_dir(self.LEFT)))
        self.assertFalse(left.exists())
        self.assertIn("title: Old", (path / PLAN_NAME).read_text(encoding="utf-8"))

    def test_it_goes_on_in_temp_when_it_cannot_move_and_nothing_is_made_beside_it(self) -> None:
        left = self.left_in_temp()
        refused = PermissionError(13, "The process cannot access the file")
        with unittest.mock.patch("services.session_migrate.os.rename", side_effect=refused), \
                contextlib.redirect_stderr(io.StringIO()):
            sid, path = session_new.ensure_session(self.LEFT, "A new title")
        self.assertEqual((sid, path), (self.LEFT, left))
        self.assertFalse(memar_fs.session_dir(self.LEFT).exists())
        self.assertIn("title: Old", (left / PLAN_NAME).read_text(encoding="utf-8"))

    def test_a_parent_still_in_temp_links_its_child(self) -> None:
        self.left_in_temp()
        with contextlib.redirect_stderr(io.StringIO()):
            _, path = session_new.ensure_session("child", TITLE, parent=self.LEFT)
        self.assertEqual(read_session(path).parent, self.LEFT)
        self.assertTrue((memar_fs.scratch_root() / self.LEFT).is_dir())


class TitleRequired(Fixture):
    def test_a_new_session_needs_a_title(self) -> None:
        for title in (None, "", "   ", "two\nlines"):
            with self.subTest(title=title):
                with self.assertRaises(SystemExit):
                    session_new.ensure_session(title=title)
        self.assertEqual(self.minted_folders(), [])

    def test_a_folder_without_a_plan_needs_a_title(self) -> None:
        bare = memar_fs.session_dir("s-bare", create=True)
        with self.assertRaises(SystemExit):
            session_new.ensure_session("s-bare")
        self.assertFalse((bare / PLAN_NAME).exists())
        session_new.ensure_session("s-bare", TITLE)
        self.assertTrue((bare / PLAN_NAME).is_file())

    def test_a_folder_with_a_plan_is_continued_without_one(self) -> None:
        sid, path = session_new.ensure_session("s-plan", TITLE)
        self.assertEqual(session_new.ensure_session("s-plan"), (sid, path))


class PlanWritten(Fixture):
    def test_the_plan_is_utf8_lf_no_bom_and_names_the_project(self) -> None:
        _, path = session_new.ensure_session("s-plan", TITLE)
        raw = (path / PLAN_NAME).read_bytes()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r", raw)
        text = raw.decode("utf-8")
        title = re.escape(TITLE)
        self.assertRegex(text, rf"\A---\ntitle: {title}\nopened: {OPENED}\nproject: .+\n---\n# {title}\nStatus: open\n")
        project = Path(re.search(r"^project: (.+)$", text, re.MULTILINE).group(1))
        self.assertEqual(project, session_new.project_root())

    def test_continuing_never_overwrites_the_plan(self) -> None:
        sid, path = session_new.ensure_session("s-keep", TITLE)
        plan = path / PLAN_NAME
        kept = plan.read_text(encoding="utf-8").replace("Status: open", "Status: done")
        plan.write_text(kept, encoding="utf-8", newline="\n")
        session_new.ensure_session(sid)
        session_new.ensure_session(sid, "Another title")
        self.assertEqual(plan.read_text(encoding="utf-8"), kept)

    def test_the_project_is_the_git_top_level_else_the_current_folder(self) -> None:
        found = subprocess.CompletedProcess([], 0, stdout=f"{self.fake_root}\n", stderr="")
        refused = subprocess.CompletedProcess([], 128, stdout="", stderr="not a git repository")
        for outcome, expected in (
            ({"return_value": found}, self.fake_root.resolve()),
            ({"return_value": refused}, Path.cwd()),
            ({"side_effect": FileNotFoundError("git")}, Path.cwd()),
        ):
            with self.subTest(expected=expected):
                with unittest.mock.patch.object(subprocess, "run", **outcome):
                    self.assertEqual(session_new.project_root(), expected)


class ParentLinked(Fixture):
    def test_a_session_opened_from_another_records_it_and_the_first_of_the_conversation(self) -> None:
        session_new.ensure_session("first", TITLE)
        _, second = session_new.ensure_session("second", "Second task", parent="first")
        _, third = session_new.ensure_session("third", "Delegated step", parent="second")
        two, three = read_session(second), read_session(third)
        self.assertEqual((two.parent, two.conversation), ("first", "first"))
        self.assertEqual((three.parent, three.conversation), ("second", "first"))

    def test_a_parent_that_is_not_there_or_is_itself_is_refused(self) -> None:
        for sid, parent in (("child", "absent"), ("child", "child"), ("child", "../x")):
            with self.subTest(parent=parent):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        session_new.ensure_session(sid, TITLE, parent=parent)
        self.assertFalse(memar_fs.session_dir("child").exists())

    def test_a_plan_keeps_the_link_it_was_written_with(self) -> None:
        session_new.ensure_session("first", TITLE)
        session_new.ensure_session("other", TITLE)
        session_new.ensure_session("second", TITLE, parent="first")
        self.assertEqual(session_new.ensure_session("second", parent="first")[0], "second")
        with self.assertRaises(SystemExit):
            session_new.ensure_session("second", parent="other")
        self.assertEqual(read_session(memar_fs.session_dir("second")).parent, "first")


class OpeningRecorded(Fixture):
    def test_opening_is_one_log_line_naming_the_parent(self) -> None:
        session_new.ensure_session("first", TITLE)
        session_new.ensure_session("second", TITLE, parent="first")
        session_new.ensure_session("second")
        opened = [line.split("\t")[1:4] for line in log_path().read_text(encoding="utf-8").splitlines()]
        opened = [event for event in opened if event[0] == "opened"]
        self.assertEqual(opened, [["opened", "first", ""], ["opened", "second", "parent first"]])


class LockSharesTheRoot(Fixture):
    def test_a_lock_and_its_intent_note_land_under_the_temp_root(self) -> None:
        target = self.fake_root / "notes.md"
        target.write_text("# Notes\n", encoding="utf-8", newline="\n")
        lock = fs_lock.edit_lock_path(target)
        self.assertEqual(lock.parent, memar_fs.scratch_root() / fs_lock.EDIT_LOCK_DIR_NAME)
        intent = fs_lock.edit_intent_path(lock)
        self.assertEqual(intent.parent, lock.parent)
        self.assertEqual(intent.name, lock.name + ".intent.json")
        _, path = session_new.ensure_session("s-3", TITLE)
        self.assertNotEqual(lock.parent, path)
        self.assertFalse(lock.parent.is_relative_to(path))


class UnresolvableRoot(unittest.TestCase):
    def test_errors_rather_than_guessing(self) -> None:
        with unittest.mock.patch.object(memar_fs, "memar_root", side_effect=SystemExit("error: no root")):
            with self.assertRaises(SystemExit):
                session_new.ensure_session("s-1", TITLE)


if __name__ == "__main__":
    unittest.main(verbosity=2)
