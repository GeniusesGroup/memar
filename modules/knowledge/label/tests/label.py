#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for a session's labels, in `modules/process/session/services/label.py`, `modules/process/session/services/labels.py` and `modules/process/session/services/plan_labels.py`.

    python modules/process/session/tests/label.py

The subject is the `Labels` field of a plan: the words that link it to other
sessions outside the structure of their ids, each written `Kind: word`, as many
as the task needs. Set by `memar session new --label KIND=WORD` (repeatable),
changed by `memar session label ID KIND=WORD [--remove]`, read as a list by
`memar session labels`. They replace the plan's `Topic` and `Kind` keys (owner,
2026-10-16). Named for the file that holds the verb per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The rulings it holds besides: a topic is free text normalized to lower case with
spaces as hyphens; a topic within edit distance 1 or 2 of one in use is warned
about and still written; `new --parent` does not copy the parent's labels.

Nothing here writes outside its scratch folder: the Memar root the services
resolve is patched onto one, made under the folder `machine/fs_test_scratch.py`
names.

What is pinned, and what each pin is for:

  LabelsField     `new --label` writes the labels as a block into a new plan and
                  adds them to one that is there; several of one kind are kept;
                  a label is never twice; `--parent` does not copy the parent's;
                  a kind no plan carries, or a word its kind refuses, is refused
                  before anything is made.
  LabelVerb       `label ID KIND=WORD` adds one and says what the plan carries;
                  `--remove` removes it, the block with the last one, keeping
                  every other line; a session that is not there is refused.
  EarlierShape    A plan still holding `Topic` or `Kind` as keys is in an earlier
                  shape, named as such, and is not rewritten.
  NearMatch       A topic one or two edits from one the project uses is warned
                  about naming both, and is still written; an equal topic, or a
                  far one, is not warned about; another kind is not compared.
  LabelsListing   `labels` lists the project's labels by kind with how many
                  sessions and how many of them are queued, the largest first;
                  another project's labels are not listed; none says so.
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
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import modules.process.project.services.registry as registry
import modules.process.session.services.ensure as session_ensure
import modules.process.session.services.label as session_label
import modules.process.session.services.labels as session_labels
import modules.knowledge.documentation.plan.services.plan as session_plan
import modules.process.session.services.plan_labels as session_plan_labels
import modules.process.session.services.plan_priority as session_plan_priority
from modules.knowledge.documentation.primitive.label import Label, Labels
from modules.knowledge.documentation.plan.primitive.topic import Topic
import re


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.git_project("project-x")
        project = unittest.mock.patch.object(session_ensure, "project_root", return_value=self.project)
        project.start()
        self.addCleanup(project.stop)

    def git_project(self, name: str) -> Path:
        folder = self.fake_root / name
        folder.mkdir()
        subprocess.run(["git", "init", "-q", str(folder)], check=True, capture_output=True)
        return folder

    def session(self, sid: str, status: str = "queued", labels: tuple[str, ...] = (), project: Path | None = None) -> Path:
        """A plan written by hand with LABELS, each `Kind: word`, as a block."""
        folder = memar_fs.session_dir(sid)
        folder.mkdir(parents=True)
        where = project or self.project
        block = "Labels:\n" + "".join(self.label_line(label, where) for label in labels) if labels else ""
        (folder / session_plan.PLAN_NAME).write_text(
            f"---\nTitle: T\nStatus: {status.capitalize()}\nStart Date: 2026-10-13T00:00:00Z\nProject: {project or self.project}\n{block}---\n"
            f"# T\n\n## Request\nx\n\n## Why\n\n## Steps\n\n## Next\n",
            encoding="utf-8",
            newline="\n",
        )
        return folder

    def label_line(self, spec: str, project: Path) -> str:
        """The block line of a label written `Kind: word`, defined in PROJECT's registry when it is a free word."""
        kind, word = (part.strip() for part in spec.split(":", 1))
        label, fresh = session_plan_labels.registry_for(project).resolve(f"{kind}={word}")
        if fresh is not None:
            session_plan_labels.keep_definition(project, fresh)
        return f"  - {label}\n"

    def words(self, folder: Path, kind: str) -> tuple[str, ...]:
        front = self.front(folder)
        return session_plan_labels.registry_of(front).words(session_plan_labels.labels_of(front), kind)

    def plan(self, folder: Path) -> Path:
        return folder / session_plan.PLAN_NAME

    def front(self, folder: Path) -> dict[str, str]:
        return session_plan.read_plan(self.plan(folder)).front or {}

    def labels(self, folder: Path) -> Labels:
        return session_plan_labels.labels_of(self.front(folder))

    def printed(self, call, *args, **kwargs) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            call(*args, **kwargs)
        return out.getvalue()

    def refused(self, call, *args, **kwargs) -> str:
        with self.assertRaises(SystemExit) as raised:
            call(*args, **kwargs)
        return str(raised.exception.code)


