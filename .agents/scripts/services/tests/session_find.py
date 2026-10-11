#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for finding sessions in `services/session_find.py`.

    python .agents/scripts/services/tests/session_find.py

The subject is `list`'s answer, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder. The Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  Listed          Every session folder is listed newest first with its title,
                  project, status, and path; a plan of the earlier sectioned
                  form also shows its tasks counted per status; a folder without a
                  readable plan is listed and marked.
  TextFilter      TEXT matches the id, title, project, or a listed task's
                  heading, in any case; an id prefix finds a session with no
                  plan.
  StatusAndIdle   --status keeps the sessions in that status, an old plan by
                  the status read off its tasks, and done keeps what the sweep
                  counts as done; --idle-days keeps those quiet
                  that long and says how long; together they find stalled work;
                  a negative --idle-days is refused.
  Conversations   The sessions of one conversation are listed together, where
                  its newest falls, each naming its parent and conversation;
                  --conversation, given any session of it, keeps only that
                  conversation, also once its first session is gone.
  ProjectLocations
                  By default only Memar's own sessions are listed. --project
                  lists every session folder in the project's own location,
                  a name the project chose among them, and each of Memar's
                  whose plan names the project, compared resolved and, on
                  Windows, in any case; it combines with TEXT, --status, and
                  --idle-days, and without a PATH it is the current project,
                  with one the project PATH lies in. A recorded location is
                  a project's only when its own project is that one: a
                  nested project's is not the enclosing one's, and a folder
                  that is no project owns none beneath it.
                  --conversation lists a conversation's sessions wherever
                  they lie; a recorded location that is gone is passed over.
  ReportMarks     A session whose report.md Stop does not map to its plan's
                  status, whose status is outside open, blocked, done, or
                  whose Stop is not a named stop, is marked with why; one
                  that agrees, an empty Stop, or no report, is not.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import contextlib
import io
import os
import subprocess
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
import services.project_preferences as project_preferences
import services.session_find as session_find
import services.session_location as session_location
from services.session_location import register
from services.session_plan import PLAN_NAME, plan_skeleton
from services.session_report import REPORT_NAME

DAY = 24 * 60 * 60
EARLIER_FORM = "1111-18dc000000000001-0"
OLDEST = "20261001T000000Z-1-0"
MIDDLE = "20261002T000000Z-1-0"
NEWEST = "20261003T000000Z-1-0"
LATEST = "20261004T000000Z-1-0"


def plan(title: str, project: str = "/work", status: str = "open", **link: str) -> str:
    return plan_skeleton(title, "2026-10-01T00:00:00Z", Path(project), **link).replace(
        "Status: open", f"Status: {status}"
    )


def sectioned_plan(title: str, tasks: list[tuple[str, str]]) -> str:
    """A plan of the earlier sectioned form: each task a `##` section, its status under the heading."""
    lines = ["---", f"title: {title}", "opened: 2026-10-01T00:00:00Z", "project: /work", "---", f"# {title}", ""]
    for heading, status in tasks:
        lines += [f"## {heading}", f"Status: {status}", "", "### Request", ""]
    return "\n".join(lines)


def git_init(path: Path) -> None:
    """Make PATH a git repository of its own, so its project is PATH and not the checkout the scratch lies in."""
    path.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", str(path)], check=True, capture_output=True)


def make_idle(path: Path, days: float) -> None:
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

    def session(self, sid: str, text: str | bytes | None = None) -> Path:
        path = memar_fs.session_dir(sid, create=True)
        if isinstance(text, bytes):
            (path / PLAN_NAME).write_bytes(text)
        elif text is not None:
            (path / PLAN_NAME).write_text(text, encoding="utf-8", newline="\n")
        return path

    def run_list(self, *arguments: str | float | None, **filters) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_find.list_sessions(*arguments, **filters)
        return out.getvalue()

    def listed(self, text: str) -> list[str]:
        """The ids in TEXT, in order: each entry's first line is the one not indented."""
        return [line.split()[0] for line in text.splitlines() if line and not line.startswith(" ")]


