#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a session's topic, in `services/session_topic.py` and the plan's `topic` key in `services/session_plan.py`.

    python .agents/scripts/services/tests/session_topic.py

The subject is the topic of a plan: the one subject a queued task is about, so
that `claims` can hand one agent the tasks of one subject (that batch rule is
tested in `session_claims.py`). Set by `memar session new --topic T`, changed by
`memar session topic ID T`, read as a list by `memar session topics`. Named for
the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The rulings it holds are the owner's of 2026-10-13, recorded in session
20261013T052606Z-30600-0: one `topic` per plan, free text normalized to lower
case with spaces as hyphens; empty removes it; a topic within edit distance 1
or 2 of one in use is warned about and still written; `new --parent` does not
copy the parent's topic.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  TopicField      The plan's `topic` is normalized when written (lower case,
                  runs of spaces as one hyphen); a plan without one has none;
                  `new --topic` writes it into a new plan and sets it on one
                  that is there; `new --parent` does not copy the parent's;
                  a topic is one line.
  TopicVerb       `topic ID T` writes T normalized and says what it was; an
                  empty T removes the key and keeps every other line; a
                  session that is not there is refused.
  NearMatch       A topic one or two edits from one the project uses is
                  warned about naming both, and is still written; an equal
                  topic, or a far one, is not warned about.
  TopicsListing   `topics` lists the project's topics with how many sessions
                  and how many of them are queued, the largest first; another
                  project's topics are not listed; no topic says so.
