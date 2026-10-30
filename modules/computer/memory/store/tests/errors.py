#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import ast
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
TIER = 'unit'
BUDGET_SECONDS = 60

def errors():
    return import_module('modules.computer.memory.store.errors.errors')

def store():
    return import_module('modules.computer.memory.store.protocol.store')

def volatile():
    return import_module('modules.computer.memory.volatile.volatile')

def declared_classes(module):
    tree = ast.parse(Path(module.__file__).read_text(encoding='utf-8'))
    return {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}

class ErrorsFolder(unittest.TestCase):

    def test_unavailability_kinds_are_the_declared_ones(self) -> None:
        self.assertEqual({each.value for each in errors().Unavailability}, {'NotHeld', 'Unreachable', 'Failed'})

    def test_refusal_kinds_are_the_declared_ones(self) -> None:
        self.assertEqual({each.value for each in errors().Refusal}, {'Malformed', 'TooLarge', 'NotAtomic'})

    def test_each_kind_says_what_it_is(self) -> None:
        for each in list(errors().Unavailability) + list(errors().Refusal):
            self.assertTrue(each.summary(), each)

    def test_the_store_uses_the_declarations_of_the_folder(self) -> None:
        self.assertIs(store().Refusal, errors().Refusal)
        self.assertIs(store().Unavailability, errors().Unavailability)

    def test_the_store_file_declares_no_error_of_its_own(self) -> None:
        self.assertEqual(declared_classes(store()) & {'Refusal', 'Unavailability'}, set())

    def test_the_volatile_file_declares_no_error_of_its_own(self) -> None:
        self.assertEqual(declared_classes(volatile()) & {'Refusal', 'Unavailability', 'Raised'}, set())

    def test_volatile_refuses_with_the_errors_of_the_folder(self) -> None:
        s, v, e = store(), volatile(), errors()
        self.assertEqual(v.Volatile().get([1]), s.Refused(e.Refusal.MALFORMED))
        limited = v.Volatile(limits=s.Limits(writes_per_batch=1))
        self.assertEqual(limited.batch([], [(b'a', b'1'), (b'b', b'2')]), s.Refused(e.Refusal.TOO_LARGE))
        single = v.Volatile(atomic_batch=False)
        self.assertEqual(single.batch([], [(b'a', b'1'), (b'b', b'2')]), s.Refused(e.Refusal.NOT_ATOMIC))

    def test_volatile_answers_unavailable_with_the_errors_of_the_folder(self) -> None:
        s, v, e = store(), volatile(), errors()
        held = v.Volatile()
        held.at_commit_point(lambda: 1 / 0)
        self.assertEqual(held.batch([], [(b'a', b'1')]), s.Unavailable(e.Unavailability.FAILED))
if __name__ == '__main__':
    unittest.main()
