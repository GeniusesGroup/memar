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
import services.session_find as session_find
from services.session_plan import PLAN_NAME, plan_skeleton

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
