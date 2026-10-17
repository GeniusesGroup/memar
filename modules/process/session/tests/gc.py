#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the sweep in `modules/process/session/services/gc.py`.

    python modules/process/session/tests/gc.py

The subject is how idle finished session folders leave, named for the file
that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder, and nothing reaches the
platform trash: the Memar root is patched onto a scratch folder and the trash
onto a stand-in that records what it was handed and removes it there.

What is pinned, and what each pin is for:

  IdleSessionsReaped  The sweep moves to the trash every session folder nothing
                      inside has changed in for the idle limit, so no session
                      has to spend a message asking for its own close; only
                      folders named as sessions, never the one being opened or
                      continued, and never one whose status is not done: idle
                      is not finished. The test is done, not not-open — a
                      status the sweep does not know, none, or a plan that
                      cannot be read is not done, while a free-text status
                      starting with done or complete is; a plan of the earlier
                      sectioned form is judged by the status read off its
                      tasks, and one with no status there is kept. The
                      limit is `SESSION_IDLE_DAYS` in the file. The caller is
                      not told what was reaped, and a folder that will not go
                      stops nothing.
  SweptOnceADay       Only the first sweep of a day walks the folders; every
                      later one that day reads one small file and stops.
  LogTrimmed          Each day's sweep is one log line, a reap is recorded with
                      how long it was idle, and lines older than four idle
                      limits leave the log for the trash.
  GcSweepsNow         `gc` is the same sweep without the daily guard, and the
                      one `new` runs; it says what it moved and which idle
                      folders it kept, with why and their age; never the
                      caller's own; never under a day.
  ProjectLocationsNotSwept
                      A folder in a project's own session location is never
                      swept, daily or by `gc`, however idle and done: it is
                      the project's. `gc` names each recorded location it did
                      not sweep, and none when none is recorded; it removes
                      from the record each location that is gone and names
                      it, which the daily sweep does not. A project's own
                      log is never trimmed.
  RecordsAddedBeforeTheFolderGoes
                      The sweep is the one act that adds a session's records
                      itself: before it moves a finished folder, whatever of
                      its records the project's records branch does not hold
                      is added, all the sweep's sessions in one commit
                      (`session_archive`); a folder whose records cannot be
                      kept is not moved, and `gc` lists it with why. A session
                      whose plan or report Status is Queued is never swept.
                      Every other class stands in for the keeping with one
                      that owes nothing, so each pins the sweep alone.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import unittest.mock
from datetime import datetime, timedelta, timezone
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

import machine.fs_memar as memar_fs
import machine.fs_trash as fs_trash
import modules.process.project.services.registry as project_registry
import modules.process.session.services.archive as session_archive
import modules.process.session.services.gc as session_gc
import modules.process.session.services.ensure as session_ensure
import modules.knowledge.documentation.plan.services.plan as session_plan
from modules.process.session.services.location import register, registered_locations
from modules.process.session.services.log import SESSION_LOG_NAME, log_path
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, plan_skeleton

DAY = 24 * 60 * 60
# Ids in the forms the id module mints, so the sweep recognizes them as sessions.
IDLE = "20261001-T000000Z-1111"
OTHER = "20261002-T000000Z-2222"
THIRD = "20261003-T000000Z-3333"


def make_idle(path: Path, days: float) -> None:
    """Set every time inside PATH, and PATH's own, to DAYS ago."""
    when = time.time() - days * DAY
    for entry in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        os.utime(entry, (when, when))
    os.utime(path, (when, when))


def plan(status: str) -> str:
    """A plan with STATUS in today's shape (PascalCase keys, Status in the front matter)."""
    return plan_skeleton("20261001T000000Z-1-0", "Work", "2026-10-01T00:00:00Z", Path("/work")).replace("Status: Active", f"Status: {status}", 1)


def earlier_plan(status: str) -> str:
    """A plan in the shape written before: lower-case keys, `Status:` in the body."""
    return f"---\ntitle: Work\nopened: 2026-10-01T00:00:00Z\nproject: /work\n---\n# Work\nStatus: {status}\n\n## Request\n"


