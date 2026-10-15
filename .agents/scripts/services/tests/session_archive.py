#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for keeping a session's records in `services/session_archive.py`.

    python .agents/scripts/services/tests/session_archive.py

The subject is keeping a finished session's records in its project — the
owner's ruling of 2026-10-14 that `session_archive`'s docstring states — named
for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
a scratch folder, and the project and its registry entry are made inside it.

What is pinned, and what each pin is for:

  WhatIsKept      A session's plan, its report, and each file its report
                  links to inside the folder are copied to the project's
                  .agents/sessions/<id>/; the claim, a file only mentioned,
                  and a link that leaves the folder or the disk are not. The
                  copied plan names its project by its registered name and is
                  otherwise as written; the report is copied as it is. Keeping
                  again writes what the folder holds now; a dry run writes
                  nothing and says what would be kept.
  WhenNotOwed     A project whose preferences say `records: off`, a plan that
                  names no project, and a folder with no plan owe no records,
                  and nothing is written.
  WhenRefused     A `records` value it may not take, a project folder that is
                  not on this computer, and a project with no registered name
                  are refused, with why, and nothing is written: a record that
                  cannot be kept is not silently dropped.
  RelatedSessions `archive` keeps the session named and every session whose
                  Parent chain leads to it, and prints where each one's
                  records are, for the commit.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import io
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

import machine.fs_memar as memar_fs
import services.session_archive as session_archive
from services.project_registry import add_project

NAME = "example"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.fake_root / "work" / NAME
        (self.project / ".agents" / "memar").mkdir(parents=True)
        add_project(NAME, self.project)

    def prefer(self, text: str) -> None:
        (self.project / ".agents" / "memar" / "preferences.md").write_text(
            f"---\n{text}\n---\n# Memar preferences\n", encoding="utf-8", newline="\n"
        )

    def session(self, sid: str, *, project: str | None = None, parent: str = "", report: str = "") -> Path:
        folder = memar_fs.session_dir(sid, create=True)
        named = str(self.project) if project is None else project
        front = ["---", f"Title: Task {sid}", "Status: Complete", "Opened: 2026-10-14T00:00:00Z"]
        if named:
            front.append(f"Project: {named}")
        if parent:
            front.append(f"Parent: {parent}")
        front.append("---")
        (folder / "plan.md").write_bytes(("\r\n".join([*front, f"# Task {sid}", "", "## Request", "Do it.", ""])).encode("utf-8"))
        (folder / "report.md").write_text(
            report or "---\nTitle: T\nStatus: Complete\n---\n# Report\n\n## Result\nDone.\n",
            encoding="utf-8",
            newline="\n",
        )
        (folder / "claim").write_text("host: here\npid: 1\n", encoding="utf-8", newline="\n")
        return folder

    def kept_at(self, sid: str) -> Path:
        return self.project / ".agents" / "sessions" / sid


class WhatIsKept(Fixture):
    REPORT = (
        "---\nTitle: T\nStatus: Complete\n---\n# Report\n\n## Result\n"
        "The entry is [drafted](docs/entry.md#first), the script [here](services/fix.py).\n"
        "Scratch left: docs/scratch.txt. Elsewhere: [other](../other/plan.md), [web](https://example.org/x),\n"
        "[top](#result), [plan](plan.md), [missing](docs/gone.md).\n"
    )

    def make(self) -> Path:
        folder = self.session("20261014-T100000Z-1", report=self.REPORT)
        (folder / "docs").mkdir()
        (folder / "services").mkdir()
        (folder / "docs" / "entry.md").write_text("# Entry\n", encoding="utf-8", newline="\n")
        (folder / "docs" / "scratch.txt").write_text("noise\n", encoding="utf-8", newline="\n")
        (folder / "services" / "fix.py").write_text("print('fix')\n", encoding="utf-8", newline="\n")
        return folder

    def test_the_plan_the_report_and_the_linked_files_are_kept_and_nothing_else(self) -> None:
        folder = self.make()
        kept = session_archive.keep_records(folder)
        self.assertIs(kept.outcome, session_archive.Outcome.KEPT, kept.why)
        where = self.kept_at(folder.name)
        self.assertEqual(kept.folder, where)
        found = sorted(path.relative_to(where).as_posix() for path in where.rglob("*") if path.is_file())
        self.assertEqual(found, ["docs/entry.md", "plan.md", "report.md", "services/fix.py"])

    def test_the_kept_plan_names_its_project_by_name_and_is_otherwise_as_written(self) -> None:
        folder = self.make()
        session_archive.keep_records(folder)
        original = (folder / "plan.md").read_bytes().decode("utf-8")
        kept = (self.kept_at(folder.name) / "plan.md").read_bytes().decode("utf-8")
        self.assertIn(f"Project: {NAME}\r\n", kept)
        self.assertNotIn(str(self.project), kept)
        self.assertEqual(kept, original.replace(f"Project: {self.project}", f"Project: {NAME}"))

    def test_the_report_is_kept_as_it_is(self) -> None:
        folder = self.make()
        session_archive.keep_records(folder)
        self.assertEqual((self.kept_at(folder.name) / "report.md").read_bytes(), (folder / "report.md").read_bytes())

    def test_a_dry_run_says_what_would_be_kept_and_writes_nothing(self) -> None:
        folder = self.make()
        kept = session_archive.keep_records(folder, write=False)
        self.assertIs(kept.outcome, session_archive.Outcome.KEPT)
        self.assertEqual(kept.folder, self.kept_at(folder.name))
        self.assertEqual(
            sorted(path.as_posix() for path in kept.files), ["docs/entry.md", "plan.md", "report.md", "services/fix.py"]
        )
        self.assertFalse((self.project / ".agents" / "sessions").exists())

    def test_keeping_again_writes_what_the_folder_holds_now(self) -> None:
        folder = self.make()
        session_archive.keep_records(folder)
        (folder / "report.md").write_text("---\nTitle: T\nStatus: Complete\n---\n# Report\nLater.\n", encoding="utf-8", newline="\n")
        session_archive.keep_records(folder)
        self.assertIn("Later.", (self.kept_at(folder.name) / "report.md").read_text(encoding="utf-8"))


