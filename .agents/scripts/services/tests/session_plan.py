#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a session's plan.md format in `services/session_plan.py`.

    python .agents/scripts/services/tests/session_plan.py

The subject is the plan format every session service reads and writes, named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: plans are written under the
folder `machine/fs_test_scratch.py` names and removed with it.

What is pinned, and what each pin is for:

  Skeleton        A new plan is front matter, the title once as its heading,
                  `Status: Active`, and Request, Why, Steps, Next; the link to a
                  parent and its conversation is written only when given.
  ReadsTodaysShape  A plan's status is the front matter's `Status`, lowercased,
                  and an unknown one is returned as written; nothing else
                  gives a plan a status: not a body `Status:` line, not a
                  lower-case key, not a `##` section, and the old words open
                  and done are not translated.
  ShapeProblem    A plan in an earlier shape (lower-case keys, a body `Status:`
                  line, the old words, no front matter Status beside a body
                  line) is named, with where today's shape is shown
                  (`memar session new --help`) and no conversion script; a
                  plan in today's shape, and one with no front matter, are not.
  WritersRefuse   Setting a status, a priority, or a topic on a plan in an
                  earlier shape is refused with that message and the plan is
                  left byte for byte; on today's shape only the line set
                  changes.
  Complete        Only the word complete is finished.
  Title           A title is one line, and required where the caller says so.
  Priority        A plan's priority is its front matter's `priority`, a whole
                  number from 1 to 10, higher sooner; absent, or not such a
                  number, it is 5. A new plan writes it only when given; one
                  set later replaces the key, or adds it at the end of the
                  front matter, and leaves every other line as written; a
                  value outside 1 to 10, or a plan with no front matter, is
                  refused.
  Rewrite         Setting a status or a priority while another writer changes
                  the plan keeps both changes, not only the last; a status set
                  on the expectation that it is still one it was is refused,
                  and the plan left as it is, once it is no longer; a rewrite
                  leaves nothing beside the plan.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

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

import services.session_plan as session_plan
from services.session_record import PlanKey
from services.status import Kind, Status

TITLE = "Parse the header"
OPENED = "2026-10-01T00:00:00Z"


def old_plan(status: str) -> str:
    """A plan in the shape written before Status moved into the front matter: lowercase keys, `Status:` in the body."""
    return (
        f"---\ntitle: {TITLE}\nopened: {OPENED}\nproject: /work\npriority: 7\n---\n"
        f"# {TITLE}\nStatus: {status}\n\n## Request\n\n## Why\n\n## Steps\n\n## Next\n"
    )


def new_plan(status: str) -> str:
    """A plan in today's shape: Status in the front matter, keys in PascalCase."""
    return (
        f"---\nTitle: {TITLE}\nStatus: {status}\nOpened: {OPENED}\nProject: /work\nPriority: 7\n---\n"
        f"# {TITLE}\n\n## Request\n\n## Why\n\n## Steps\n\n## Next\n"
    )


def sectioned_plan(sections: list[tuple[str, str]]) -> str:
    """A plan of the earlier sectioned form: each request its own `##` section, its status under the heading."""
    lines = ["---", f"Title: {TITLE}", f"Opened: {OPENED}", "Project: /work", "---", f"# {TITLE}", ""]
    for heading, status in sections:
        lines += [f"## {heading}"] + ([f"Status: {status}"] if status else []) + ["", "### Request", ""]
    return "\n".join(lines) + "\n"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)

    def path(self, text: str) -> Path:
        path = self.folder / session_plan.PLAN_NAME
        path.write_bytes(text.encode("utf-8"))
        return path

    def read(self, text: str) -> session_plan.Plan:
        return session_plan.read_plan(self.path(text))


class Skeleton(Fixture):
    def test_a_new_plan_is_front_matter_with_its_status_the_title_and_four_parts(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"))
        self.assertEqual(
            text,
            f"---\nTitle: {TITLE}\nStatus: Active\nOpened: {OPENED}\nProject: {Path('/work')}\n---\n"
            f"# {TITLE}\n\n## Request\n\n## Why\n\n## Steps\n\n## Next\n",
        )
        self.assertEqual(text.count(TITLE), 2)
        plan = self.read(text)
        self.assertEqual(plan.status, "active")
        self.assertNotIn(PlanKey.PARENT.key, plan.front)
        self.assertIsNone(session_plan.plan_shape_problem(text.splitlines()))

    def test_the_link_is_written_only_when_given(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), parent="P-1", conversation="C-0")
        front = self.read(text).front
        self.assertEqual(front[PlanKey.PARENT.key], "P-1")
        self.assertEqual(front[PlanKey.CONVERSATION.key], "C-0")


