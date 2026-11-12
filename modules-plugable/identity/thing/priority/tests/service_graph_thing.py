#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_services = import_module('modules.process.services.services')
_m_rank_ops = import_module('modules-plugable.identity.thing.priority.services.graph_priority_ops')
_m_label_ops = import_module('modules-plugable.knowledge.label.services.graph_label_ops')
GraphWiring = import_module('modules-plugable.management.task.services.graph_wiring').GraphWiring
_m_rank = import_module('modules-plugable.identity.thing.priority.primitive.rank')
_m_priority = import_module('modules-plugable.identity.thing.priority.labels.Priority')
_m_memory = import_module('modules.knowledge.label.tests.memory_labels')
_m_ranks = import_module('modules-plugable.identity.thing.priority.services.rank_store')
faces = import_module('modules-plugable.identity.thing.priority.services.register_services')
Volatile = _m_volatile.Volatile
Graph_Store = _m_graph.Graph_Store
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
priority_on_graph = _m_rank_ops.priority_on_graph
labels_on_graph = _m_label_ops.labels_on_graph
Priority_Rank = _m_rank.Priority_Rank
Label_Priority = _m_priority.Label_Priority
Process_Services = _m_services.Process_Services
Memory = _m_memory.Memory
MemoryRankStore = _m_ranks.MemoryRankStore
SET = faces.SET_UUID
READ = faces.READ_UUID
TITLES = {Label_Priority.as_label.id: Label_Priority.as_label.title}
THING_TEXT = '01900000-0000-7000-8000-0000000000e1'
THING = uuid.UUID(THING_TEXT).bytes
PROJECT = 'p'


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = Graph_Store(Volatile(), LAYOUT_COMPACT)
        self.opened = []

        def open_graph(project, needs):
            self.opened.append(project)
            return self.graph
        self.opener = GraphWiring(open_graph, TITLES.get)
        self.services = Process_Services()
        faces.register_services(self.services, opener=lambda: self.opener)

    def call(self, service_id, **arguments):
        return self.services.get_by_id(service_id).do(**arguments)


class GraphThing(Fixture):

    def test_set_then_read_through_the_registry_round_trips_in_the_graph(self) -> None:
        self.call(SET, thing=THING_TEXT, word='8', project=PROJECT)
        read = self.call(READ, thing=THING_TEXT, project=PROJECT)
        self.assertIn('priority 8', read)
        self.assertNotIn('default lowest', read)
        self.assertEqual(priority_on_graph(self.graph).get_rank(THING), Priority_Rank(8))
        titles = [item.title for item in labels_on_graph(self.graph, TITLES.get).get(THING)]
        self.assertEqual(titles, ['Priority'])

    def test_a_later_set_replaces_the_rank(self) -> None:
        self.call(SET, thing=THING_TEXT, word='8', project=PROJECT)
        self.call(SET, thing=THING_TEXT, word='3', project=PROJECT)
        self.assertEqual(priority_on_graph(self.graph).get_rank(THING), Priority_Rank(3))

    def test_a_thing_with_no_priority_reads_as_the_lowest_by_default(self) -> None:
        read = self.call(READ, thing=THING_TEXT, project=PROJECT)
        self.assertIn(f'priority {int(Priority_Rank.LOWEST)}', read)
        self.assertIn('(default lowest)', read)

    def test_a_value_outside_the_bounds_is_refused_and_nothing_is_written(self) -> None:
        with self.assertRaises(SystemExit):
            self.call(SET, thing=THING_TEXT, word='99', project=PROJECT)
        self.assertIsNone(priority_on_graph(self.graph).get_rank(THING))

    def test_a_uuid_thing_without_a_project_fails_naming_project_path(self) -> None:
        with self.assertRaises(SystemExit) as raised:
            self.call(READ, thing=THING_TEXT, project=None)
        self.assertIn('--project-path', str(raised.exception.code))
        self.assertEqual(self.opened, [])


class TaskThing(Fixture):

    def test_a_task_id_thing_still_goes_to_the_old_stores_and_never_opens_a_graph(self) -> None:
        labels = Memory()
        ranks = MemoryRankStore()
        asked = []
        saved = faces.stores_for
        faces.stores_for = lambda thing, project=None: (asked.append(thing), (labels, ranks))[1]
        self.addCleanup(setattr, faces, 'stores_for', saved)
        self.call(SET, thing='T', word='8', project=PROJECT)
        read = self.call(READ, thing='T', project=PROJECT)
        self.assertEqual(asked, ['T', 'T'])
        self.assertIn('priority 8', read)
        self.assertEqual(self.opened, [])


if __name__ == '__main__':
    unittest.main()