class Fixture(unittest.TestCase):
    """A scratch root with session folders of chosen ages and a stand-in trash."""

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.trashed: list[Path] = []

        def move_aside(path: Path) -> None:
            self.trashed.append(Path(path))
            if Path(path).is_dir():
                shutil.rmtree(path)
            else:
                Path(path).unlink()

        self.trash = unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=move_aside)
        self.trash.start()
        self.addCleanup(self.trash.stop)
        # `new` asks the project it runs in where to put a folder; a scratch
        # one, so a real project's preferences never reach this suite.
        project = unittest.mock.patch.object(session_ensure, "project_root", return_value=self.fake_root)
        project.start()
        self.addCleanup(project.stop)
        # The plans here name /work, a project on no computer; keeping records
        # is pinned in RecordsAddedBeforeTheFolderGoes, which stops this stand-in.
        self.keeping = unittest.mock.patch.object(
            session_gc,
            "keep_records",
            side_effect=lambda folders, **_: [
                session_archive.Kept(session_archive.Outcome.NOT_OWED, None, "a stand-in") for _ in folders
            ],
        )
        self.keeping.start()
        self.addCleanup(self.keeping.stop)

    def folder(self, name: str, idle_days: float, *, status: str | None = None, recent_file: bool = False) -> Path:
        path = memar_fs.session_dir(name, create=True)
        (path / "work").mkdir()
        (path / "work" / "notes.md").write_text("# Notes\n", encoding="utf-8", newline="\n")
        if status is not None:
            (path / PLAN_NAME).write_text(plan(status), encoding="utf-8", newline="\n")
        make_idle(path, idle_days)
        if recent_file:
            os.utime(path / "work" / "notes.md", None)
        return path

    def daily(self, keep: str = "s-new", *, new_day: bool = True) -> str:
        """The daily sweep, as `new` runs it; returns what it printed."""
        if new_day:
            (memar_fs.sessions_root() / session_gc.SWEPT_MARKER_NAME).unlink(missing_ok=True)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            session_gc.reap_once_a_day(keep)
        return out.getvalue()

    def run_gc(self, keep: str | None = None, idle_days: float | None = None) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            session_gc.collect(keep, idle_days)
        return out.getvalue()

    def events(self) -> list[list[str]]:
        return [line.split("\t")[1:4] for line in log_path().read_text(encoding="utf-8").splitlines()]