class ReadsTodaysShape(Fixture):
    def test_the_front_matter_status_is_the_plans_in_any_case_and_an_unknown_one_as_written(self) -> None:
        for written, read in (("Active", "active"), ("COMPLETE", "complete"), ("Queued", "queued"), ("blocked", "blocked"), ("Archived", "archived")):
            with self.subTest(written=written):
                plan = self.read(new_plan(written))
                self.assertEqual(plan.status, read)
                self.assertEqual(plan.front["title"], TITLE)
                self.assertEqual(session_plan.priority_of(plan.front), 7)

    def test_the_old_words_are_not_translated(self) -> None:
        self.assertEqual(self.read(new_plan("open")).status, "open")
        self.assertEqual(self.read(new_plan("Done")).status, "done")
        self.assertNotIn(self.read(new_plan("open")).status, Status.keys(Kind.SESSION_PLAN))

    def test_a_body_status_line_gives_a_plan_no_status(self) -> None:
        self.assertEqual(self.read(old_plan("open")).status, "")
        text = new_plan("Complete").replace(f"# {TITLE}\n", f"# {TITLE}\nStatus: open\n")
        self.assertEqual(self.read(text).status, "complete")
        self.assertEqual(self.read("# Notes only\nStatus: done\n").status, "")

    def test_lower_case_keys_are_not_read(self) -> None:
        plan = self.read(old_plan("open"))
        self.assertNotIn("title", plan.front)
        self.assertNotIn("priority", plan.front)
        lower = new_plan("Active").replace("\nStatus:", "\nstatus:")
        self.assertEqual(self.read(lower).status, "")

    def test_sections_give_a_plan_no_status(self) -> None:
        self.assertEqual(self.read(sectioned_plan([("Lex", "done"), ("Parse", "open")])).status, "")

    def test_front_matter_is_none_without_it(self) -> None:
        self.assertIsNone(self.read("# Notes only\n").front)


class ShapeProblem(Fixture):
    def problem(self, text: str) -> str | None:
        return session_plan.plan_shape_problem(text.splitlines())

    def test_each_earlier_shape_is_named_with_where_todays_shape_is_shown(self) -> None:
        shapes = {
            "lower-case keys and a body status": old_plan("open"),
            "lower-case keys alone": new_plan("Active").replace("\nTitle:", "\ntitle:"),
            "a body status line": new_plan("Active").replace("Status: Active\n", "").replace(f"# {TITLE}\n", f"# {TITLE}\nStatus: open\n"),
            "the old word open": new_plan("open"),
            "the old word done": new_plan("done"),
        }
        for name, text in shapes.items():
            with self.subTest(shape=name):
                found = self.problem(text)
                self.assertIsNotNone(found)
                self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, found)
                self.assertIn("memar session new --help", found)
                self.assertNotIn(".py", found)

    def test_todays_shape_and_a_plan_without_front_matter_have_none(self) -> None:
        for text in (new_plan("Active"), new_plan("Complete (2026-10-09)"), "# T\nStatus: open\n", sectioned_plan([("A", "open")])):
            with self.subTest(text=text[:30]):
                self.assertIsNone(self.problem(text))

    def test_a_body_line_beside_a_front_matter_status_is_not_a_shape_problem(self) -> None:
        text = new_plan("Complete").replace(f"# {TITLE}\n", f"# {TITLE}\nStatus: open\n")
        self.assertIsNone(self.problem(text))

    def test_the_file_reading_form_reads_the_plan_and_says_none_for_a_missing_one(self) -> None:
        self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, session_plan.plan_file_problem(self.path(old_plan("done"))))
        self.assertIsNone(session_plan.plan_file_problem(self.folder / "missing.md"))