class Listed(Fixture):
    def test_sessions_are_listed_newest_first_and_only_sessions(self) -> None:
        for sid in (MIDDLE, EARLIER_FORM, NEWEST, OLDEST):
            self.session(sid, plan(sid))
        for name in ("images", "memar-edit-locks", "s-old"):
            (memar_fs.sessions_root() / name).mkdir()
        self.assertEqual(self.listed(self.run_list()), [NEWEST, MIDDLE, OLDEST, EARLIER_FORM])

    def test_an_entry_shows_title_project_status_and_path(self) -> None:
        path = self.session(NEWEST, plan("Parser: phase two", "C:/work/parser", "blocked"))
        text = self.run_list()
        self.assertIn(f"{NEWEST}  Parser: phase two", text)
        self.assertIn(f"project: {Path('C:/work/parser')}", text)
        self.assertIn("status: blocked", text)
        self.assertIn(f"path: {path}", text)
        self.assertNotIn("tasks:", text)
        self.assertNotIn("parent:", text)

    def test_a_plan_of_the_sectioned_form_shows_its_status_and_tasks(self) -> None:
        tasks = [("Parse", "open"), ("Lex", "done"), ("Emit", "open"), ("Wait for review", "blocked")]
        self.session(NEWEST, sectioned_plan("Old plan", tasks))
        text = self.run_list()
        self.assertIn("status: open", text)
        self.assertIn("tasks: 2 open, 1 blocked, 1 done", text)

    def test_a_folder_without_a_readable_plan_is_listed_and_marked(self) -> None:
        bare = self.session(OLDEST)
        self.session(MIDDLE, "# Notes only\nStatus: open\n")
        self.session(NEWEST, b"\xff\xfe")
        text = self.run_list()
        self.assertEqual(self.listed(text), [NEWEST, MIDDLE, OLDEST])
        self.assertIn(f"{OLDEST}  {session_find.NO_PLAN}", text)
        self.assertIn(f"path: {bare}", text)
        self.assertIn(f"{MIDDLE}  {session_find.NO_FRONT_MATTER}", text)
        self.assertIn(f"{NEWEST}  {session_find.UNREADABLE_PLAN}", text)
        self.assertEqual(text.count("status:"), 1)

    def test_a_plan_whose_status_cannot_be_read_is_listed_saying_so(self) -> None:
        self.session(NEWEST, sectioned_plan("Old", [("Parse", "")]).replace("Status: \n", ""))
        text = self.run_list()
        self.assertEqual(self.listed(text), [NEWEST])
        self.assertIn("status: none", text)

    def test_nothing_to_list_is_said(self) -> None:
        self.assertIn("no session folder", self.run_list())
        self.assertIn("no session folder matches", self.run_list("anything"))


class TextFilter(Fixture):
    def test_text_filters_over_id_title_project_and_task_headings_in_any_case(self) -> None:
        self.session(OLDEST, plan("Ship the parser", "/work/parser"))
        self.session(MIDDLE, sectioned_plan("Fix login", [("Reset the PASSWORD form", "done")]))
        self.session(NEWEST, plan("Write docs", "/work/website"))
        self.session(LATEST)
        self.assertEqual(self.listed(self.run_list("PARSER")), [OLDEST])
        self.assertEqual(self.listed(self.run_list("Website")), [NEWEST])
        self.assertEqual(self.listed(self.run_list("20261002")), [MIDDLE])
        self.assertEqual(self.listed(self.run_list("20261004")), [LATEST])
        self.assertEqual(self.listed(self.run_list("password")), [MIDDLE])
        self.assertEqual(self.listed(self.run_list("nothing like it")), [])


class StatusAndIdle(Fixture):
    def test_status_keeps_only_the_sessions_in_that_state(self) -> None:
        self.session(OLDEST, plan("Ship", status="open"))
        self.session(MIDDLE, plan("Fix", status="done"))
        self.session(NEWEST, sectioned_plan("Old", [("Write", "done"), ("Review", "blocked")]))
        self.session(LATEST)
        self.assertEqual(self.listed(self.run_list(status="open")), [OLDEST])
        self.assertEqual(self.listed(self.run_list(status="blocked")), [NEWEST])
        self.assertEqual(self.listed(self.run_list(status="done")), [MIDDLE])

    def test_done_lists_what_the_sweep_counts_as_done(self) -> None:
        self.session(OLDEST, plan("Ship", status="Complete (2026-10-09)"))
        self.session(MIDDLE, plan("Fix", status="incomplete"))
        self.assertEqual(self.listed(self.run_list(status="done")), [OLDEST])

    def test_idle_days_keeps_only_the_sessions_quiet_that_long(self) -> None:
        stale = self.session(OLDEST, plan("Ship"))
        self.session(NEWEST, plan("Fresh"))
        make_idle(stale, 9)
        text = self.run_list(idle_days=7)
        self.assertEqual(self.listed(text), [OLDEST])
        self.assertIn("idle: 9.0 days", text)

    def test_both_filters_together_find_the_sessions_work_stalled_in(self) -> None:
        stalled = self.session(OLDEST, plan("Stalled"))
        self.session(MIDDLE, plan("Busy"))
        finished = self.session(NEWEST, plan("Finished", status="done"))
        make_idle(stalled, 8)
        make_idle(finished, 8)
        text = self.run_list(status="open", idle_days=7)
        self.assertEqual(self.listed(text), [OLDEST])
        self.assertIn("idle: 8.0 days", text)

    def test_a_negative_idle_days_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_list(idle_days=-1)


