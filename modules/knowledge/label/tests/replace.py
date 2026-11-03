#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True
from modules.identity.thing.labels.Complete import Label_Complete
from modules.identity.thing.labels.Queued import Label_Queued
from modules.knowledge.label.primitive.label import Label, Labels, new_id
replace = import_module('modules.knowledge.label.services.replace_label').replace
RED = Label('red', new_id())
GREEN = Label('green', new_id())
BLUE = Label('blue', new_id())
GOLD = Label('gold', new_id())

class Memory:

    def __init__(self, **held: Labels) -> None:
        self.held = dict(held)
        self.puts = 0

    def get(self, thing: str) -> Labels:
        return self.held.get(thing, Labels())

    def put(self, thing: str, labels: Labels) -> None:
        self.puts += 1
        self.held[thing] = labels

class Replace(unittest.TestCase):

    def test_the_new_label_stands_where_the_old_one_stood(self) -> None:
        store = Memory(a=Labels((RED, GREEN, BLUE)))
        replace(store, 'a', GREEN, GOLD)
        self.assertEqual(store.held['a'].items, (RED, GOLD, BLUE))

    def test_every_other_label_and_other_things_are_kept(self) -> None:
        store = Memory(a=Labels((RED, GREEN)), b=Labels((GREEN,)))
        replace(store, 'a', RED, BLUE)
        self.assertEqual(store.held['a'].items, (BLUE, GREEN))
        self.assertEqual(store.held['b'].items, (GREEN,))

    def test_a_thing_that_does_not_carry_the_old_label_is_refused(self) -> None:
        store = Memory(a=Labels((RED,)))
        with self.assertRaises(SystemExit) as refused:
            replace(store, 'a', GREEN, GOLD)
        self.assertIn('green', str(refused.exception))
        with self.assertRaises(SystemExit):
            replace(store, 'unknown', GREEN, GOLD)

    def test_a_refusal_leaves_the_store_untouched(self) -> None:
        store = Memory(a=Labels((RED, BLUE)))
        with self.assertRaises(SystemExit):
            replace(store, 'a', GREEN, GOLD)
        self.assertEqual(store.held, {'a': Labels((RED, BLUE))})
        self.assertEqual(store.puts, 0)

    def test_a_new_label_already_carried_is_not_carried_twice(self) -> None:
        store = Memory(a=Labels((RED, GREEN)))
        replace(store, 'a', RED, GREEN)
        self.assertEqual(store.held['a'].items, (GREEN,))

    def test_a_status_swap_works(self) -> None:
        store = Memory(task=Labels((RED, Label_Queued.as_label)))
        replace(store, 'task', Label_Queued.as_label, Label_Complete.as_label)
        self.assertEqual(store.held['task'].items, (RED, Label_Complete.as_label))

if __name__ == '__main__':
    unittest.main(verbosity=2)
