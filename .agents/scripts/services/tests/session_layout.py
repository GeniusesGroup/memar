#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for what stands at a session folder's top, and where the rest goes, in `services/session_layout.py`.

    python .agents/scripts/services/tests/session_layout.py

The subject is the layout every session service reads,
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes anything: names are read and compared.

What is pinned, and what each pin is for:

  TopHoldsOnly   The top holds plan.md and report.md, and the claim Memar
                 writes there while an agent holds the task (with its
                 takeover), and nothing else; the names are the ones the
                 services that write those files declare.
  KindsGoToRoles Each kind's folder is a module role folder; a note (.md)
                 goes in docs/ and a script (.py, .mjs, .js, .ps1, .sh) in
                 services/ (owner, 2026-10-14); a file of no kind named here,
                 and a folder, have no kind, so nothing guesses where they go.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# This suite lives in the `tests/` folder of the shelf that owns its subject, so
# the scripts folder is two levels up. Running a file puts its OWN folder on the
# module search path and not its parent's, which is the one line this needs and
# the reason it carries one.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

import services.session_layout as session_layout
from services.module_folders import ROLE_FOLDERS
from services.session_claim import CLAIM_NAME, CLAIM_TAKEOVER_NAME
from services.session_plan import PLAN_NAME
from services.session_report import REPORT_NAME


class TopHoldsOnly(unittest.TestCase):
    def test_the_top_holds_the_plan_the_report_and_the_claim(self) -> None:
        self.assertEqual(session_layout.TOP_NAMES, (PLAN_NAME, REPORT_NAME, CLAIM_NAME, CLAIM_TAKEOVER_NAME))
        self.assertEqual((PLAN_NAME, REPORT_NAME, CLAIM_NAME), ("plan.md", "report.md", "claim"))

    def test_a_role_folder_belongs_at_the_top_and_a_stray_does_not(self) -> None:
        for name in (*session_layout.TOP_NAMES, *ROLE_FOLDERS):
            with self.subTest(name=name):
                self.assertTrue(session_layout.belongs_at_top(name))
        for name in ("entry.md", "make_reviews.py", "msg1.txt", "scratch", "Plan.md"):
            with self.subTest(name=name):
                self.assertFalse(session_layout.belongs_at_top(name))


class KindsGoToRoles(unittest.TestCase):
    def test_each_kinds_folder_is_a_role_folder(self) -> None:
        for kind in session_layout.KINDS:
            with self.subTest(kind=kind.name):
                self.assertIn(kind.folder, ROLE_FOLDERS)

    def test_a_note_goes_in_docs_and_a_script_in_services(self) -> None:
        for name, folder in (
            ("entry.md", "docs"),
            ("NOTES.MD", "docs"),
            ("make_reviews.py", "services"),
            ("probe.mjs", "services"),
            ("run.js", "services"),
            ("go.ps1", "services"),
            ("go.sh", "services"),
        ):
            with self.subTest(name=name):
                kind = session_layout.kind_of(name)
                self.assertIsNotNone(kind)
                self.assertEqual(kind.folder, folder)

    def test_a_file_of_no_kind_named_here_has_none(self) -> None:
        for name in ("msg1.txt", "run.log", "c1.plan.json", "a.diff", "claim.pyc", "README"):
            with self.subTest(name=name):
                self.assertIsNone(session_layout.kind_of(name))

    def test_the_kinds_read_as_one_line_for_the_help(self) -> None:
        self.assertEqual(
            session_layout.kinds_listing(),
            "a note (.md) in docs/, a script (.py, .mjs, .js, .ps1, .sh) in services/",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
