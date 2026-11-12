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

BUDGET_SECONDS = 30

Memory = import_module('modules.knowledge.label.tests.memory_labels').Memory
MemoryRankStore = import_module('modules-plugable.identity.thing.priority.services.rank_store').MemoryRankStore
Label_Priority = import_module('modules-plugable.identity.thing.priority.labels.Priority').Label_Priority
Priority_Rank = import_module('modules-plugable.identity.thing.priority.primitive.rank').Priority_Rank
set_priority = import_module('modules-plugable.identity.thing.priority.services.set_priority').set_priority
read_priority = import_module('modules-plugable.identity.thing.priority.services.read_priority').read_priority
rank = import_module('modules-plugable.identity.thing.priority.services.read_priority').rank
set_mod = import_module('modules-plugable.identity.thing.priority.services.set_priority')
read_mod = import_module('modules-plugable.identity.thing.priority.services.read_priority')


class SetPriority(unittest.TestCase):

    def test_set_writes_rank_and_attaches_priority_label(self) -> None:
        labels = Memory()
        ranks = MemoryRankStore()
        set_priority(labels, ranks, 'T', 8)
        set_priority(labels, ranks, 'T', 3)
        value, found = read_priority(labels, ranks, 'T')
        self.assertTrue(found)
        self.assertEqual(int(value), 3)
        self.assertTrue(any(item.id == Label_Priority.as_label.id for item in labels.get('T')))

    def test_missing_priority_ranks_as_lowest(self) -> None:
        labels = Memory()
        ranks = MemoryRankStore()
        self.assertEqual(rank(labels, ranks, 'T'), int(Priority_Rank.LOWEST))
        value, found = read_priority(labels, ranks, 'T')
        self.assertFalse(found)
        self.assertEqual(int(value), int(Priority_Rank.LOWEST))

    def test_higher_rank_is_greater(self) -> None:
        labels = Memory()
        ranks = MemoryRankStore()
        set_priority(labels, ranks, 'A', 2)
        set_priority(labels, ranks, 'B', 9)
        self.assertGreater(rank(labels, ranks, 'B'), rank(labels, ranks, 'A'))

    def test_service_uuid_is_on_the_services_not_the_label(self) -> None:
        self.assertEqual(set_mod.SERVICE_UUID, 'f28f2eba-6923-5e6c-814d-92ca70b4d97e')
        self.assertEqual(read_mod.SERVICE_UUID, '70cd58f2-61bc-5813-8ec3-4cde61e0a53b')
        self.assertFalse(hasattr(Label_Priority, 'SERVICE_SET'))
        self.assertFalse(hasattr(Label_Priority, 'members'))

    def test_a_value_outside_the_bounds_is_refused_and_nothing_is_written(self) -> None:
        labels = Memory()
        ranks = MemoryRankStore()
        with self.assertRaises(SystemExit):
            set_priority(labels, ranks, 'T', 99)
        self.assertEqual(list(labels.get('T')), [])
        self.assertIsNone(ranks.get_rank('T'))


if __name__ == '__main__':
    unittest.main()
