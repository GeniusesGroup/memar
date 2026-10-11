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
                     the project `new` resolves, which is the git top-level
                     else the current folder — asked of a given folder the
                     same way, which `list --project` relies on —
                     and is never overwritten: it is the record the next
                     session continues from.
  ParentLinked       `--parent` records the session a task came from and the
                     first session of its conversation, read off the parent's
                     own plan; a parent that is not there, or the session
                     itself, is refused, and a plan keeps the link it was
                     written with.
  ReportWritten      Beside the plan, `new` writes report.md's skeleton when
                     it is absent and never overwrites one, and prints where
                     it is.
  RoleFoldersMade    Every run makes the module role folders the session
                     folder lacks, and leaves what is in them alone.
  ProjectLocation    A project whose preferences set `sessions` gets its new
                     folders there, relative to its top folder or absolute;
                     with no preferences, an empty key, or a location inside
                     Memar's scratch, the folder is Memar's as before, and
                     for the last `new` says so. The project's top folder or
                     a root is refused, and a location that cannot be made
                     fails with a message, both with nothing made. A name
                     there that is not a session folder is refused and never
                     written into; a new one is made there. A
                     folder there is recorded, continued and linked to from
                     another project, and `new` says each time that it is the
                     project's and never swept; a recorded location that is
                     gone is passed over, and once `gc` has removed it, the
                     next folder made there records it again; a location a
                     `new` records while `gc` prunes is kept. The project is
                     a scratch folder, so a real project's preferences never
                     reach a test.
  BriefPrinted       A session made with --parent ends with the brief that
                     hands it to a sub-agent, its id filled in; one without
                     a parent prints none.
  OpeningRecorded    Opening a folder is one line in the session log, naming
                     the parent when there is one; a folder in a project's
                     own location is recorded in that location's log, not
                     Memar's.
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
import shutil
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
import services.project_preferences as project_preferences
import services.session_new as session_new
from services.module_folders import ROLE_FOLDERS
from services.session_folder import read_session
from services.session_id import is_session_id
from services.session_brief import brief_text
import services.session_location as session_location
from services.session_location import prune_registry, registered_locations
from services.session_log import SESSION_LOG_NAME, log_path
from services.session_plan import PLAN_NAME
from services.session_report import REPORT_NAME

TITLE = "Test the session services"
OPENED = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"
REPORT = "# Report\nStop:\n\n## What ran\n## Check\n## Result\n## Left open\n"
# Kept before any fixture patches it, for the one test that asks git itself.
GIT_PROJECT_ROOT = session_location.project_root


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
        # The project `new` runs in is a scratch folder too, so a real
        # project's preferences never send a test's folder into it.
        self.project = self.fake_root / "project"
        self.project.mkdir()
        self.in_project(self.project)

    def in_project(self, project: Path) -> None:
        patched = unittest.mock.patch.object(session_new, "project_root", return_value=project)
        patched.start()
        self.addCleanup(patched.stop)

    def prefer(self, project: Path, sessions: str) -> None:
        path = project_preferences.preferences_path(project)
        path.parent.mkdir(parents=True, exist_ok=True)
        text = project_preferences.PREFERENCES_TEXT.replace("sessions:\n", f"sessions: {sessions}\n", 1)
        path.write_text(text, encoding="utf-8", newline="\n")

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
                    self.assertEqual(GIT_PROJECT_ROOT(), expected)

    def test_a_folders_project_is_asked_of_git_in_that_folder_else_is_the_folder(self) -> None:
        refused = subprocess.CompletedProcess([], 128, stdout="", stderr="not a git repository")
        with unittest.mock.patch.object(subprocess, "run", return_value=refused) as run:
            self.assertEqual(GIT_PROJECT_ROOT(self.project), self.project.resolve())
        self.assertEqual(run.call_args.args[0][:3], ["git", "-C", str(self.project.resolve())])


class ReportWritten(Fixture):
    def test_a_report_skeleton_is_written_beside_the_plan(self) -> None:
        _, path = session_new.ensure_session("s-report", TITLE)
        raw = (path / REPORT_NAME).read_bytes()
        self.assertNotIn(b"\r", raw)
        self.assertEqual(raw.decode("utf-8"), REPORT)

    def test_a_report_is_never_overwritten_and_one_missing_is_written(self) -> None:
        _, path = session_new.ensure_session("s-report", TITLE)
        report = path / REPORT_NAME
        report.write_text("# Report\nStop: success\n", encoding="utf-8", newline="\n")
        session_new.ensure_session("s-report")
        self.assertEqual(report.read_text(encoding="utf-8"), "# Report\nStop: success\n")
        report.unlink()
        session_new.ensure_session("s-report")
        self.assertEqual(report.read_text(encoding="utf-8"), REPORT)

    def test_new_prints_where_the_report_is(self) -> None:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_new.open_session("s-said", TITLE, None)
        self.assertIn(f"report: {memar_fs.session_dir('s-said') / REPORT_NAME}", out.getvalue())


