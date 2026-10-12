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
                  `Status: open`, and Request, Why, Steps, Next; the link to a
                  parent and its conversation is written only when given.
  OwnStatus       A plan's status is the `Status:` line above its first `##`
                  heading, lowercased, and an unknown one is returned as
                  written.
  SectionedForm   A plan of the earlier sectioned form — each task a `##`
                  section, its status under the heading — is still read: open
                  when any task is, else blocked, else the first status not
                  done, and done only when every task is; a status inside a
                  section's part is not the section's, and a plan with no
                  status anywhere has none, which is not done.
  Finished        A status that starts with done or complete, in any case, is
                  finished, so an earlier plan's free-text status is read;
                  any other is not.
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

TITLE = "Parse the header"
OPENED = "2026-10-01T00:00:00Z"


def sectioned_plan(sections: list[tuple[str, str]]) -> str:
    """A plan of the earlier sectioned form: each request its own `##` section, its status under the heading."""
    lines = ["---", f"title: {TITLE}", f"opened: {OPENED}", "project: /work", "---", f"# {TITLE}", ""]
    for heading, status in sections:
        lines += [f"## {heading}"] + ([f"Status: {status}"] if status else []) + ["", "### Request", ""]
    return "\n".join(lines) + "\n"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.folder = Path(self.scratch.name)

    def read(self, text: str) -> session_plan.Plan:
        path = self.folder / session_plan.PLAN_NAME
        path.write_text(text, encoding="utf-8", newline="\n")
        return session_plan.read_plan(path)


class Skeleton(Fixture):
    def test_a_new_plan_is_front_matter_title_open_status_and_four_parts(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"))
        self.assertEqual(
            text,
            f"---\ntitle: {TITLE}\nopened: {OPENED}\nproject: {Path('/work')}\n---\n"
            f"# {TITLE}\nStatus: open\n\n## Request\n\n## Why\n\n## Steps\n\n## Next\n",
        )
        self.assertEqual(text.count(TITLE), 2)
        plan = self.read(text)
        self.assertEqual(plan.status, "open")
        self.assertEqual(plan.tasks, [])
        self.assertNotIn(session_plan.PARENT_KEY, plan.front)

    def test_the_link_is_written_only_when_given(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), parent="P-1", conversation="C-0")
        front = self.read(text).front
        self.assertEqual(front[session_plan.PARENT_KEY], "P-1")
        self.assertEqual(front[session_plan.CONVERSATION_KEY], "C-0")