class WhenNotOwed(Fixture):
    def test_a_project_that_says_off_keeps_none(self) -> None:
        self.prefer("records: off")
        folder = self.session("20261014-T100001Z-2")
        kept = session_archive.keep_records(folder)
        self.assertIs(kept.outcome, session_archive.Outcome.NOT_OWED)
        self.assertIn("records: off", kept.why)
        self.assertFalse(self.kept_at(folder.name).exists())

    def test_an_empty_key_and_on_keep_them(self) -> None:
        for text in ("records:", "records: on", "sessions:"):
            with self.subTest(text=text):
                self.prefer(text)
                folder = self.session(f"20261014-T10000{len(text) % 10}Z-3")
                self.assertIs(session_archive.keep_records(folder).outcome, session_archive.Outcome.KEPT)

    def test_a_plan_that_names_no_project_owes_none(self) -> None:
        folder = self.session("20261014-T100002Z-4", project="")
        kept = session_archive.keep_records(folder)
        self.assertIs(kept.outcome, session_archive.Outcome.NOT_OWED)
        self.assertFalse((self.project / ".agents" / "sessions").exists())

    def test_a_folder_with_no_plan_owes_none(self) -> None:
        folder = memar_fs.session_dir("20261014-T100003Z-5", create=True)
        self.assertIs(session_archive.keep_records(folder).outcome, session_archive.Outcome.NOT_OWED)


class WhenRefused(Fixture):
    def assertRefused(self, folder: Path, words: str) -> None:
        kept = session_archive.keep_records(folder)
        self.assertIs(kept.outcome, session_archive.Outcome.REFUSED)
        self.assertIn(words, kept.why)
        self.assertFalse(self.kept_at(folder.name).exists())

    def test_a_value_records_may_not_take_is_refused(self) -> None:
        self.prefer("records: maybe")
        self.assertRefused(self.session("20261014-T100004Z-6"), "maybe")

    def test_a_project_not_on_this_computer_is_refused(self) -> None:
        self.assertRefused(self.session("20261014-T100005Z-7", project=str(self.fake_root / "elsewhere")), "not a folder")

    def test_a_project_with_no_registered_name_is_refused(self) -> None:
        other = self.fake_root / "work" / "unnamed"
        other.mkdir(parents=True)
        folder = self.session("20261014-T100006Z-8", project=str(other))
        kept = session_archive.keep_records(folder)
        self.assertIs(kept.outcome, session_archive.Outcome.REFUSED)
        self.assertIn("memar project add", kept.why)
        self.assertFalse((other / ".agents" / "sessions").exists())


class RelatedSessions(Fixture):
    def run_archive(self, sid: str) -> str:
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        run = session_archive.describe(verbs)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            run(parser.parse_args([session_archive.ARCHIVE_COMMAND, "--session-id", sid]))
        return out.getvalue()

    def test_the_session_and_those_its_parent_chain_leads_to_are_kept_and_named(self) -> None:
        top = self.session("20261014-T110000Z-10")
        child = self.session("20261014-T110001Z-11", parent=top.name)
        grandchild = self.session("20261014-T110002Z-12", parent=child.name)
        other = self.session("20261014-T110003Z-13")
        said = self.run_archive(top.name)
        for each in (top, child, grandchild):
            self.assertTrue((self.kept_at(each.name) / "plan.md").is_file(), each.name)
            self.assertIn(str(self.kept_at(each.name)), said)
        self.assertFalse(self.kept_at(other.name).exists())

    def test_a_refused_session_is_named_with_why_and_fails_the_verb(self) -> None:
        top = self.session("20261014-T110004Z-14", project=str(self.fake_root / "elsewhere"))
        with self.assertRaises(SystemExit):
            self.run_archive(top.name)

    def test_an_unknown_session_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            self.run_archive("20261014-T110005Z-15")


if __name__ == "__main__":
    unittest.main(verbosity=2)