class RoleFoldersMade(Fixture):
    def test_every_run_makes_the_role_folders_that_are_missing(self) -> None:
        _, path = session_new.ensure_session("s-roles", TITLE)
        self.assertEqual(sorted(entry.name for entry in path.iterdir() if entry.is_dir()), sorted(ROLE_FOLDERS))
        (path / "docs" / "note.md").write_text("# Note\n", encoding="utf-8", newline="\n")
        (path / "rules").rmdir()
        session_new.ensure_session("s-roles")
        self.assertTrue((path / "rules").is_dir())
        self.assertTrue((path / "docs" / "note.md").is_file())


class ProjectLocation(Fixture):
    """A project whose preferences set `sessions` gets its session folders there."""

    def open(self, *arguments) -> tuple[str, Path, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_new.open_session(*arguments)
        printed = out.getvalue()
        sid = re.search(r"session_id: (\S+)", printed).group(1)
        return sid, Path(re.search(r"path: (.+)", printed).group(1).strip()), printed

    def test_without_preferences_or_with_an_empty_key_the_folder_is_memars(self) -> None:
        for prepare in (lambda: None, lambda: self.prefer(self.project, "")):
            with self.subTest(prepare=prepare):
                prepare()
                sid, path, printed = self.open(None, TITLE, None)
                self.assertEqual(path, memar_fs.session_dir(sid))
                self.assertNotIn("location:", printed)
                self.assertEqual(registered_locations(), [])
                self.assertFalse(memar_fs.project_sessions_registry().exists())

    def test_a_relative_location_is_under_the_projects_top_folder(self) -> None:
        self.prefer(self.project, "work/sessions")
        sid, path, printed = self.open(None, TITLE, None)
        location = self.project / "work" / "sessions"
        self.assertEqual(path, location / sid)
        self.assertTrue((path / PLAN_NAME).is_file())
        self.assertTrue((path / REPORT_NAME).is_file())
        self.assertTrue(all((path / role).is_dir() for role in ROLE_FOLDERS))
        self.assertFalse(memar_fs.session_dir(sid).exists())
        self.assertIn(f"location: {location} is a project's own session location", printed)
        self.assertIn("Memar's sweep never moves a folder there", printed)
        self.assertEqual(registered_locations(), [location.resolve()])

    def test_an_absolute_location_is_used_as_it_is(self) -> None:
        elsewhere = self.fake_root / "elsewhere"
        self.prefer(self.project, str(elsewhere))
        sid, path, _ = self.open(None, TITLE, None)
        self.assertEqual(path, elsewhere / sid)

    def test_a_location_inside_memars_scratch_is_memars_own_and_new_says_so(self) -> None:
        self.prefer(self.project, str(memar_fs.sessions_root()))
        sid, path, printed = self.open(None, TITLE, None)
        self.assertEqual(path, memar_fs.session_dir(sid))
        self.assertNotIn("location:", printed)
        said = [line for line in printed.splitlines() if "inside Memar's own temp/" in line]
        self.assertEqual(len(said), 1, printed)
        self.assertIn(str(project_preferences.preferences_path(self.project)), said[0])
        self.assertEqual(registered_locations(), [])

    def test_the_projects_top_folder_or_a_root_is_refused_and_nothing_is_made(self) -> None:
        for value in (".", "work/..", str(self.project), Path(self.project.resolve().anchor).as_posix()):
            with self.subTest(value=value):
                self.prefer(self.project, value)
                before = sorted(entry.name for entry in self.project.iterdir())
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
                    session_new.open_session(None, TITLE, None)
                self.assertIn("`sessions` in", str(raised.exception.code))
                self.assertEqual(sorted(entry.name for entry in self.project.iterdir()), before)
                self.assertEqual(self.minted_folders(), [])
                self.assertFalse(memar_fs.project_sessions_registry().exists())

    def test_an_existing_folder_that_is_not_a_session_is_never_written_into(self) -> None:
        self.prefer(self.project, "work")
        own = self.project / "work" / "src"
        own.mkdir(parents=True)
        (own / "main.kh").write_text("x\n", encoding="utf-8", newline="\n")
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
            session_new.open_session("src", TITLE, None)
        self.assertIn("is not a session folder", str(raised.exception.code))
        self.assertEqual([entry.name for entry in own.iterdir()], ["main.kh"])
        self.assertFalse(memar_fs.session_dir("src").exists())
        self.assertFalse(memar_fs.project_sessions_registry().exists())

    def test_a_new_name_in_the_location_is_still_made_there(self) -> None:
        self.prefer(self.project, "work")
        sid, path, _ = self.open("my-task", TITLE, None)
        self.assertEqual((sid, path), ("my-task", self.project / "work" / "my-task"))
        again, path_again, _ = self.open("my-task", None, None)
        self.assertEqual((again, path_again), (sid, path))

    def test_a_location_that_is_a_file_fails_with_a_message(self) -> None:
        self.prefer(self.project, "work")
        (self.project / "work").write_text("not a folder\n", encoding="utf-8", newline="\n")
        with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as raised:
            session_new.open_session(None, TITLE, None)
        message = str(raised.exception.code)
        self.assertIn("could not be made", message)
        self.assertIn(str(project_preferences.preferences_path(self.project)), message)
        self.assertTrue((self.project / "work").is_file())
        self.assertFalse(memar_fs.project_sessions_registry().exists())

    def test_it_is_continued_and_linked_to_from_another_project_and_says_so_again(self) -> None:
        self.prefer(self.project, "sessions")
        sid, path, _ = self.open(None, TITLE, None)
        other = self.fake_root / "other"
        other.mkdir()
        self.in_project(other)
        again, path_again, printed = self.open(sid, None, None)
        self.assertEqual((again, path_again), (sid, path))
        self.assertIn("location:", printed)
        _, child, _ = self.open(None, "Delegated step", sid)
        self.assertEqual(child, memar_fs.session_dir(child.name))
        self.assertEqual(read_session(child).parent, sid)

    def test_a_location_registered_once_and_gone_is_passed_over(self) -> None:
        self.prefer(self.project, "sessions")
        self.open(None, TITLE, None)
        self.open(None, TITLE, None)
        lines = memar_fs.project_sessions_registry().read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 1)
        gone = memar_fs.project_sessions_registry()
        gone.write_text(lines[0] + "\n" + str(self.fake_root / "unmounted") + "\n", encoding="utf-8", newline="\n")
        self.assertEqual(registered_locations(), [(self.project / "sessions").resolve()])

    def test_a_location_pruned_once_gone_is_recorded_again_when_a_session_is_made_there(self) -> None:
        self.prefer(self.project, "sessions")
        self.open(None, TITLE, None)
        location = (self.project / "sessions").resolve()
        shutil.rmtree(location)
        self.assertEqual(prune_registry(), [location])
        self.assertEqual(memar_fs.project_sessions_registry().read_text(encoding="utf-8"), "")
        self.open(None, TITLE, None)
        self.assertEqual(memar_fs.project_sessions_registry().read_text(encoding="utf-8").splitlines(), [str(location)])

    def test_a_location_appended_while_pruning_is_kept(self) -> None:
        registry = memar_fs.project_sessions_registry()
        registry.parent.mkdir(parents=True, exist_ok=True)
        gone = self.fake_root / "gone"
        registry.write_text(f"{gone}\n", encoding="utf-8", newline="\n")
        appended = self.fake_root / "appended"
        appended.mkdir()
        read = session_location._registry_lines

        def read_then_a_new_appends(path: Path) -> list[str] | None:
            lines = read(path)
            if str(appended) not in registry.read_text(encoding="utf-8"):
                with registry.open("a", encoding="utf-8", newline="\n") as file:
                    file.write(f"{appended}\n")
            return lines

        with unittest.mock.patch.object(session_location, "_registry_lines", side_effect=read_then_a_new_appends):
            self.assertEqual(prune_registry(), [gone])
        self.assertEqual(registry.read_text(encoding="utf-8").splitlines(), [str(appended)])


