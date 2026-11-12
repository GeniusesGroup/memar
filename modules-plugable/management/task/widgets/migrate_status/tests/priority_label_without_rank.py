#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
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
base = import_module('modules-plugable.management.task.widgets.migrate_status.tests.migrate_status')
Labels = base.Labels
Memory = base.Memory
ManyFacts = base.ManyFacts
Label_Priority = base.Label_Priority
PROJECT = base.PROJECT
T1 = base.T1
T2 = base.T2
MigrateStatus_Error_Differs = base.MigrateStatus_Error_Differs


def labelled() -> ManyFacts:
    return ManyFacts(**{T1: Memory(status='active', labels=Labels((Label_Priority.as_label,)), priority_rank='')})


def plain() -> ManyFacts:
    return ManyFacts(**{T2: Memory(status='active', priority_rank='')})


class PriorityLabelWithoutRank(unittest.TestCase):

    def test_the_priority_label_without_a_rank_lands_on_the_thing(self) -> None:
        opener, _, _, _ = base.opened()
        base.run(labelled(), opener, ids=base.tasks_of(T1))
        self.assertEqual(base.status_of(opener, PROJECT, T1), ['Active', 'Priority'])
        self.assertIsNone(base.rank_of(opener, PROJECT, T1))

    def test_verify_passes_after_migrate_for_a_priority_label_without_a_rank(self) -> None:
        opener, _, _, _ = base.opened()
        base.run(labelled(), opener, ids=base.tasks_of(T1))
        plan, _ = base.run(labelled(), opener, ids=base.tasks_of(T1), verify=True)
        self.assertEqual(list(plan.differences), [])

    def test_the_second_run_writes_nothing_for_a_priority_label_without_a_rank(self) -> None:
        opener, _, volatile, _ = base.opened()
        base.run(labelled(), opener, ids=base.tasks_of(T1))
        batches = volatile.batches
        plan, _ = base.run(labelled(), opener, ids=base.tasks_of(T1))
        self.assertEqual(plan.written, 0)
        self.assertEqual(volatile.batches, batches)

    def test_a_thing_without_the_label_and_without_a_rank_gets_no_priority_label(self) -> None:
        opener, _, _, _ = base.opened()
        base.run(plain(), opener, ids=base.tasks_of(T2))
        self.assertEqual(base.status_of(opener, PROJECT, T2), ['Active'])
        plan, _ = base.run(plain(), opener, ids=base.tasks_of(T2), verify=True)
        self.assertEqual(list(plan.differences), [])

    def test_verify_reports_a_priority_label_the_graph_holds_and_the_facts_lack(self) -> None:
        opener, _, _, _ = base.opened()
        base.run(labelled(), opener, ids=base.tasks_of(T1))
        with self.assertRaises(MigrateStatus_Error_Differs):
            base.run(ManyFacts(**{T1: Memory(status='active', priority_rank='')}), opener, ids=base.tasks_of(T1), verify=True)


if __name__ == '__main__':
    unittest.main()
