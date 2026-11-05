#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
BUDGET_SECONDS = 60
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
for _folder in (TOP, TOP / 'bundles' / 'memar', TOP / 'bundles' / 'memar' / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
rule_module = import_module('modules.knowledge.text.services.text_line_ending_rule')


class LineEnding:

    def __init__(self, sequence: str) -> None:
        self.sequence = sequence

    def get_sequence(self) -> str:
        return self.sequence


class Choice:

    def __init__(self, line_ending=None) -> None:
        self.line_ending = line_ending

    def is_given(self) -> bool:
        return self.line_ending is not None

    def get_line_ending(self):
        return self.line_ending


LF = LineEnding('\n')
CRLF = LineEnding('\r\n')


class Detect(unittest.TestCase):

    def setUp(self) -> None:
        self.rule = rule_module.Text_LineEnding_Rule()

    def sequence(self, held: str) -> str:
        return self.rule.detect(held).get_sequence()

    def test_a_text_with_only_crlf_is_crlf(self) -> None:
        self.assertEqual(self.sequence('a\r\nb\r\n'), '\r\n')

    def test_a_text_with_only_lf_is_lf(self) -> None:
        self.assertEqual(self.sequence('a\nb\n'), '\n')

    def test_a_text_mixing_crlf_and_a_bare_lf_is_lf(self) -> None:
        self.assertEqual(self.sequence('a\r\nb\nc\r\n'), '\n')

    def test_an_empty_text_and_a_text_with_no_line_ending_are_lf(self) -> None:
        self.assertEqual(self.sequence(''), '\n')
        self.assertEqual(self.sequence('abc'), '\n')

    def test_a_lone_carriage_return_is_ignored(self) -> None:
        self.assertEqual(self.sequence('a\rb'), '\n')
        self.assertEqual(self.sequence('a\r\nb\rc'), '\r\n')


class Choose(unittest.TestCase):

    def setUp(self) -> None:
        self.rule = rule_module.Text_LineEnding_Rule()

    def test_a_given_choice_wins_over_the_held_text(self) -> None:
        self.assertEqual(self.rule.choose(Choice(CRLF), 'a\nb\n').get_sequence(), '\r\n')
        self.assertEqual(self.rule.choose(Choice(LF), 'a\r\nb\r\n').get_sequence(), '\n')

    def test_without_a_choice_the_held_text_decides(self) -> None:
        self.assertEqual(self.rule.choose(Choice(), 'a\r\nb\r\n').get_sequence(), '\r\n')
        self.assertEqual(self.rule.choose(Choice(), 'a\nb\n').get_sequence(), '\n')
        self.assertEqual(self.rule.choose(Choice(), '').get_sequence(), '\n')


class Normalize(unittest.TestCase):

    def setUp(self) -> None:
        self.rule = rule_module.Text_LineEnding_Rule()

    def test_every_kind_of_line_ending_becomes_the_given_one(self) -> None:
        self.assertEqual(self.rule.normalize('a\nb\r\nc\rd', CRLF), 'a\r\nb\r\nc\r\nd\r\n')
        self.assertEqual(self.rule.normalize('a\nb\r\nc\rd', LF), 'a\nb\nc\nd\n')

    def test_a_non_empty_text_ends_with_the_line_ending_once(self) -> None:
        self.assertEqual(self.rule.normalize('a', LF), 'a\n')
        self.assertEqual(self.rule.normalize('a\n', LF), 'a\n')
        self.assertEqual(self.rule.normalize('a\r\n', CRLF), 'a\r\n')
        self.assertEqual(self.rule.normalize('a\n\n', LF), 'a\n\n')

    def test_an_empty_text_stays_empty(self) -> None:
        self.assertEqual(self.rule.normalize('', CRLF), '')

    def test_other_characters_are_kept(self) -> None:
        self.assertEqual(self.rule.normalize('# Ünï\tx\n', CRLF), '# Ünï\tx\r\n')


if __name__ == '__main__':
    unittest.main(verbosity=2)