class BriefPrinted(Fixture):
    def opened(self, *arguments) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_new.open_session(*arguments)
        return out.getvalue()

    def test_a_session_made_with_a_parent_ends_with_its_brief_ready_to_paste(self) -> None:
        session_new.ensure_session("first", TITLE)
        printed = self.opened("second", "Delegated step", "first").splitlines()
        self.assertEqual(printed[-2], "    brief:")
        self.assertEqual(printed[-1], f"        {brief_text('second')}")
        self.assertIn("memar session new --session-id second", printed[-1])

    def test_a_session_made_without_a_parent_prints_no_brief(self) -> None:
        self.assertNotIn("brief:", self.opened("first", TITLE, None))
        self.assertNotIn("brief:", self.opened("first", None, None))


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

    def test_a_session_in_a_project_location_is_recorded_in_that_locations_log(self) -> None:
        self.prefer(self.project, "sessions")
        session_new.ensure_session("first", TITLE)
        _, path = session_new.ensure_session("second", TITLE, parent="first")
        own = (self.project / "sessions" / SESSION_LOG_NAME).read_text(encoding="utf-8").splitlines()
        self.assertEqual([line.split("\t")[1:4] for line in own], [["opened", "first", ""], ["opened", "second", "parent first"]])
        self.assertEqual(log_path(path), path.parent / SESSION_LOG_NAME)
        memars = log_path().read_text(encoding="utf-8") if log_path().is_file() else ""
        self.assertNotIn("\topened\t", memars)


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
