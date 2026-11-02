#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if p.name == 'modules').parent
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 10
Word = import_module('modules.knowledge.content.primitive.word').Word

class WordPins(unittest.TestCase):

    def test_a_word_type_says_everything_about_itself_by_class_attributes(self) -> None:
        class Pending(Word):
            word = 'Pending'
            meaning = 'the open state'
            order = 1
            labels = ('propagation-state',)
        self.assertEqual((Pending.word, Pending.meaning, Pending.order, Pending.labels), ('Pending', 'the open state', 1, ('propagation-state',)))

    def test_it_is_a_plain_class_with_no_members(self) -> None:
        self.assertFalse(hasattr(Word, '__members__'))
        self.assertEqual(Word.__mro__, (Word, object))
if __name__ == '__main__':
    unittest.main(verbosity=2)
