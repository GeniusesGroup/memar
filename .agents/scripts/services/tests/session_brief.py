#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the brief that hands a session to a sub-agent, in `services/session_brief.py`.

    python .agents/scripts/services/tests/session_brief.py

The subject is the one text a delegating session hands over, named for the
file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
That `new --parent` prints it is pinned in `session_new`'s suite.

Nothing here writes outside its scratch folder: the Memar root is patched onto
one, made under the folder `machine/fs_test_scratch.py` names, and removed
again.

What is pinned, and what each pin is for:

  OneText          The brief is one line holding the session's id where the
                   task is named and continued, the skill to load, the
                   plan, its Request, that nothing but the plan and the
                   report stands at the folder's top, the report, and the
                   session help it points to, and the check that an ideation, design, or
                   critique Request first meets what the skill requires of
                   it; it carries nothing of the task itself.
  ReprintedByBrief `brief ID` prints that text alone for a session folder that
                   is there with its plan, in Memar's own root or a project's
                   location, and refuses an id with no session folder or
                   shaped like a path, and a folder with no plan.md, naming
                   `new --title T --parent ID` as the way to open one.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

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
import services.session_brief as session_brief
from services.session_location import register
from services.session_plan import PLAN_NAME, plan_skeleton

SID = "20261011-T000000Z-1"
BRIEF = (
    "Load the Memar skill: run `memar content path .agents/skills/memar/SKILL.md` and follow the file it prints. "
    f"Your task is session {SID}: run `memar session new --session-id {SID}`, read the plan.md it names, "
    "and do what its Request says, without rewriting that Request. "
    "Put nothing at the session folder's top but plan.md and report.md: anything else you make goes in "
    "the role folder of its kind, as `memar session --help` says. "
    "If the Request ideates, designs, or critiques, first check that you read in this context what the skill "
    "names for that and run on the model it requires; where either fails, end Blocked saying which. "
    "End with its report.md and Status as `memar session --help` says: write them where you may write files; "
    "where you may only return text, return the report as your final text, and the delegating session "
    "writes it as report.md before its next step."
)


class Fixture(unittest.TestCase):
    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, "memar_root", return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)

    def printed(self, session_id: str) -> str:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            session_brief.print_brief(session_id)
        return out.getvalue()


class OneText(Fixture):
    def test_the_brief_is_one_line_naming_the_session_and_nothing_of_its_task(self) -> None:
        self.assertEqual(session_brief.brief_text(SID), BRIEF)
        self.assertNotIn("\n", session_brief.brief_text(SID))


class ReprintedByBrief(Fixture):
    def test_brief_prints_the_text_alone_for_a_session_that_is_there(self) -> None:
        folder = memar_fs.session_dir(SID, create=True)
        (folder / PLAN_NAME).write_text(
            plan_skeleton("Delegated", "2026-10-11T00:00:00Z", self.fake_root), encoding="utf-8", newline="\n"
        )
        self.assertEqual(self.printed(SID), BRIEF + "\n")

    def test_a_session_with_no_plan_is_refused_naming_how_to_open_one(self) -> None:
        memar_fs.session_dir(SID, create=True)
        with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit) as refused:
            session_brief.print_brief(SID)
        self.assertEqual(out.getvalue(), "")
        self.assertIn(f"no task to hand over in {SID}", str(refused.exception.code))
        self.assertIn("`memar session new --title T --parent ID --project NAME` (or `--project-path PATH`)", str(refused.exception.code))

    def test_brief_finds_a_session_in_a_project_location(self) -> None:
        location = self.fake_root / "project" / "sessions"
        folder = location / "my-task"
        folder.mkdir(parents=True)
        (folder / PLAN_NAME).write_text(
            plan_skeleton("Named", "2026-10-11T00:00:00Z", self.fake_root / "project"), encoding="utf-8", newline="\n"
        )
        register(location)
        self.assertEqual(self.printed("my-task"), session_brief.brief_text("my-task") + "\n")

    def test_an_id_with_no_session_folder_or_shaped_like_a_path_is_refused(self) -> None:
        for bad in (SID, "a/b", ".."):
            with self.subTest(bad=bad):
                with contextlib.redirect_stdout(io.StringIO()) as out, self.assertRaises(SystemExit):
                    session_brief.print_brief(bad)
                self.assertEqual(out.getvalue(), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