class LabelsField(Fixture):
    def test_a_topic_is_written_lower_case_with_hyphens_for_spaces(self) -> None:
        for given, written in (("Khayyam", "khayyam"), ("  Local  LSP server ", "local-lsp-server"), ("a\tb", "a-b")):
            with self.subTest(given=given):
                self.assertEqual(Topic.normalized(given), written)

    def test_a_plan_without_labels_has_none(self) -> None:
        folder = self.session("20261013T000001Z-1-0")
        self.assertFalse(self.labels(folder))
        self.assertEqual(session_plan_labels.topics_of(self.front(folder)), ())
        self.assertEqual(session_plan_labels.topics_of(None), ())

    def test_new_writes_the_labels_as_a_block_into_a_new_plan(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_ensure.ensure_session(
                "20261013T000002Z-1-0", "Title", None, labels=["Topic=Khayyam LSP", "TaskKind=Design"], project=str(self.project)
            )
        self.assertEqual(self.words(path, "Topic"), ("khayyam-lsp",))
        self.assertEqual(self.words(path, "TaskKind"), ("design",))
        self.assertRegex(self.plan(path).read_text(encoding="utf-8"), r"Labels:\n  - khayyam-lsp\([0-9a-f-]{36}\)\n  - design\([0-9a-f-]{36}\)\n---\n")
        self.assertIn("- khayyam-lsp(", (self.project / session_plan_labels.REGISTRY_FILE).read_text(encoding="utf-8"))

    def test_new_without_labels_writes_no_block(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_ensure.ensure_session("20261013T000003Z-1-0", "Title", None, project=str(self.project))
        self.assertNotIn("Labels", self.plan(path).read_text(encoding="utf-8"))
        self.assertFalse(self.labels(path))

    def test_new_adds_labels_to_a_plan_that_is_there(self) -> None:
        folder = self.session("20261013T000004Z-1-0", "active", ("Topic: docs",))
        with contextlib.redirect_stdout(io.StringIO()):
            session_ensure.ensure_session(folder.name, None, None, labels=["Topic=more", "Topic=docs"])
        self.assertEqual(self.words(folder, "Topic"), ("docs", "more"))
        self.assertEqual(session_plan.read_plan(self.plan(folder)).status, "active")

    def test_several_labels_of_one_kind_are_kept_and_none_is_twice(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_ensure.ensure_session(
                "20261013T000007Z-1-0", "Title", None, labels=["Topic=a", "Topic=b", "Topic=a"], project=str(self.project)
            )
        self.assertEqual(self.words(path, "Topic"), ("a", "b"))

    def test_a_child_opened_with_a_parent_does_not_copy_the_parents_labels(self) -> None:
        parent = self.session("20261013T000005Z-1-0", "active", ("Topic: docs",))
        with contextlib.redirect_stdout(io.StringIO()):
            _, path = session_ensure.ensure_session("20261013T000006Z-1-0", "Child", parent.name, project=str(self.project))
        self.assertFalse(self.labels(path))

    def test_a_kind_no_plan_carries_is_refused_and_nothing_is_made(self) -> None:
        text = self.refused(session_ensure.ensure_session, "20261013T000008Z-1-0", "Title", None, labels=["Colour=red"], project=str(self.project))
        self.assertIn("Colour", text)
        self.assertIn("TaskKind", text)
        self.assertFalse(memar_fs.session_dir("20261013T000008Z-1-0").exists())

    def test_a_word_its_kind_refuses_is_refused_with_the_kinds_words(self) -> None:
        text = self.refused(session_ensure.ensure_session, "20261013T000009Z-1-0", "Title", None, labels=["TaskKind=gardening"], project=str(self.project))
        self.assertIn("a kind is one of", text)

    def test_a_label_is_written_kind_equals_word(self) -> None:
        self.assertIn("KIND=WORD", self.refused(session_plan_labels.checked_label, "design", None))

    def test_a_topic_is_one_line(self) -> None:
        self.assertIn("one line", self.refused(Topic.checked, "a\nb"))
        self.assertEqual(Topic.checked("  "), "")

    def test_the_task_kind_is_the_first_judgment_kind_a_plan_carries(self) -> None:
        folder = self.session("20261013T000014Z-1-0", "queued", ("TaskKind: mechanical", "TaskKind: design"))
        self.assertEqual(session_plan_labels.task_kind_of(self.front(folder)), "design")
        folder = self.session("20261013T000015Z-1-0", "queued", ("TaskKind: mechanical",))
        self.assertEqual(session_plan_labels.task_kind_of(self.front(folder)), "mechanical")
        self.assertEqual(session_plan_labels.task_kind_of(None), "")


class LabelVerb(Fixture):
    def test_the_verb_adds_a_label_and_says_what_the_plan_carries(self) -> None:
        folder = self.session("20261013T000010Z-1-0", "active")
        text = self.printed(session_label.set_session_label, folder.name, "Topic=Docs Cleanup", False)
        self.assertIn(f"{folder.name}  added docs-cleanup", text)
        self.assertEqual(self.words(folder, "Topic"), ("docs-cleanup",))
        text = self.printed(session_label.set_session_label, folder.name, "TaskKind=critique", False)
        self.assertEqual(self.words(folder, "TaskKind"), ("critique",))
        self.assertIn("docs-cleanup", text)
        self.assertIn("critique", text)

    def test_adding_a_label_the_plan_has_changes_nothing(self) -> None:
        folder = self.session("20261013T000016Z-1-0", "queued", ("Topic: docs",))
        before = self.plan(folder).read_text(encoding="utf-8")
        self.printed(session_label.set_session_label, folder.name, "Topic=docs", False)
        self.assertEqual(self.plan(folder).read_text(encoding="utf-8"), before)

    def test_remove_takes_the_label_out_and_the_block_with_the_last_one(self) -> None:
        folder = self.session("20261013T000011Z-1-0", "queued", ("Topic: docs", "TaskKind: design"))
        before = self.plan(folder).read_text(encoding="utf-8")
        text = self.printed(session_label.set_session_label, folder.name, "Topic=docs", True)
        self.assertIn(f"{folder.name}  removed docs", text)
        after = self.plan(folder).read_text(encoding="utf-8")
        self.assertEqual(after, re.sub(r"  - docs\([0-9a-f-]{36}\)\n", "", before))
        self.printed(session_label.set_session_label, folder.name, "TaskKind=design", True)
        self.assertEqual(self.plan(folder).read_text(encoding="utf-8"), re.sub(r"Labels:\n(  - [^\n]*\n)+", "", before))
        self.assertFalse(self.labels(folder))

    def test_removing_a_label_the_plan_lacks_changes_nothing(self) -> None:
        folder = self.session("20261013T000017Z-1-0", "queued", ("Topic: docs",))
        before = self.plan(folder).read_text(encoding="utf-8")
        text = self.printed(session_label.set_session_label, folder.name, "Topic=other", True)
        self.assertIn("does not carry", text)
        self.assertEqual(self.plan(folder).read_text(encoding="utf-8"), before)

    def test_the_other_front_matter_and_the_body_are_kept(self) -> None:
        folder = self.session("20261013T000012Z-1-0", "queued")
        session_plan_priority.set_priority(self.plan(folder), 8)
        self.printed(session_label.set_session_label, folder.name, "Topic=docs", False)
        front = self.front(folder)
        self.assertEqual((front["priority"], front["title"]), ("8", "T"))
        self.assertEqual(session_plan.read_plan(self.plan(folder)).status, "queued")
        self.assertTrue(self.plan(folder).read_text(encoding="utf-8").endswith("## Next\n"))

    def test_a_crlf_plan_keeps_its_line_endings(self) -> None:
        folder = self.session("20261013T000018Z-1-0", "queued")
        text = self.plan(folder).read_text(encoding="utf-8").replace("\n", "\r\n")
        self.plan(folder).write_bytes(text.encode("utf-8"))
        self.printed(session_label.set_session_label, folder.name, "Topic=docs", False)
        data = self.plan(folder).read_bytes()
        self.assertRegex(data, rb"Labels:\r\n  - docs\([0-9a-f-]{36}\)\r\n---")
        self.assertNotIn(b"\n", data.replace(b"\r\n", b""))

    def test_a_session_that_is_not_there_is_refused(self) -> None:
        self.assertIn("no session", self.refused(session_label.set_session_label, "20261013T000013Z-1-0", "Topic=docs", False))


class EarlierShape(Fixture):
    def test_a_plan_holding_a_topic_or_kind_key_is_in_an_earlier_shape_and_is_not_rewritten(self) -> None:
        for key in ("Topic: docs", "Kind: design"):
            with self.subTest(key=key):
                folder = self.session(f"20261013T0000{19 if key.startswith('Topic') else 20}Z-9-0", "queued")
                text = self.plan(folder).read_text(encoding="utf-8").replace("---\n# T", f"{key}\n---\n# T", 1)
                self.plan(folder).write_text(text, encoding="utf-8", newline="\n")
                problem = session_plan.plan_file_problem(self.plan(folder))
                self.assertIn("earlier shape", problem)
                self.assertIn("labels", problem)
                self.assertIn("earlier shape", self.refused(session_label.set_session_label, folder.name, "Topic=x", False))
                self.assertEqual(self.plan(folder).read_text(encoding="utf-8"), text)


class NearMatch(Fixture):
    def test_a_topic_one_or_two_edits_from_one_in_use_is_warned_about_and_still_written(self) -> None:
        self.session("20261013T000020Z-1-0", "queued", ("Topic: khayyam",))
        for index, typed in enumerate(("khayam", "khayyyam", "kayyam", "khayymal")):
            with self.subTest(typed=typed):
                folder = self.session(f"20261013T0000{21 + index}Z-1-0", "active")
                text = self.printed(session_label.set_session_label, folder.name, f"Topic={typed}", False)
                self.assertIn(typed, text)
                self.assertIn("khayyam", text)
                self.assertIn("near", text)
                self.assertEqual(self.words(folder, "Topic"), (typed,))

    def test_new_warns_the_same_way(self) -> None:
        self.session("20261013T000030Z-1-0", "queued", ("Topic: khayyam",))
        text = self.printed(session_ensure.ensure_session, "20261013T000031Z-1-0", "Title", None, labels=["Topic=khayam"], project=str(self.project))
        self.assertIn("near", text)
        self.assertIn("khayyam", text)

    def test_an_equal_topic_or_a_far_one_is_not_warned_about(self) -> None:
        self.session("20261013T000040Z-1-0", "queued", ("Topic: khayyam",))
        for index, typed in enumerate(("khayyam", "docs-cleanup")):
            with self.subTest(typed=typed):
                folder = self.session(f"20261013T0000{41 + index}Z-1-0", "active")
                self.assertNotIn("near", self.printed(session_label.set_session_label, folder.name, f"Topic={typed}", False))

    def test_another_projects_topics_are_not_compared(self) -> None:
        other = self.git_project("project-y")
        self.session("20261013T000050Z-1-0", "queued", ("Topic: khayyam",), project=other)
        folder = self.session("20261013T000051Z-1-0", "active")
        self.assertNotIn("near", self.printed(session_label.set_session_label, folder.name, "Topic=khayam", False))

    def test_a_task_kind_is_not_compared_with_topics(self) -> None:
        self.session("20261013T000052Z-1-0", "queued", ("Topic: design",))
        folder = self.session("20261013T000053Z-1-0", "active")
        self.assertNotIn("near", self.printed(session_label.set_session_label, folder.name, "TaskKind=design", False))

    def test_edit_distance_counts_insertions_deletions_and_substitutions(self) -> None:
        for one, two, distance in (("a", "a", 0), ("abc", "abd", 1), ("abc", "abcd", 1), ("abc", "ac", 1), ("kitten", "sitting", 3)):
            with self.subTest(one=one, two=two):
                self.assertEqual(session_label.edit_distance(one, two), distance)


class LabelsListing(Fixture):
    def listed(self, project: Path | None = None) -> str:
        return self.printed(session_labels.list_labels, str(project or self.project))

    def test_labels_are_listed_by_kind_with_their_counts_the_largest_first(self) -> None:
        self.session("20261013T000060Z-1-0", "queued", ("Topic: docs",))
        self.session("20261013T000061Z-1-0", "queued", ("Topic: khayyam", "TaskKind: design"))
        self.session("20261013T000062Z-1-0", "active", ("Topic: khayyam",))
        self.session("20261013T000063Z-1-0", "queued", ("Topic: khayyam",))
        self.session("20261013T000064Z-1-0", "queued")
        lines = [line for line in self.listed().splitlines() if line.strip()]
        self.assertEqual(len(lines), 3)
        self.assertIn("khayyam(", lines[0])
        self.assertIn("3 sessions", lines[0])
        self.assertIn("2 queued", lines[0])
        self.assertTrue(lines[1].startswith("docs(") or lines[1].startswith("design("))
        self.assertIn("1 session", lines[2])
        self.assertNotIn("1 sessions", lines[2])

    def test_the_project_is_named_by_a_name_or_a_folder_and_never_by_the_calling_folder(self) -> None:
        registry.add_project("project-x", self.project)
        self.session("20261013T000070Z-1-0", "queued", ("Topic: docs",))
        parser = argparse.ArgumentParser()
        command = session_labels.describe(parser.add_subparsers())
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            command(parser.parse_args(["labels", "--project", "project-x"]))
        self.assertIn("docs", out.getvalue())
        for missing in (None, "", " "):
            with self.subTest(missing=missing):
                with self.assertRaises(SystemExit) as raised:
                    self.printed(session_labels.list_labels, missing)
                self.assertIn("--project" if missing is None else "--project-path", str(raised.exception.code))

    def test_another_projects_labels_are_not_listed(self) -> None:
        other = self.git_project("project-y")
        self.session("20261013T000070Z-1-0", "queued", ("Topic: theirs",), project=other)
        self.session("20261013T000071Z-1-0", "queued", ("Topic: ours",))
        text = self.listed()
        self.assertIn("ours", text)
        self.assertNotIn("theirs", text)
        self.assertIn("theirs", self.listed(other))

    def test_no_label_in_use_is_said(self) -> None:
        self.session("20261013T000080Z-1-0", "queued")
        self.assertIn("no label", self.listed())


if __name__ == "__main__":
    unittest.main()