class IdleSessionsReaped(Fixture):
    def test_a_session_idle_past_the_limit_goes_to_the_trash(self) -> None:
        idle = self.folder(IDLE, 8)
        self.daily()
        self.assertEqual(self.trashed, [idle])

    def test_a_session_inside_the_limit_is_kept(self) -> None:
        kept = self.folder(IDLE, 0.5)
        self.daily()
        self.assertEqual(self.trashed, [])
        self.assertTrue(kept.is_dir())

    def test_a_file_changed_deep_inside_keeps_the_session(self) -> None:
        self.folder(IDLE, 8, recent_file=True)
        self.daily()
        self.assertEqual(self.trashed, [])

    def test_only_folders_named_as_sessions_are_reaped(self) -> None:
        for name in ("images", "memar-edit-locks", "s-old"):
            self.folder(name, 30)
        self.daily()
        self.assertEqual(self.trashed, [])

    def test_a_session_whose_status_is_not_done_is_kept(self) -> None:
        # Idle says the task has not been touched, not that it is finished, and
        # a status the vocabulary may gain tomorrow, or none, is not done.
        for index, status in enumerate(("active", "blocked", "archived", ""), start=1):
            with self.subTest(status=status):
                kept = self.folder(f"2026100{index}-T000000Z-4444", 8, status=status or "active")
                if not status:
                    text = (kept / PLAN_NAME).read_text(encoding="utf-8").replace("Status: active\n", "")
                    (kept / PLAN_NAME).write_text(text, encoding="utf-8", newline="\n")
                    make_idle(kept, 8)
                self.daily()
                self.assertEqual(self.trashed, [])
                self.assertTrue(kept.is_dir())

    def test_a_plan_that_cannot_be_read_is_kept(self) -> None:
        kept = self.folder(IDLE, 8)
        (kept / PLAN_NAME).write_bytes(b"---\ntitle: \xff\xfe broken\n---\n")
        make_idle(kept, 8)
        self.daily()
        self.assertEqual(self.trashed, [])

    def test_a_plan_in_an_earlier_shape_is_kept_and_gc_names_it_with_where_todays_shape_is_shown(self) -> None:
        sectioned = "---\nTitle: Old\n---\n# Old\n\n## Did it\nStatus: done\n\n### Request\n"
        shapes = {"sectioned": sectioned, "body status": earlier_plan("complete"), "old word": plan("done")}
        for index, (name, shape) in enumerate(shapes.items(), start=1):
            with self.subTest(shape=name):
                kept = self.folder(f"2026100{index}-T000000Z-6666", 8)
                (kept / PLAN_NAME).write_text(shape, encoding="utf-8", newline="\n")
                make_idle(kept, 8)
                self.daily()
                self.assertEqual(self.trashed, [])
                self.assertTrue(kept.is_dir())
        printed = self.run_gc()
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, printed)

    def test_a_plan_whose_status_cannot_be_read_is_kept(self) -> None:
        # A status written anywhere but under its heading is not read, and a
        # status not read is not known to be done.
        for index, text in enumerate(
            (
                "---\ntitle: Old\n---\n# Old\n\n## Do it\n\n### Request\nStatus: done\n",
                "---\ntitle: Old\n---\n# Old\nNo status at all.\n",
            ),
            start=1,
        ):
            with self.subTest(text=text):
                kept = self.folder(f"2026100{index}-T000000Z-5555", 8)
                (kept / PLAN_NAME).write_text(text, encoding="utf-8", newline="\n")
                make_idle(kept, 8)
                self.daily()
                self.assertEqual(self.trashed, [])
                self.assertTrue(kept.is_dir())

    def test_a_session_whose_status_is_complete_is_reaped(self) -> None:
        gone = self.folder(IDLE, 8, status="complete")
        self.daily()
        self.assertEqual(self.trashed, [gone])

    def test_a_session_whose_status_is_complete_in_the_front_matter_is_reaped_and_an_active_one_kept(self) -> None:
        gone = self.folder(IDLE, 8)
        (gone / PLAN_NAME).write_text(plan("Complete"), encoding="utf-8", newline="\n")
        make_idle(gone, 8)
        kept = self.folder(OTHER, 8)
        (kept / PLAN_NAME).write_text(plan("Active"), encoding="utf-8", newline="\n")
        make_idle(kept, 8)
        self.daily()
        self.assertEqual(self.trashed, [gone])
        self.assertTrue(kept.is_dir())

    def test_only_the_word_complete_is_finished_so_free_text_and_done_are_kept(self) -> None:
        kept = self.folder(IDLE, 8, status="Complete (2026-10-09 14:00, merged)")
        also = self.folder(OTHER, 8, status="incomplete")
        self.daily()
        self.assertEqual(self.trashed, [])
        self.assertTrue(kept.is_dir() and also.is_dir())

    def test_the_session_being_opened_or_continued_is_never_reaped(self) -> None:
        self.folder(IDLE, 30, status="complete")
        self.daily(keep=IDLE)
        self.assertEqual(self.trashed, [])

    def test_the_limit_is_the_number_in_the_file(self) -> None:
        self.assertEqual(session_gc.SESSION_IDLE_DAYS, 1)
        self.assertNotIn("os.environ", Path(session_gc.__file__).read_text(encoding="utf-8"))
        with unittest.mock.patch.object(session_gc, "SESSION_IDLE_DAYS", 10):
            self.folder(IDLE, 8)
            older = self.folder(OTHER, 11)
            self.daily()
        self.assertEqual(self.trashed, [older])

    def test_the_caller_is_not_told_what_was_reaped(self) -> None:
        self.folder(IDLE, 8)
        printed = self.daily()
        self.assertEqual(len(self.trashed), 1)
        self.assertNotIn(IDLE, printed)

    def test_a_folder_that_will_not_go_stops_nothing(self) -> None:
        stuck = self.folder(IDLE, 8)
        idle = self.folder(OTHER, 8)
        self.trash.stop()

        def refuse_one(path: Path) -> None:
            if Path(path) == stuck:
                raise SystemExit(f"error: Recycle Bin move failed: {path}")
            self.trashed.append(Path(path))
            shutil.rmtree(path)

        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=refuse_one):
            self.daily()
        self.trash.start()
        self.assertEqual(self.trashed, [idle])
        self.assertTrue(stuck.is_dir())


class SweptOnceADay(Fixture):
    def test_a_later_sweep_on_the_same_day_walks_nothing(self) -> None:
        self.daily()
        idle = self.folder(IDLE, 8)
        with unittest.mock.patch.object(session_gc, "last_change") as walked:
            self.daily(new_day=False)
        walked.assert_not_called()
        self.assertTrue(idle.is_dir())

    def test_the_first_sweep_of_the_next_day_sweeps_again(self) -> None:
        self.daily()
        idle = self.folder(IDLE, 8)
        marker = memar_fs.sessions_root() / session_gc.SWEPT_MARKER_NAME
        marker.write_text("2000-01-01\n", encoding="utf-8", newline="\n")
        self.daily(new_day=False)
        self.assertEqual(self.trashed, [idle])
        self.assertNotEqual(marker.read_text(encoding="utf-8"), "2000-01-01\n")