class Conversations(Fixture):
    def setUp(self) -> None:
        super().setUp()
        # Two conversations, interleaved in time: OLDEST opened MIDDLE's
        # and LATEST's tasks; NEWEST is a conversation of its own.
        self.session(OLDEST, plan("First request"))
        self.session(MIDDLE, plan("Delegated step", parent=OLDEST, conversation=OLDEST))
        self.session(NEWEST, plan("Unrelated"))
        self.session(LATEST, plan("Second request", parent=MIDDLE, conversation=OLDEST))

    def test_a_conversations_sessions_are_listed_together_where_its_newest_falls(self) -> None:
        text = self.run_list()
        self.assertEqual(self.listed(text), [LATEST, MIDDLE, OLDEST, NEWEST])
        self.assertIn(f"parent: {MIDDLE}", text)
        self.assertIn(f"conversation: {OLDEST}", text)

    def test_any_session_names_its_conversation(self) -> None:
        for named in (OLDEST, MIDDLE, LATEST):
            with self.subTest(named=named):
                self.assertEqual(self.listed(self.run_list(conversation=named)), [LATEST, MIDDLE, OLDEST])
        self.assertEqual(self.listed(self.run_list(conversation=NEWEST)), [NEWEST])

    def test_a_conversation_whose_first_session_is_gone_is_still_found(self) -> None:
        first = memar_fs.session_dir(OLDEST)
        (first / PLAN_NAME).unlink()
        first.rmdir()
        self.assertEqual(self.listed(self.run_list(conversation=OLDEST)), [LATEST, MIDDLE])


class ProjectLocations(Fixture):
    def setUp(self) -> None:
        super().setUp()
        # A project keeping its sessions in its own `sessions` folder, holding
        # a minted id, a name the project chose, and a folder of its own; and
        # Memar's own sessions, one opened from that project and one not.
        self.project = self.fake_root / "project"
        git_init(self.project)
        preferences = project_preferences.preferences_path(self.project)
        preferences.parent.mkdir(parents=True)
        preferences.write_text(
            project_preferences.PREFERENCES_TEXT.replace("sessions:\n", "sessions: sessions\n", 1),
            encoding="utf-8",
            newline="\n",
        )
        self.location = self.project / "sessions"
        self.in_location(LATEST, plan("The project's", str(self.project), "blocked", parent=MIDDLE, conversation=MIDDLE))
        self.in_location("my-task", plan("Named by the project", str(self.project)))
        (self.location / "notes").mkdir()
        (self.location / "src").mkdir()
        (self.location / "src" / PLAN_NAME).write_text("# Not a session\n", encoding="utf-8", newline="\n")
        register(self.location)
        register(self.fake_root / "unmounted")
        named = str(self.project).upper() if os.name == "nt" else str(self.project)
        self.session(MIDDLE, plan("Opened from the project", named))
        self.session(OLDEST, plan("Another project's", str(self.fake_root / "other")))

    def in_location(self, sid: str, text: str) -> Path:
        path = self.location / sid
        path.mkdir(parents=True)
        (path / PLAN_NAME).write_text(text, encoding="utf-8", newline="\n")
        return path

    def test_by_default_only_memars_own_sessions_are_listed(self) -> None:
        self.assertEqual(self.listed(self.run_list()), [MIDDLE, OLDEST])
        self.assertEqual(self.listed(self.run_list(status="blocked")), [])

    def test_project_lists_its_own_location_and_memars_sessions_that_name_it(self) -> None:
        text = self.run_list(project=str(self.project))
        self.assertEqual(self.listed(text), [LATEST, MIDDLE, "my-task"])
        self.assertIn(f"path: {self.location / 'my-task'}", text)
        self.assertNotIn("notes", text)
        self.assertNotIn(f"path: {self.location / 'src'}", text)

    def test_project_combines_with_text_status_and_idle_days(self) -> None:
        make_idle(self.location / LATEST, 9)
        self.assertEqual(self.listed(self.run_list("named", project=str(self.project))), ["my-task"])
        self.assertEqual(self.listed(self.run_list(status="blocked", project=str(self.project))), [LATEST])
        self.assertEqual(self.listed(self.run_list(idle_days=7, project=str(self.project))), [LATEST])

    def test_project_without_a_path_is_the_project_of_the_current_folder(self) -> None:
        with unittest.mock.patch.object(session_find, "project_root", return_value=self.project):
            self.assertEqual(self.listed(self.run_list(project="")), [LATEST, MIDDLE, "my-task"])
        with unittest.mock.patch.object(session_find, "project_root", return_value=self.fake_root / "other"):
            self.assertEqual(self.listed(self.run_list(project="")), [OLDEST])

    def test_project_with_a_path_in_a_subfolder_is_that_folders_project(self) -> None:
        subfolder = self.project / "src" / "deep"
        subfolder.mkdir(parents=True)
        self.assertEqual(self.listed(self.run_list(project=str(subfolder))), [LATEST, MIDDLE, "my-task"])

    def test_a_nested_projects_location_is_its_own_not_the_enclosing_ones(self) -> None:
        inner = self.project / "inner"
        git_init(inner)
        folder = inner / "sessions" / "inner-task"
        folder.mkdir(parents=True)
        (folder / PLAN_NAME).write_text(plan("The inner project's", str(inner)), encoding="utf-8", newline="\n")
        register(inner / "sessions")
        self.assertEqual(self.listed(self.run_list(project=str(self.project))), [LATEST, MIDDLE, "my-task"])
        self.assertEqual(self.listed(self.run_list(project=str(inner))), ["inner-task"])
        self.assertEqual(session_location.locations_of(self.project), [self.location.resolve()])

    def test_a_folder_that_is_no_project_owns_no_location_beneath_it(self) -> None:
        inner = self.project / "inner"
        git_init(inner)
        (inner / "sessions").mkdir()
        register(inner / "sessions")
        self.assertEqual(session_location.locations_of(self.fake_root), [])
        with unittest.mock.patch.object(session_find, "project_root", return_value=self.fake_root):
            self.assertEqual(self.listed(self.run_list(project="")), [])

    def test_a_project_named_session_is_listed_in_a_recorded_location(self) -> None:
        self.assertIn("my-task", self.listed(self.run_list(project=str(self.project))))
        self.assertEqual(self.listed(self.run_list(conversation="my-task")), ["my-task"])

    def test_conversation_lists_its_sessions_wherever_they_lie_and_a_gone_location_is_passed_over(self) -> None:
        for named in (MIDDLE, LATEST):
            with self.subTest(named=named):
                self.assertEqual(self.listed(self.run_list(conversation=named)), [LATEST, MIDDLE])


