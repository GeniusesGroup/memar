#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the session record types in `services/session_record.py`.

    python .agents/scripts/services/tests/session_record.py

The subject is the shape of a session's plan.md and report.md, declared once,
named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes.

What is pinned, and what each pin is for:

PlanRecord    plan.md: the front-matter keys in the order a new plan
                 writes them, each with a description, and the four parts; its
                 Statuses are those the table gives a session plan.
  ReportRecord  report.md: the session's id, the Title and Status keys, the
                 four parts, the `Decisions needed` hand-back part and its
                 ten-line limit; its Statuses are those the table gives a
                 session report.
  TheSessionId  Both records name the session they belong to, in the same
                 front matter and from the one declaration.
  Outline       The shape rendered for a help text names every key and every
                 part, produced from the record and kept nowhere else.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
# The scripts folder is two levels up from this suite's folder; running a file
# puts its own folder on the module search path, not its parent's.
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from services.session_record import PLAN, REPORT, PlanKey, ReportKey, SESSION_FIELD
from services.status import Kind, Status


class PlanRecord(unittest.TestCase):
    def test_the_file_and_the_parts(self) -> None:
        self.assertEqual(PLAN.file_name, "plan.md")
        self.assertEqual(PLAN.parts, ("Request", "Why", "Steps", "Next"))

    def test_the_keys_in_the_order_a_new_plan_writes_them(self) -> None:
        self.assertEqual(
            [key.key for key in PLAN.keys],
            ["session", "title", "status", "opened", "project", "parent", "conversation", "priority", "topic", "kind", "depends_on"],
        )
        self.assertIs(PlanKey.STATUS, PLAN.keys[2])

    def test_every_key_says_what_it_holds(self) -> None:
        for key in PLAN.keys:
            with self.subTest(key=key.key):
                self.assertTrue(key.description)

    def test_the_statuses_are_those_of_a_session_plan(self) -> None:
        self.assertEqual(PLAN.kind, Kind.SESSION_PLAN)
        self.assertEqual(PLAN.statuses, (Status.QUEUED, Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))

    def test_a_key_is_written_in_pascal_case(self) -> None:
        self.assertEqual(PlanKey.PARENT.written, "Parent")


class ReportRecord(unittest.TestCase):
    def test_the_file_and_the_parts(self) -> None:
        self.assertEqual(REPORT.file_name, "report.md")
        self.assertEqual(REPORT.parts, ("What ran", "Check", "Result", "Left open"))

    def test_the_keys(self) -> None:
        self.assertEqual([key.key for key in REPORT.keys], ["session", "title", "status"])
        self.assertIs(ReportKey.STATUS, REPORT.keys[2])

    def test_the_hand_back_part_and_its_limit(self) -> None:
        self.assertEqual(REPORT.hand_back_part, "Decisions needed")
        self.assertEqual(REPORT.hand_back_max_lines, 10)

    def test_the_plan_has_no_hand_back_part(self) -> None:
        self.assertIsNone(PLAN.hand_back_part)

    def test_the_statuses_are_those_of_a_session_report(self) -> None:
        self.assertEqual(REPORT.kind, Kind.SESSION_REPORT)
        self.assertEqual(REPORT.statuses, (Status.ACTIVE, Status.BLOCKED, Status.COMPLETE))


class TheSessionId(unittest.TestCase):
    def test_both_records_open_with_the_session_they_belong_to(self) -> None:
        self.assertIs(PLAN.keys[0], PlanKey.SESSION)
        self.assertIs(REPORT.keys[0], ReportKey.SESSION)

    def test_the_field_is_declared_once_and_written_in_pascal_case(self) -> None:
        self.assertEqual(PlanKey.SESSION.value, SESSION_FIELD)
        self.assertEqual(ReportKey.SESSION.value, SESSION_FIELD)
        self.assertEqual(PlanKey.SESSION.written, "Session")
        self.assertEqual(ReportKey.SESSION.written, "Session")


class Outline(unittest.TestCase):
    def test_the_outline_names_every_key_and_part(self) -> None:
        for record in (PLAN, REPORT):
            text = record.outline()
            for key in record.keys:
                self.assertIn(f"{key.written}:", text)
            for part in record.parts:
                self.assertIn(f"## {part}", text)

    def test_the_outline_starts_and_ends_the_front_matter(self) -> None:
        lines = PLAN.outline().splitlines()
        self.assertEqual(lines[0], "---")
        self.assertIn("---", lines[1:])


if __name__ == "__main__":
    unittest.main(verbosity=2)
