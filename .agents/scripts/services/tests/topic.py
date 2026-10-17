#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the topic type in `services/topic.py`.

    python .agents/scripts/services/tests/topic.py

The subject is a plan's topic, declared once: the one subject `claims` batches
by, free text normalized to lower case with runs of white space as one hyphen,
one line. Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)).

Nothing here writes.

What is pinned, and what each pin is for:

  Normalizing  Text becomes a topic by one rule, whoever asks.
  Checking     A topic holding a line break is refused; an empty one is a
               topic that removes the key.
  Reading      A plan's front matter reads as its topic, normalized, or empty.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent.parent
sys.path.insert(0, str(SCRIPTS))
sys.dont_write_bytecode = True

from services.session_record import PlanKey
from services.topic import Topic


class Normalizing(unittest.TestCase):
    def test_lower_case_and_each_run_of_white_space_one_hyphen(self) -> None:
        for text, expected in (
            ("Khayyam LSP", "khayyam-lsp"),
            ("  docs   cleanup ", "docs-cleanup"),
            ("docs", "docs"),
            ("", ""),
            ("   ", ""),
        ):
            with self.subTest(text=text):
                self.assertEqual(Topic.normalized(text), expected)
                self.assertIsInstance(Topic.normalized(text), Topic)


class Checking(unittest.TestCase):
    def test_a_topic_is_returned_normalized(self) -> None:
        self.assertEqual(Topic.checked("Docs Cleanup"), "docs-cleanup")

    def test_an_empty_topic_is_allowed_since_it_removes_the_key(self) -> None:
        self.assertEqual(Topic.checked(""), "")

    def test_a_line_break_is_refused(self) -> None:
        for text in ("a\nb", "a\rb"):
            with self.subTest(text=text):
                with self.assertRaises(SystemExit):
                    Topic.checked(text)


class Reading(unittest.TestCase):
    def test_a_plans_front_matter_reads_as_its_topic_normalized(self) -> None:
        self.assertEqual(Topic.of({PlanKey.TOPIC.key: "Docs  Cleanup"}), "docs-cleanup")

    def test_a_plan_without_one_has_none(self) -> None:
        self.assertEqual(Topic.of({}), "")
        self.assertEqual(Topic.of(None), "")


if __name__ == "__main__":
    unittest.main(verbosity=2)