class WritersRefuse(Fixture):
    def test_every_writer_refuses_a_plan_in_an_earlier_shape_and_leaves_it_byte_for_byte(self) -> None:
        for text in (old_plan("queued"), new_plan("open")):
            path = self.path(text)
            for write in (
                lambda: session_plan.set_status(path, "active"),
                lambda: session_plan.set_priority(path, 3),
                lambda: session_plan.set_topic(path, "x"),
            ):
                with self.subTest(text=text[:40]):
                    with self.assertRaises(SystemExit) as refused:
                        write()
                    self.assertIn(session_plan.EARLIER_SHAPE_REMEDY, str(refused.exception.code))
                    self.assertEqual(path.read_bytes(), text.encode("utf-8"))

    def test_on_todays_shape_only_the_line_set_changes(self) -> None:
        path = self.path(new_plan("Queued"))
        session_plan.set_status(path, "active", expected=("queued",))
        self.assertEqual(path.read_text(encoding="utf-8"), new_plan("Active"))

    def test_setting_a_priority_and_a_topic_keep_the_status_and_an_empty_topic_removes_the_key(self) -> None:
        path = self.path(new_plan("Blocked"))
        session_plan.set_priority(path, 3)
        session_plan.set_topic(path, "Lexer Fixes")
        text = path.read_text(encoding="utf-8")
        self.assertIn("\nStatus: Blocked\n", text)
        self.assertIn("\nPriority: 3\n", text)
        self.assertIn("\nTopic: lexer-fixes\n", text)
        session_plan.set_topic(path, "")
        self.assertNotIn("opic", path.read_text(encoding="utf-8"))

    def test_a_plan_with_front_matter_and_no_status_is_given_one_and_without_front_matter_is_refused(self) -> None:
        path = self.path(f"---\nTitle: {TITLE}\n---\n# {TITLE}\n\n## Request\n")
        session_plan.set_status(path, "active")
        self.assertEqual(session_plan.read_plan(path).status, "active")
        bare = self.path("# T\n\n## Request\n")
        with self.assertRaises(SystemExit):
            session_plan.set_status(bare, "complete")

    def test_line_endings_are_kept(self) -> None:
        path = self.path(new_plan("Queued").replace("\n", "\r\n"))
        session_plan.set_status(path, "active")
        self.assertNotIn(b"\n", path.read_bytes().replace(b"\r\n", b""))

    def test_the_old_word_is_not_accepted_as_a_status_to_set_or_expect(self) -> None:
        path = self.path(new_plan("Queued"))
        with self.assertRaises(SystemExit):
            session_plan.set_status(path, "open")
        with self.assertRaises(SystemExit):
            session_plan.set_status(path, "active", expected=("open",))


class Complete(unittest.TestCase):
    def test_only_the_word_complete_is_finished(self) -> None:
        self.assertTrue(session_plan.is_complete("complete"))
        for status in ("done", "Complete (2026-10-09 12:00)", "completed", "open", "blocked", "", "incomplete"):
            with self.subTest(status=status):
                self.assertFalse(session_plan.is_complete(status))


class Title(unittest.TestCase):
    def test_a_title_is_one_line_and_blank_is_none(self) -> None:
        for title in ("two\nlines", "carriage\rreturn"):
            with self.subTest(title=title):
                with self.assertRaises(SystemExit):
                    session_plan.checked_title(title, required=False)
        self.assertIsNone(session_plan.checked_title("   ", required=False))
        self.assertEqual(session_plan.checked_title(" T ", required=True), "T")

    def test_a_required_title_that_is_absent_is_refused(self) -> None:
        for title in (None, "", "  "):
            with self.subTest(title=title):
                with self.assertRaises(SystemExit):
                    session_plan.checked_title(title, required=True)


