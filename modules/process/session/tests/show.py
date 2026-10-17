#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for reading a session's records in `modules/process/session/services/show.py`.

    python modules/process/session/tests/show.py

The subject is `memar session show`, which returns a session's plan and report,
or the files an agent asks for, from the main repository's temp first and then
from the records branch (owner, 2026-10-15). It is named for the file that
holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder: the Memar root is patched onto
a scratch folder, and the project, its repository and its registry entry are
made inside it.

What is pinned, and what each pin is for:

  ReadsTempFirst   A session whose folder is still in temp is read from the
                   folder, even where the branch holds an older copy; a file
                   the folder lacks is read from the branch; each file says
                   where it came from.
  ReadsTheBranch   A session whose folder is gone is read from the project's
                   records branch: the plan, the report, and any file asked
                   for by its path from the session's folder; the plan as kept
                   names the project by name.
  Refusals         A project must be named, by `--project` or
                   `--project-path`, and the folder this runs in is never
                   read. A file that is nowhere, a path that leaves the
                   session's folder, a session in neither place, and a
                   project with no branch are refused saying where each was
                   looked for.
  HandBack         `--hand-back` prints the report's Status, its path and the
                   lines under Decisions needed, and no other line of the
                   report; a report that is not a hand-back is named with why.
  Listing          `--list` names the files the session has, from the folder
                   when it is in temp, else from the branch.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import contextlib
import io
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
SCRIPTS = TESTS.parents[3] / ".agents" / "scripts"
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))  # the checkout's top, where `modules/` is imported from
sys.dont_write_bytecode = True

from machine.fs_test_scratch import suite_scratch

import machine.fs_memar as memar_fs
import modules.process.session.services.archive as session_archive
import modules.process.session.services.show as session_show
from modules.process.project.services.registry import add_project

NAME = "example"
SID = "20261015-T100000Z-1"


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.project = self.fake_root / "work" / NAME
        self.project.mkdir(parents=True)
        add_project(NAME, self.project)
        for args in (["init", "-q", "-b", "main"], ["config", "user.name", "Test"], ["config", "user.email", "t@example.org"]):
            subprocess.run(["git", "-C", str(self.project), *args], check=True, capture_output=True)

    def session(self, sid: str = SID) -> Path:
        folder = memar_fs.session_dir(sid, create=True)
        (folder / "plan.md").write_bytes(
            f"---\nTitle: T\nStatus: Complete\nOpened: x\nProject: {self.project}\n---\n# T\n\n## Request\nPlan text.\n".encode("utf-8")
        )
        (folder / "report.md").write_bytes(b"---\nTitle: T\nStatus: Complete\n---\n# Report\nBranch report.\n")
        (folder / "docs").mkdir()
        (folder / "docs" / "note.md").write_bytes("# Note\nnaïve — text\n".encode("utf-8"))
        return folder

    def archived_and_gone(self, sid: str = SID) -> Path:
        folder = self.session(sid)
        self.assertEqual(session_archive.keep_records([folder])[0].outcome, session_archive.Outcome.KEPT)
        shutil.rmtree(folder)
        return folder

    def show(self, *arguments: str, project: str | None = "path") -> tuple[str, str | None]:
        """What `show` printed and, when it stopped, why."""
        parser = argparse.ArgumentParser()
        verbs = parser.add_subparsers()
        run = session_show.describe(verbs)
        flags = {"path": ["--project-path", str(self.project)], "name": ["--project", NAME], None: []}[project]
        out = io.StringIO()
        try:
            with contextlib.redirect_stdout(out):
                run(parser.parse_args([session_show.SHOW_COMMAND, "--session-id", SID, *flags, *arguments]))
        except SystemExit as stopped:
            return out.getvalue(), str(stopped.code)
        return out.getvalue(), None


class ReadsTempFirst(Fixture):
    def test_a_folder_still_in_temp_is_read_from_the_folder_even_where_the_branch_has_an_older_copy(self) -> None:
        folder = self.session()
        session_archive.keep_records([folder])
        (folder / "report.md").write_bytes(b"---\nTitle: T\nStatus: Complete\n---\n# Report\nFolder report.\n")
        said, stopped = self.show()
        self.assertIsNone(stopped)
        self.assertIn("Folder report.", said)
        self.assertNotIn("Branch report.", said)
        self.assertIn(str(folder / "report.md"), said)

    def test_a_file_the_folder_lacks_is_read_from_the_branch_and_says_so(self) -> None:
        folder = self.session()
        session_archive.keep_records([folder])
        (folder / "report.md").unlink()
        said, stopped = self.show()
        self.assertIsNone(stopped)
        self.assertIn("Plan text.", said)
        self.assertIn("Branch report.", said)
        self.assertIn(session_archive.reference(SID) + "report.md", said)