class LogTrimmed(Fixture):
    def test_each_days_sweep_is_recorded_once_and_a_reap_with_its_idle_time(self) -> None:
        self.folder(IDLE, 8)
        self.daily()
        self.daily(new_day=False)
        events = self.events()
        self.assertEqual([event[0] for event in events if event[0] == "swept"], ["swept"])
        reaped = [event for event in events if event[:2] == ["reaped", IDLE]]
        self.assertEqual(len(reaped), 1)
        self.assertIn("idle", reaped[0][2])

    def test_old_lines_leave_the_log_for_the_trash(self) -> None:
        self.assertEqual(session_gc.LOG_KEEP_DAYS, 28)
        now = datetime.now(timezone.utc)
        old = (now - timedelta(days=session_gc.LOG_KEEP_DAYS + 1)).isoformat(timespec="seconds")
        recent = (now - timedelta(days=1)).isoformat(timespec="seconds")
        log = log_path()
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text(f"{old}\topened\t{IDLE}\t\n{recent}\topened\t{OTHER}\t\nnot a record\n", encoding="utf-8", newline="\n")
        moved: list[str] = []
        self.trash.stop()

        def keep_what_was_moved(path: Path) -> None:
            if Path(path).is_file():
                moved.append(Path(path).read_text(encoding="utf-8"))
                Path(path).unlink()

        with unittest.mock.patch.object(fs_trash, "soft_delete", side_effect=keep_what_was_moved):
            self.daily()
        self.trash.start()
        self.assertEqual(moved, [f"{old}\topened\t{IDLE}\t\n"])
        text = log.read_text(encoding="utf-8")
        self.assertNotIn(old, text)
        self.assertIn(f"{recent}\topened\t{OTHER}", text)
        self.assertIn("not a record", text)


class GcSweepsNow(Fixture):
    def test_gc_sweeps_even_after_todays_sweep_and_says_what_it_moved(self) -> None:
        self.daily()
        gone = self.folder(IDLE, 8, status="complete")
        printed = self.run_gc()
        self.assertEqual(self.trashed, [gone])
        self.assertIn(f"moved to the recycle bin: {IDLE}  idle 8.0 days", printed)

    def test_gc_is_the_same_sweep_new_runs_once_a_day(self) -> None:
        with unittest.mock.patch.object(session_gc, "reap_idle_sessions", wraps=session_gc.reap_idle_sessions) as sweep:
            with contextlib.redirect_stdout(io.StringIO()):
                session_ensure.ensure_session("s-new", "Open one", project=str(self.fake_root))
                self.run_gc()
        self.assertEqual(sweep.call_count, 2)

    def test_gc_lists_the_idle_folders_kept_for_unfinished_work(self) -> None:
        self.folder(IDLE, 12, status="blocked")
        unreadable = self.folder(OTHER, 9)
        (unreadable / PLAN_NAME).write_bytes(b"\xff\xfe")
        make_idle(unreadable, 9)
        unstated = self.folder(THIRD, 10)
        (unstated / PLAN_NAME).write_text("---\nTitle: Old\n---\n# Old\n", encoding="utf-8", newline="\n")
        make_idle(unstated, 10)
        printed = self.run_gc()
        self.assertEqual(self.trashed, [])
        self.assertIn(f"kept, its status is blocked: {IDLE}  idle 12.0 days", printed)
        self.assertIn(f"kept, its {PLAN_NAME} cannot be read: {OTHER}  idle 9.0 days", printed)
        self.assertIn(f"kept, it has no status: {THIRD}  idle 10.0 days", printed)
        self.assertIn(session_gc.CLOSE_HINT, printed)

    def test_gc_flags_a_kept_folder_that_looks_finished_or_abandoned_and_still_moves_nothing(self) -> None:
        finished = self.folder(IDLE, 12, status="active")
        (finished / PLAN_NAME).write_text(
            plan("active").replace("## Steps", "## Steps\n- [x] 1. a"), encoding="utf-8", newline="\n"
        )
        make_idle(finished, 12)
        printed = self.run_gc()
        self.assertEqual(self.trashed, [])
        self.assertIn(f"kept, its status is active: {IDLE}  idle 12.0 days", printed)
        self.assertIn(f"flagged, every step is checked, yet the status is active: {IDLE}", printed)
        self.assertIn(f"flagged, its Request is empty and nothing has changed for 12.0 days: {IDLE}", printed)

    def test_gc_sweeps_a_folder_with_no_plan_and_a_report_as_it_says(self) -> None:
        old = self.folder(IDLE, 12)
        (old / "report.md").write_text("# Report\nStop: success\n", encoding="utf-8", newline="\n")
        make_idle(old, 12)
        self.run_gc()
        self.assertEqual(self.trashed, [old])

    def test_gc_never_sweeps_the_callers_own_session(self) -> None:
        self.folder(IDLE, 30, status="complete")
        self.run_gc(keep=IDLE)
        self.assertEqual(self.trashed, [])

    def test_a_shorter_limit_is_honoured_and_one_under_a_day_refused(self) -> None:
        gone = self.folder(IDLE, 3, status="complete")
        for limit in (0, 0.5, -1, float("nan")):
            with self.subTest(limit=limit):
                with self.assertRaises(SystemExit):
                    self.run_gc(idle_days=limit)
        self.assertEqual(self.trashed, [])
        self.run_gc(idle_days=2)
        self.assertEqual(self.trashed, [gone])

    def test_gc_logs_as_the_daily_sweep_does_and_says_who_asked(self) -> None:
        self.folder(IDLE, 8, status="complete")
        self.run_gc()
        self.assertIn(["swept", "", "limit 1 days, by gc"], self.events())
        self.assertIn(["reaped", IDLE], [event[:2] for event in self.events()])

    def test_nothing_to_sweep_is_said(self) -> None:
        self.assertIn("no session folder has been idle more than 1 days", self.run_gc())