"""
from __future__ import annotations

import argparse
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import services.project_registry as registry
import services.session_new as session_new
import services.session_plan as session_plan
import services.session_topic as session_topic
import services.session_topics as session_topics


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.git_project("project-x")
        project = unittest.mock.patch.object(session_new, "project_root", return_value=self.project)
        project.start()
        self.addCleanup(project.stop)

    def git_project(self, name: str) -> Path:
        folder = self.fake_root / name
        folder.mkdir()
        subprocess.run(["git", "init", "-q", str(folder)], check=True, capture_output=True)
        return folder

    def session(self, sid: str, status: str = "queued", topic: str | None = None, project: Path | None = None) -> Path:
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        tagged = f"Topic: {topic}\n" if topic is not None else ""
        (folder / session_plan.PLAN_NAME).write_text(
            f"---\nTitle: T\nStatus: {status.capitalize()}\nOpened: 2026-10-13T00:00:00Z\nProject: {project or self.project}\n{tagged}---\n"
            f"# T\n\n## Request\nx\n\n## Why\n\n## Steps\n\n## Next\n",
            encoding="utf-8",
            newline="\n",
        )
        return folder

    def front(self, folder: Path) -> dict[str, str]:
        return session_plan.read_plan(folder / session_plan.PLAN_NAME).front or {}

    def printed(self, call, *args, **kwargs) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            call(*args, **kwargs)
        return out.getvalue()

    def refused(self, call, *args) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args)
        return str(raised.exception.code)


class TopicField(Fixture):
    def test_a_topic_is_written_lower_case_with_hyphens_for_spaces(self) -> None:
        for given, written in (("Khayyam", "khayyam"), ("  Local  LSP server ", "local-lsp-server"), ("a\tb", "a-b")):
            with self.subTest(given=given):
                self.assertEqual(session_plan.normalized_topic(given), written)

    def test_a_plan_without_a_topic_has_none(self) -> None:
        folder = self.session("20261013T000001Z-1-0")
        self.assertEqual(session_plan.topic_of(self.front(folder)), "")
        self.assertEqual(session_plan.topic_of(None), "")

    def test_new_writes_the_topic_into_a_new_plan(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            sid, path = session_new.ensure_session("20261013T000002Z-1-0", "Title", None, topic="Khayyam LSP", project=str(self.project))
        self.assertEqual(self.front(path)["topic"], "khayyam-lsp")
        self.assertIn("Topic: khayyam-lsp\n", (path / session_plan.PLAN_NAME).read_text(encoding="utf-8"))

    def test_new_without_a_topic_writes_none(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_new.ensure_session("20261013T000003Z-1-0", "Title", None, project=str(self.project))
        self.assertNotIn("topic", self.front(path))

    def test_new_sets_the_topic_on_a_plan_that_is_there(self) -> None:
        folder = self.session("20261013T000004Z-1-0", "active")
        with contextlib.redirect_stdout(io.StringIO()):
            session_new.ensure_session(folder.name, None, None, topic="docs")
        self.assertEqual(self.front(folder)["topic"], "docs")
        self.assertEqual(session_plan.read_plan(folder / session_plan.PLAN_NAME).status, "active")

    def test_a_child_opened_with_a_parent_does_not_copy_the_parents_topic(self) -> None:
        parent = self.session("20261013T000005Z-1-0", "active", topic="docs")
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_new.ensure_session("20261013T000006Z-1-0", "Child", parent.name, project=str(self.project))
        self.assertNotIn("topic", self.front(path))

    def test_a_topic_is_one_line_and_not_empty_on_new(self) -> None:
        self.assertIn("one line", self.refused(session_plan.checked_topic, "a\nb"))
        self.assertEqual(session_plan.checked_topic("  "), "")


class TopicVerb(Fixture):
    def test_the_verb_writes_the_topic_and_says_what_it_was(self) -> None:
        folder = self.session("20261013T000010Z-1-0", "active")
        text = self.printed(session_topic.set_session_topic, folder.name, "Docs Cleanup")
        self.assertIn(f"{folder.name}  topic docs-cleanup, was (none)", text)
        self.assertEqual(self.front(folder)["topic"], "docs-cleanup")
        text = self.printed(session_topic.set_session_topic, folder.name, "docs")
        self.assertIn("topic docs, was docs-cleanup", text)

    def test_an_empty_topic_removes_the_key_and_keeps_every_other_line(self) -> None:
        folder = self.session("20261013T000011Z-1-0", "queued", topic="docs")
        before = (folder / session_plan.PLAN_NAME).read_text(encoding="utf-8")
        text = self.printed(session_topic.set_session_topic, folder.name, "")
        self.assertIn("topic (none), was docs", text)
        after = (folder / session_plan.PLAN_NAME).read_text(encoding="utf-8")
        self.assertEqual(after, before.replace("Topic: docs\n", ""))
        self.assertNotIn("topic", self.front(folder))

    def test_the_other_front_matter_and_the_body_are_kept(self) -> None:
        folder = self.session("20261013T000012Z-1-0", "queued")
        session_plan.set_priority(folder / session_plan.PLAN_NAME, 8)
        self.printed(session_topic.set_session_topic, folder.name, "docs")
        front = self.front(folder)
        self.assertEqual((front["priority"], front["topic"], front["title"]), ("8", "docs", "T"))
        self.assertEqual(session_plan.read_plan(folder / session_plan.PLAN_NAME).status, "queued")

    def test_a_session_that_is_not_there_is_refused(self) -> None:
        self.assertIn("no session", self.refused(session_topic.set_session_topic, "20261013T000013Z-1-0", "docs"))


class NearMatch(Fixture):
    def test_a_topic_one_or_two_edits_from_one_in_use_is_warned_about_and_still_written(self) -> None:
        self.session("20261013T000020Z-1-0", "queued", topic="khayyam")
        for index, typed in enumerate(("khayam", "khayyyam", "kayyam", "khayymal")):
            with self.subTest(typed=typed):
                folder = self.session(f"20261013T0000{21 + index}Z-1-0", "active")
                text = self.printed(session_topic.set_session_topic, folder.name, typed)
                self.assertIn(typed, text)
                self.assertIn("khayyam", text)
                self.assertIn("near", text)
                self.assertEqual(self.front(folder)["topic"], typed)

    def test_new_warns_the_same_way(self) -> None:
        self.session("20261013T000030Z-1-0", "queued", topic="khayyam")
        text = self.printed(session_new.ensure_session, "20261013T000031Z-1-0", "Title", None, topic="khayam", project=str(self.project))
        self.assertIn("near", text)
        self.assertIn("khayyam", text)

    def test_an_equal_topic_or_a_far_one_is_not_warned_about(self) -> None:
        self.session("20261013T000040Z-1-0", "queued", topic="khayyam")
        for index, typed in enumerate(("khayyam", "docs-cleanup")):
            with self.subTest(typed=typed):
                folder = self.session(f"20261013T0000{41 + index}Z-1-0", "active")
                self.assertNotIn("near", self.printed(session_topic.set_session_topic, folder.name, typed))

    def test_another_projects_topics_are_not_compared(self) -> None:
        other = self.git_project("project-y")
        self.session("20261013T000050Z-1-0", "queued", topic="khayyam", project=other)
        folder = self.session("20261013T000051Z-1-0", "active")
        self.assertNotIn("near", self.printed(session_topic.set_session_topic, folder.name, "khayam"))

    def test_edit_distance_counts_insertions_deletions_and_substitutions(self) -> None:
        for one, two, distance in (("a", "a", 0), ("abc", "abd", 1), ("abc", "abcd", 1), ("abc", "ac", 1), ("kitten", "sitting", 3)):
            with self.subTest(one=one, two=two):
                self.assertEqual(session_topic.edit_distance(one, two), distance)


class TopicsListing(Fixture):
    def listed(self, project: Path | None = None) -> str:
        return self.printed(session_topics.list_topics, str(project or self.project))

    def test_topics_are_listed_with_their_counts_the_largest_first(self) -> None:
        self.session("20261013T000060Z-1-0", "queued", topic="docs")
        self.session("20261013T000061Z-1-0", "queued", topic="khayyam")
        self.session("20261013T000062Z-1-0", "active", topic="khayyam")
        self.session("20261013T000063Z-1-0", "queued", topic="khayyam")
        self.session("20261013T000064Z-1-0", "queued")
        lines = [line for line in self.listed().splitlines() if line.strip()]
        self.assertEqual(len(lines), 2)
        self.assertIn("khayyam", lines[0])
        self.assertIn("3 sessions", lines[0])
        self.assertIn("2 queued", lines[0])
        self.assertIn("docs", lines[1])
        self.assertIn("1 session", lines[1])
        self.assertNotIn("1 sessions", lines[1])

    def test_the_project_is_named_by_a_name_or_a_folder_and_never_by_the_calling_folder(self) -> None:
        registry.add_project("project-x", self.project)
        self.session("20261013T000070Z-1-0", "queued", topic="docs")
        parser = argparse.ArgumentParser()
        command = session_topics.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(["topics", "--project", "project-x"]))
        self.assertIn("docs", out.getvalue())
        for missing in (None, "", " "):
            with self.subTest(missing=missing):
                with self.assertRaises(SystemExit) as raised:
                    self.printed(session_topics.list_topics, missing)
                self.assertIn("--project" if missing is None else "--project-path", str(raised.exception.code))

    def test_another_projects_topics_are_not_listed(self) -> None:
        other = self.git_project("project-y")
        self.session("20261013T000070Z-1-0", "queued", topic="theirs", project=other)
        self.session("20261013T000071Z-1-0", "queued", topic="ours")
        text = self.listed()
        self.assertIn("ours", text)
        self.assertNotIn("theirs", text)
        self.assertIn("theirs", self.listed(other))

    def test_no_topic_in_use_is_said(self) -> None:
        self.session("20261013T000080Z-1-0", "queued")
        self.assertIn("no topic", self.listed())


if __name__ == "__main__":
    unittest.main()