class Priority(Fixture):
    def test_a_plan_without_priority_reads_as_the_default_five(self) -> None:
        self.assertEqual(session_plan.DEFAULT_PRIORITY, 5)
        front = self.read(session_plan.plan_skeleton(TITLE, OPENED, Path("/work"))).front
        self.assertNotIn(PlanKey.PRIORITY.key, front)
        self.assertEqual(session_plan.priority_of(front), 5)
        self.assertEqual(session_plan.priority_of(None), 5)

    def test_a_written_priority_is_read_and_one_not_from_1_to_10_is_the_default(self) -> None:
        for value, expected in (("1", 1), ("10", 10), (" 7 ", 7), ("0", 5), ("11", 5), ("high", 5), ("3.5", 5)):
            with self.subTest(value=value):
                self.assertEqual(session_plan.priority_of({PlanKey.PRIORITY.key: value}), expected)

    def test_a_new_plan_writes_its_priority_only_when_given(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), priority=8)
        self.assertIn("\nPriority: 8\n---\n", text)
        self.assertEqual(session_plan.priority_of(self.read(text).front), 8)

    def test_setting_a_priority_replaces_or_adds_the_key_and_keeps_every_other_line(self) -> None:
        path = self.folder / session_plan.PLAN_NAME
        original = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), status="queued").replace("\n", "\r\n")
        path.write_bytes(original.encode("utf-8"))
        session_plan.set_priority(path, 9)
        text = path.read_bytes().decode("utf-8")
        self.assertEqual(text, original.replace("\r\n---\r\n#", "\r\nPriority: 9\r\n---\r\n#", 1))
        session_plan.set_priority(path, 2)
        self.assertEqual(session_plan.priority_of(session_plan.read_plan(path).front), 2)
        self.assertEqual(path.read_bytes().decode("utf-8").count("riority:"), 1)
        self.assertEqual(session_plan.read_plan(path).status, "queued")

    def test_a_priority_outside_1_to_10_or_a_plan_without_front_matter_is_refused(self) -> None:
        for value in ("0", "11", "x", "5.0"):
            with self.subTest(value=value):
                with self.assertRaises(SystemExit):
                    session_plan.checked_priority(value)
        self.assertEqual(session_plan.checked_priority("10"), 10)
        path = self.folder / session_plan.PLAN_NAME
        path.write_text("# T\nStatus: open\n", encoding="utf-8")
        with self.assertRaises(SystemExit):
            session_plan.set_priority(path, 3)


class Rewrite(Fixture):
    def plan(self, status: str) -> Path:
        path = self.folder / session_plan.PLAN_NAME
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), status=status)
        path.write_text(text, encoding="utf-8", newline="\n")
        return path

    def changed_once_after_reading(self, path: Path, old: str, new: str):
        """A patch under which the first read of PATH is followed at once by another writer replacing OLD with NEW."""
        real = Path.read_bytes
        done = []

        def read_bytes(self_path: Path) -> bytes:
            data = real(self_path)
            if self_path == path and not done:
                done.append(True)
                path.write_bytes(data.replace(old.encode(), new.encode()))
            return data

        return unittest.mock.patch.object(Path, "read_bytes", read_bytes)

    def test_a_priority_set_while_the_status_changes_keeps_both(self) -> None:
        path = self.plan("queued")
        with self.changed_once_after_reading(path, "Status: Queued", "Status: Active"):
            session_plan.set_priority(path, 9)
        plan = session_plan.read_plan(path)
        self.assertEqual((plan.status, session_plan.priority_of(plan.front)), ("active", 9))

    def test_a_status_set_while_the_priority_changes_keeps_both(self) -> None:
        path = self.plan("queued")
        with self.changed_once_after_reading(path, f"Opened: {OPENED}\n", f"Opened: {OPENED}\nPriority: 8\n"):
            session_plan.set_status(path, "active")
        plan = session_plan.read_plan(path)
        self.assertEqual((plan.status, session_plan.priority_of(plan.front)), ("active", 8))

    def test_a_status_no_longer_the_expected_one_is_left_as_it_is(self) -> None:
        path = self.plan("queued")
        with self.changed_once_after_reading(path, "Status: Queued", "Status: Complete"):
            with self.assertRaises(SystemExit):
                session_plan.set_status(path, "active", expected=("queued",))
        self.assertEqual(session_plan.read_plan(path).status, "complete")

    def test_a_rewrite_leaves_only_the_plan_in_its_folder(self) -> None:
        path = self.plan("queued")
        session_plan.set_priority(path, 3)
        session_plan.set_status(path, "active")
        self.assertEqual([entry.name for entry in self.folder.iterdir()], [session_plan.PLAN_NAME])


if __name__ == "__main__":
    unittest.main(verbosity=2)