class ProjectLocationsNotSwept(Fixture):
    def project_folder(self) -> tuple[Path, Path]:
        location = self.fake_root / "project" / "sessions"
        folder = location / IDLE
        folder.mkdir(parents=True)
        (folder / PLAN_NAME).write_text(plan("complete"), encoding="utf-8", newline="\n")
        make_idle(folder, 30)
        register(location)
        return location, folder

    def test_neither_sweep_moves_a_folder_in_a_project_location(self) -> None:
        _, folder = self.project_folder()
        self.daily()
        self.run_gc()
        self.assertEqual(self.trashed, [])
        self.assertTrue(folder.is_dir())

    def test_gc_names_each_project_location_it_did_not_sweep(self) -> None:
        location, _ = self.project_folder()
        printed = self.run_gc()
        self.assertIn(f"{session_gc.NOT_SWEPT}: {location.resolve()}", printed)

    def test_gc_names_none_when_no_project_location_is_recorded(self) -> None:
        self.assertNotIn("not swept", self.run_gc())

    def test_gc_removes_each_recorded_location_that_is_gone_and_names_it(self) -> None:
        location, _ = self.project_folder()
        gone = self.fake_root / "unmounted"
        register(gone)
        printed = self.run_gc()
        self.assertIn(f"{session_gc.FORGOTTEN}: {gone.resolve()}", printed)
        self.assertNotIn(f"{session_gc.FORGOTTEN}: {location.resolve()}", printed)
        self.assertEqual(registered_locations(), [location.resolve()])
        self.assertEqual([each for entry in project_registry.read_entries() for each in entry.locations], [str(location.resolve())])
        self.assertNotIn(session_gc.FORGOTTEN, self.run_gc())

    def test_the_daily_sweep_leaves_the_record_as_it_is(self) -> None:
        self.project_folder()
        register(self.fake_root / "unmounted")
        registry = memar_fs.projects_log()
        before = registry.read_text(encoding="utf-8")
        self.daily()
        self.assertEqual(registry.read_text(encoding="utf-8"), before)

    def test_the_daily_sweep_trims_memars_log_only(self) -> None:
        location, _ = self.project_folder()
        old = (datetime.now(timezone.utc) - timedelta(days=session_gc.LOG_KEEP_DAYS + 1)).isoformat(timespec="seconds")
        own = location / SESSION_LOG_NAME
        own.write_text(f"{old}\topened\t{IDLE}\t\n", encoding="utf-8", newline="\n")
        self.daily()
        self.assertEqual(own.read_text(encoding="utf-8"), f"{old}\topened\t{IDLE}\t\n")
        self.assertNotIn(own, self.trashed)