class ReportMarks(Fixture):
    def report(self, sid: str, status: str, stop: str | None) -> None:
        path = self.session(sid, plan(sid, status=status))
        if stop is not None:
            (path / REPORT_NAME).write_text(f"# Report\nStop: {stop}\n\n## What ran\n", encoding="utf-8", newline="\n")

    def mark_of(self, sid: str) -> str | None:
        text = self.run_list(sid)
        found = [line.strip() for line in text.splitlines() if line.strip().startswith(session_find.DISAGREES)]
        return found[0] if found else None

    def test_a_stop_that_agrees_with_the_status_is_not_marked(self) -> None:
        for index, (status, stop) in enumerate(
            (
                ("done", "success"),
                ("done", "clean no-op"),
                ("blocked", "blocked"),
                ("blocked", "approval-required: which module owns it?"),
                ("open", "exhausted"),
                ("open", "No progress"),
            )
        ):
            sid = f"2026100{index}T000000Z-7-0"
            with self.subTest(stop=stop):
                self.report(sid, status, stop)
                self.assertIsNone(self.mark_of(sid))

    def test_a_stop_that_disagrees_with_the_status_is_marked_with_why(self) -> None:
        self.report(NEWEST, "open", "success")
        self.assertEqual(
            self.mark_of(NEWEST),
            f"{session_find.DISAGREES} {REPORT_NAME} Stop success means status done, the plan says open",
        )
        self.report(MIDDLE, "done", "blocked")
        self.assertIn("means status blocked", self.mark_of(MIDDLE))

    def test_an_empty_stop_or_no_report_is_not_marked(self) -> None:
        self.report(NEWEST, "done", "")
        self.report(MIDDLE, "open", None)
        self.assertIsNone(self.mark_of(NEWEST))
        self.assertIsNone(self.mark_of(MIDDLE))

    def test_a_status_outside_the_vocabulary_or_a_stop_not_named_is_marked(self) -> None:
        self.report(NEWEST, "complete", None)
        self.assertEqual(self.mark_of(NEWEST), f"{session_find.DISAGREES} status complete is not one of open, blocked, done")
        self.report(MIDDLE, "done", "finished")
        self.assertIn("Stop finished is not one of", self.mark_of(MIDDLE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
