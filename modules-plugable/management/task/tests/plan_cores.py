#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the cores of the plan, priority, labels, depends-on and queue services of `modules-plugable/management/task/services/`.

    python modules-plugable/management/task/tests/plan_cores.py

Each core takes a store (`modules-plugable/management/task/protocol/task-*-store.kh`) and opens no file; the
stores here are in memory, so a core that touched a file would be seen.
"""
from __future__ import annotations
from importlib import import_module
import builtins
import sys
import unittest
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 20
errors = import_module('modules-plugable.management.task.errors.errors')
priority_core = import_module('modules-plugable.management.task.services.plan_priority')
labels_core = import_module('modules-plugable.management.task.services.plan_labels')
depends_core = import_module('modules-plugable.management.task.services.plan_depends')
status_core = import_module('modules-plugable.management.task.services.plan_status')
write_core = import_module('modules-plugable.management.task.services.plan_write')
_m_dependency = import_module('modules-plugable.management.task.services.dependency')
DependsOn = _m_dependency.DependsOn
from modules.knowledge.label.primitive.label import Label, Labels

LABEL = Labels.read('implement(01a14a04-6533-7efe-98ac-0e9e47dc1376)')

class Memory:

    def __init__(self, **facts) -> None:
        self.facts = {'priority': 5, 'status': 'active', 'labels': Labels(), 'depends_on': DependsOn.normalized([])}
        self.facts.update(facts)
        self.versions = {key: 0 for key in self.facts}
        self.interfere = {}
        self.writes = []
        self.problem = None

    def read(self, key):
        return (self.facts[key], str(self.versions[key]))

    def replace(self, key, value, expected):
        if key in self.interfere:
            self.versions[key] += 1
            self.interfere.pop(key)
        if str(self.versions[key]) != expected:
            raise errors.Task_Error_Changed()
        self.facts[key] = value
        self.versions[key] += 1
        self.writes.append(key)
        return str(self.versions[key])

    def shape_problem(self, project, task): return self.problem
    def read_priority(self, project, task): return self.read('priority')
    def replace_priority(self, project, task, value, expected): return self.replace('priority', value, expected)
    def read_status(self, project, task): return self.read('status')
    def replace_status(self, project, task, value, expected): return self.replace('status', value, expected)
    def read_labels(self, project, task): return self.read('labels')
    def replace_labels(self, project, task, value, expected): return self.replace('labels', value, expected)
    def read_depends_on(self, project, task): return self.read('depends_on')
    def replace_depends_on(self, project, task, value, expected): return self.replace('depends_on', value, expected)

class Priority(unittest.TestCase):

    def test_the_priority_is_replaced_through_the_store(self) -> None:
        store = Memory()
        priority_core.set_priority(store, None, 'T', 8)
        self.assertEqual(store.facts['priority'], 8)

    def test_a_value_outside_the_bounds_is_refused_and_nothing_is_written(self) -> None:
        store = Memory()
        with self.assertRaises(SystemExit):
            priority_core.set_priority(store, None, 'T', 99)
        self.assertEqual(store.writes, [])

    def test_a_change_between_read_and_replace_is_read_again_not_lost(self) -> None:
        store = Memory()
        store.interfere['priority'] = True
        priority_core.set_priority(store, None, 'T', 3)
        self.assertEqual(store.facts['priority'], 3)

class Status(unittest.TestCase):

    def test_a_status_is_set(self) -> None:
        store = Memory(status='active')
        status_core.set_status(store, None, 'T', 'queued')
        self.assertEqual(store.facts['status'], 'queued')

    def test_only_from_refuses_a_status_that_is_no_longer_expected_and_writes_nothing(self) -> None:
        store = Memory(status='complete')
        with self.assertRaises(SystemExit):
            status_core.set_status(store, None, 'T', 'active', only_from=('queued',))
        self.assertEqual(store.writes, [])

    def test_only_from_holds_against_a_change_that_lands_meanwhile(self) -> None:
        store = Memory(status='queued')
        store.interfere['status'] = True
        status_core.set_status(store, None, 'T', 'active', only_from=('queued', 'active'))
        self.assertEqual(store.facts['status'], 'active')

    def test_a_word_that_is_no_status_is_refused(self) -> None:
        with self.assertRaises(SystemExit):
            status_core.set_status(Memory(), None, 'T', 'open')

class Queue(unittest.TestCase):

    def test_an_active_unclaimed_task_is_queued(self) -> None:
        store = Memory(status='active')
        write_core.queue_plan(store, None, 'T', claimed=False)
        self.assertEqual(store.facts['status'], 'queued')

    def test_a_queued_task_stays_queued_and_nothing_is_written(self) -> None:
        store = Memory(status='queued')
        write_core.queue_plan(store, None, 'T', claimed=True)
        self.assertEqual(store.writes, [])

    def test_a_claimed_task_is_refused(self) -> None:
        store = Memory(status='active')
        with self.assertRaises(SystemExit):
            write_core.queue_plan(store, None, 'T', claimed=True)
        self.assertEqual(store.facts['status'], 'active')

    def test_a_task_that_is_not_active_is_refused(self) -> None:
        store = Memory(status='complete')
        with self.assertRaises(SystemExit):
            write_core.queue_plan(store, None, 'T', claimed=False)

class Labels_(unittest.TestCase):

    def test_a_label_is_added_once_and_removed(self) -> None:
        store = Memory()
        label = next(iter(LABEL))
        labels_core.add_label(store, None, 'T', label)
        labels_core.add_label(store, None, 'T', label)
        self.assertEqual(list(store.facts['labels']), [label])
        labels_core.remove_label(store, None, 'T', label)
        self.assertFalse(store.facts['labels'])

    def test_an_add_that_changes_nothing_writes_nothing(self) -> None:
        label = next(iter(LABEL))
        store = Memory(labels=LABEL)
        labels_core.add_label(store, None, 'T', label)
        self.assertEqual(store.writes, [])

class Depends(unittest.TestCase):

    def test_depends_on_is_replaced_through_the_store(self) -> None:
        store = Memory()
        now = DependsOn.normalized([])
        depends_core.set_depends_on(store, None, 'T', now)
        self.assertEqual(store.writes, ['depends_on'])

class NoFile(unittest.TestCase):

    def test_a_core_opens_no_file(self) -> None:
        real = builtins.open
        seen = []

        def spy(*args, **kwargs):
            seen.append(args[0])
            return real(*args, **kwargs)
        builtins.open = spy
        try:
            store = Memory(status='active')
            priority_core.set_priority(store, None, 'T', 2)
            status_core.set_status(store, None, 'T', 'queued')
            labels_core.add_label(store, None, 'T', next(iter(LABEL)))
            depends_core.set_depends_on(store, None, 'T', DependsOn.normalized([]))
            write_core.queue_plan(Memory(status='active'), None, 'T', claimed=False)
        finally:
            builtins.open = real
        self.assertEqual(seen, [])

if __name__ == '__main__':
    unittest.main()