class RecordsAddedBeforeTheFolderGoes(Fixture):
    """The sweep is the one act that adds a session's records itself (owner, 2026-10-15): everything left, one commit, then the trash."""

    def setUp(self) -> None:
        super().setUp()
        self.keeping.stop()
        self.project = self.fake_root / "work" / "example"
        self.project.mkdir(parents=True)
        for args in (["init", "-q", "-b", "main"], ["config", "user.name", "Test"], ["config", "user.email", "t@example.org"]):
            subprocess.run(["git", "-C", str(self.project), *args], check=True, capture_output=True)
        project_registry.add_project("example", self.project)

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.project), *args], capture_output=True, text=True, check=True).stdout.strip()

    def commits(self) -> int:
        return len(self.git("rev-list", "dev-knowledge").split()) if self.git("branch", "--list", "dev-knowledge") else 0

    def finished(self, name: str, project: Path, *, status: str = "Complete", idle: float = 8) -> Path:
        path = memar_fs.session_dir(name, create=True)
        (path / PLAN_NAME).write_text(
            plan_skeleton("20261001T000000Z-1-0", "Work", "2026-10-01T00:00:00Z", project).replace("Status: Active", f"Status: {status}", 1),
            encoding="utf-8",
            newline="\n",
        )
        (path / "docs").mkdir()
        (path / "docs" / "note.md").write_text("# Note\n", encoding="utf-8", newline="\n")
        make_idle(path, idle)
        return path

    def test_the_records_are_added_before_the_folder_is_moved(self) -> None:
        idle = self.finished(IDLE, self.project)
        self.daily()
        self.assertEqual(self.trashed, [idle])
        plan_on_branch = self.git("show", f"dev-knowledge:.agents/sessions/{IDLE}/{PLAN_NAME}")
        self.assertIn("Project: example", plan_on_branch)
        self.assertEqual(self.git("show", f"dev-knowledge:.agents/sessions/{IDLE}/docs/note.md"), "# Note")

    def test_every_session_the_sweep_moves_is_added_in_one_commit(self) -> None:
        first, second = self.finished(IDLE, self.project), self.finished(OTHER, self.project)
        self.run_gc()
        self.assertEqual(sorted(self.trashed), sorted([first, second]))
        self.assertEqual(self.commits(), 1)
        for name in (IDLE, OTHER):
            self.assertTrue(self.git("ls-tree", "-r", "--name-only", "dev-knowledge", "--", f".agents/sessions/{name}/"))

    def test_a_session_already_archived_adds_nothing(self) -> None:
        idle = self.finished(IDLE, self.project)
        self.assertEqual(session_archive.keep_records([idle])[0].outcome, session_archive.Outcome.KEPT)
        make_idle(idle, 8)
        self.run_gc()
        self.assertEqual(self.trashed, [idle])
        self.assertEqual(self.commits(), 1)

    def test_a_folder_whose_records_cannot_be_kept_is_not_moved_and_gc_says_why(self) -> None:
        stuck = self.finished(OTHER, self.fake_root / "elsewhere")
        printed = self.run_gc()
        self.assertEqual(self.trashed, [])
        self.assertTrue(stuck.is_dir())
        self.assertIn("its records cannot be kept", printed)
        self.assertIn(OTHER, printed)

    def test_a_refused_session_does_not_hold_back_another_projects_commit(self) -> None:
        stuck = self.finished(OTHER, self.fake_root / "elsewhere")
        idle = self.finished(IDLE, self.project)
        self.run_gc()
        self.assertEqual(self.trashed, [idle])
        self.assertTrue(stuck.is_dir())

    def test_a_session_whose_report_is_queued_is_never_swept_nor_added(self) -> None:
        held = self.finished(IDLE, self.project)
        (held / "report.md").write_text("---\nTitle: T\nStatus: Queued\n---\n# Report\n", encoding="utf-8", newline="\n")
        make_idle(held, 8)
        printed = self.run_gc()
        self.assertEqual(self.trashed, [])
        self.assertTrue(held.is_dir())
        self.assertIn("Queued", printed)
        self.assertEqual(self.commits(), 0)

    def test_a_session_whose_plan_is_queued_is_never_swept_nor_added(self) -> None:
        held = self.finished(IDLE, self.project, status="Queued")
        self.run_gc()
        self.daily()
        self.assertEqual(self.trashed, [])
        self.assertEqual(self.commits(), 0)

    def test_a_folder_in_no_project_is_moved_as_before(self) -> None:
        bare = memar_fs.session_dir(THIRD, create=True)
        make_idle(bare, 8)
        self.run_gc()
        self.assertEqual(self.trashed, [bare])
        self.assertEqual(self.commits(), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
