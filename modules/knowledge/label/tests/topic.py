#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the topic type in `modules/knowledge/label/primitive/topic.py`.

    python modules/knowledge/label/tests/topic.py

The subject is a plan's topic, declared once: the one subject `claims` batches
by, free text normalized to lower case with runs of white space as one hyphen,
one line. Named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).
The fact is written once ([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).

Nothing here writes.

What is pinned, and what each pin is for:

  Normalizing  Text becomes a topic by one rule, whoever asks.
  Checking     A topic holding a line break is refused; an empty one is a
               topic that removes the key.
  Reading      A plan's labels read as its topics, normalized, in the order written, or none;
               the kind `Topic` declares the rule that makes a word of it.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
from modules.knowledge.label.primitive.label import LabelProblem
from modules.knowledge.label.primitive.topic import LABEL_KIND, TOPIC_LABEL, Topic

class Normalizing(unittest.TestCase):

    def test_lower_case_and_each_run_of_white_space_one_hyphen(self) -> None:
        for text, expected in (('Khayyam LSP', 'khayyam-lsp'), ('  docs   cleanup ', 'docs-cleanup'), ('docs', 'docs'), ('', ''), ('   ', '')):
            with self.subTest(text=text):
                self.assertEqual(Topic.normalized(text), expected)
                self.assertIsInstance(Topic.normalized(text), Topic)

class Checking(unittest.TestCase):

    def test_a_topic_is_returned_normalized(self) -> None:
        self.assertEqual(Topic.checked('Docs Cleanup'), 'docs-cleanup')

    def test_an_empty_topic_is_allowed_since_it_removes_the_key(self) -> None:
        self.assertEqual(Topic.checked(''), '')

    def test_a_line_break_is_refused(self) -> None:
        for text in ('a\nb', 'a\rb'):
            with self.subTest(text=text):
                with self.assertRaises(SystemExit):
                    Topic.checked(text)

class Reading(unittest.TestCase):

    def test_a_topic_is_a_free_label_kind_whose_rule_is_the_types(self) -> None:
        self.assertEqual(LABEL_KIND.name, 'Topic')
        self.assertEqual(LABEL_KIND.define(' Docs  Cleanup ').label.word, 'docs-cleanup')
        self.assertTrue(LABEL_KIND.define('docs').is_a(TOPIC_LABEL))
        self.assertEqual(LABEL_KIND.closed, ())
        with self.assertRaises(LabelProblem):
            LABEL_KIND.define('   ')
        with self.assertRaises(LabelProblem):
            LABEL_KIND.define('a\nb')
if __name__ == '__main__':
    unittest.main(verbosity=2)