class ReadsTheBranch(Fixture):
    def test_the_plan_and_the_report_are_returned_by_default(self) -> None:
        self.archived_and_gone()
        said, stopped = self.show()
        self.assertIsNone(stopped)
        self.assertIn("Plan text.", said)
        self.assertIn("Branch report.", said)
        self.assertIn(f"Project: {NAME}", said)
        self.assertLess(said.index("Plan text."), said.index("Branch report."))

    def test_a_named_file_is_returned_from_the_sessions_folder_and_only_that_one(self) -> None:
        self.archived_and_gone()
        said, stopped = self.show("--file", "docs/note.md")
        self.assertIsNone(stopped)
        self.assertIn("naïve — text", said)
        self.assertNotIn("Plan text.", said)

    def test_the_project_may_be_named_by_name(self) -> None:
        self.archived_and_gone()
        said, stopped = self.show(project="name")
        self.assertIsNone(stopped)
        self.assertIn("Plan text.", said)

    def test_each_file_is_headed_by_its_name_and_where_it_came_from(self) -> None:
        self.archived_and_gone()
        said, _ = self.show()
        self.assertIn(f"=== plan.md ({session_archive.reference(SID)}plan.md)", said)


class Refusals(Fixture):
    def test_no_project_is_refused_and_the_folder_this_runs_in_is_not_read(self) -> None:
        self.archived_and_gone()
        _, stopped = self.show(project=None)
        self.assertIn("--project", stopped or "")

    def test_a_file_that_is_nowhere_is_refused_saying_where_it_was_looked_for(self) -> None:
        self.archived_and_gone()
        _, stopped = self.show("--file", "docs/none.md")
        self.assertIn("docs/none.md", stopped or "")
        self.assertIn("dev-knowledge", stopped or "")

    def test_a_path_that_leaves_the_sessions_folder_is_refused(self) -> None:
        self.archived_and_gone()
        for bad in ("../x.md", "/etc/passwd", "docs/../../x.md", "C:\\x.md", ""):
            with self.subTest(bad=bad):
                _, stopped = self.show("--file", bad)
                self.assertIsNotNone(stopped)

    def test_a_session_in_neither_place_is_refused(self) -> None:
        subprocess.run(["git", "-C", str(self.project), "commit", "-q", "--allow-empty", "-m", "base"], check=True, capture_output=True)
        _, stopped = self.show()
        self.assertIn(SID, stopped or "")

    def test_a_project_with_no_records_branch_says_so(self) -> None:
        _, stopped = self.show()
        self.assertIn("dev-knowledge", stopped or "")


class Listing(Fixture):
    def test_a_folder_in_temp_is_listed_from_the_folder(self) -> None:
        folder = self.session()
        (folder / "temp").mkdir()
        (folder / "temp" / "draft.md").write_bytes(b"d\n")
        said, stopped = self.show("--list")
        self.assertIsNone(stopped)
        self.assertEqual(said.splitlines(), sorted(["docs/note.md", "plan.md", "report.md", "temp/draft.md"]))

    def test_a_folder_gone_is_listed_from_the_branch(self) -> None:
        self.archived_and_gone()
        said, stopped = self.show("--list")
        self.assertIsNone(stopped)
        self.assertEqual(said.splitlines(), ["docs/note.md", "plan.md", "report.md"])


class HandBack(Fixture):
    def report(self, text: bytes) -> None:
        folder = self.session()
        (folder / "report.md").write_bytes(text)

    def test_only_the_status_the_path_and_the_decisions_are_printed(self) -> None:
        self.report(b"---\nTitle: T\nStatus: Complete\n---\n# Report\nSECRET body.\n\n## Decisions needed\n- Q1 a | b (recommended).\n")
        said, stopped = self.show("--hand-back")
        self.assertIsNone(stopped)
        lines = said.splitlines()
        self.assertEqual(lines[0], "Status: complete")
        self.assertTrue(lines[1].startswith("Report: ") and lines[1].endswith("report.md"))
        self.assertEqual(lines[2:], ["- Q1 a | b (recommended)."])
        self.assertNotIn("SECRET", said)

    def test_a_report_with_too_many_decision_lines_is_named_not_a_hand_back(self) -> None:
        many = "".join(f"- Q{n}.\n" for n in range(40))
        self.report(f"---\nTitle: T\nStatus: Complete\n---\n# Report\n\n## Decisions needed\n{many}".encode("utf-8"))
        said, stopped = self.show("--hand-back")
        self.assertIsNone(stopped)
        self.assertIn("Not a hand-back:", said)

    def test_a_report_with_no_status_is_named_not_a_hand_back(self) -> None:
        self.report(b"---\nTitle: T\nStatus:\n---\n# Report\n")
        said, _ = self.show("--hand-back")
        self.assertIn("Not a hand-back: report.md has no Status", said)

    def test_a_session_with_no_folder_is_refused(self) -> None:
        said, stopped = self.show("--hand-back")
        self.assertEqual(said, "")
        self.assertIn("no folder in temp", stopped)


if __name__ == "__main__":
    unittest.main(verbosity=2)