class OwnStatus(Fixture):
    def test_the_status_above_the_first_section_is_the_plans(self) -> None:
        for written, read in (("done", "done"), ("Blocked", "blocked"), ("archived", "archived")):
            with self.subTest(written=written):
                text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work")).replace(
                    "Status: open", f"Status: {written}"
                )
                self.assertEqual(self.read(text).status, read)

    def test_a_status_line_inside_a_part_is_not_the_plans(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work")).replace("Status: open\n", "")
        text += "Status: done\n"
        plan = self.read(text)
        self.assertNotEqual(plan.status, "done")


class SectionedForm(Fixture):
    def test_any_open_task_makes_the_plan_open(self) -> None:
        plan = self.read(sectioned_plan([("Lex", "done"), ("Parse", "open"), ("Wait", "blocked")]))
        self.assertEqual(plan.status, "open")
        self.assertEqual(plan.tasks, [("Lex", "done"), ("Parse", "open"), ("Wait", "blocked")])

    def test_blocked_comes_next_then_any_status_not_done(self) -> None:
        self.assertEqual(self.read(sectioned_plan([("Lex", "done"), ("Wait", "blocked")])).status, "blocked")
        self.assertEqual(self.read(sectioned_plan([("Lex", "done"), ("Later", "archived")])).status, "archived")
        self.assertEqual(self.read(sectioned_plan([("Lex", "done"), ("Later", "")])).status, "")

    def test_done_only_when_every_task_is(self) -> None:
        self.assertEqual(self.read(sectioned_plan([("Lex", "done"), ("Parse", "Done")])).status, "done")

    def test_a_status_inside_a_part_is_not_the_sections(self) -> None:
        text = sectioned_plan([("Lex", "")]).replace("### Request\n", "### Request\nStatus: done\n")
        plan = self.read(text)
        self.assertEqual(plan.tasks, [("Lex", "")])
        self.assertEqual(plan.status, "")

    def test_a_plan_with_no_status_anywhere_has_none(self) -> None:
        self.assertEqual(self.read(sectioned_plan([])).status, "")
        self.assertEqual(self.read("# Notes only\n").status, "")

    def test_front_matter_is_read_in_both_forms(self) -> None:
        self.assertEqual(self.read(sectioned_plan([])).front["title"], TITLE)
        self.assertIsNone(self.read("# Notes only\n").front)

    def test_a_task_finished_in_free_text_counts_as_done(self) -> None:
        plan = self.read(sectioned_plan([("Lex", "done"), ("Parse", "Complete (2026-10-09, merged)")]))
        self.assertEqual(plan.status, "done")


class Finished(unittest.TestCase):
    def test_a_status_starting_with_done_or_complete_is_finished_and_no_other(self) -> None:
        for status in ("done", "Done", "DONE — merged", "complete", "Complete (2026-10-09 12:00)", "completed"):
            with self.subTest(status=status):
                self.assertTrue(session_plan.is_done(status))
        for status in ("open", "blocked", "archived", "", "not done", "incomplete", "in progress, done soon"):
            with self.subTest(status=status):
                self.assertFalse(session_plan.is_done(status))


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
        self.assertNotIn(session_plan.PRIORITY_KEY, front)
        self.assertEqual(session_plan.priority_of(front), 5)
        self.assertEqual(session_plan.priority_of(None), 5)

    def test_a_written_priority_is_read_and_one_not_from_1_to_10_is_the_default(self) -> None:
        for value, expected in (("1", 1), ("10", 10), (" 7 ", 7), ("0", 5), ("11", 5), ("high", 5), ("3.5", 5)):
            with self.subTest(value=value):
                self.assertEqual(session_plan.priority_of({session_plan.PRIORITY_KEY: value}), expected)

    def test_a_new_plan_writes_its_priority_only_when_given(self) -> None:
        text = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), priority=8)
        self.assertIn("\npriority: 8\n---\n", text)
        self.assertEqual(session_plan.priority_of(self.read(text).front), 8)

    def test_setting_a_priority_replaces_or_adds_the_key_and_keeps_every_other_line(self) -> None:
        path = self.folder / session_plan.PLAN_NAME
        original = session_plan.plan_skeleton(TITLE, OPENED, Path("/work"), status="queued").replace("\n", "\r\n")
        path.write_bytes(original.encode("utf-8"))
        session_plan.set_priority(path, 9)
        text = path.read_bytes().decode("utf-8")
        self.assertEqual(text, original.replace("\r\n---\r\n#", "\r\npriority: 9\r\n---\r\n#", 1))
        session_plan.set_priority(path, 2)
        self.assertEqual(session_plan.priority_of(session_plan.read_plan(path).front), 2)
        self.assertEqual(path.read_bytes().decode("utf-8").count("priority:"), 1)
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
        with self.changed_once_after_reading(path, "Status: queued", "Status: open"):
            session_plan.set_priority(path, 9)
        plan = session_plan.read_plan(path)
        self.assertEqual((plan.status, session_plan.priority_of(plan.front)), ("open", 9))

    def test_a_status_set_while_the_priority_changes_keeps_both(self) -> None:
        path = self.plan("queued")
        with self.changed_once_after_reading(path, f"opened: {OPENED}\n", f"opened: {OPENED}\npriority: 8\n"):
            session_plan.set_status(path, "open")
        plan = session_plan.read_plan(path)
        self.assertEqual((plan.status, session_plan.priority_of(plan.front)), ("open", 8))

    def test_a_status_no_longer_the_expected_one_is_left_as_it_is(self) -> None:
        path = self.plan("queued")
        with self.changed_once_after_reading(path, "Status: queued", "Status: done"):
            with self.assertRaises(SystemExit):
                session_plan.set_status(path, "open", expected=("queued",))
        self.assertEqual(session_plan.read_plan(path).status, "done")

    def test_a_rewrite_leaves_only_the_plan_in_its_folder(self) -> None:
        path = self.plan("queued")
        session_plan.set_priority(path, 3)
        session_plan.set_status(path, "open")
        self.assertEqual([entry.name for entry in self.folder.iterdir()], [session_plan.PLAN_NAME])


if __name__ == "__main__":
    unittest.main(verbosity=2)
