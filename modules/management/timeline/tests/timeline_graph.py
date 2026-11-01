#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for Timeline_Placement_Store over Graph_Store (`services/timeline_graph.py`).

    python modules/management/timeline/tests/timeline_graph.py
"""
from __future__ import annotations
from importlib import import_module
import sys
import unittest
import uuid
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()) / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 30
Volatile = import_module('modules.computer.memory.volatile.volatile').Volatile
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
errors = import_module('modules.management.timeline.errors.placement')
timeline_graph = import_module('modules.management.timeline.services.timeline_graph')
Graph_Store = _m_graph.Graph_Store
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
Committed = import_module('modules.computer.memory.store.protocol.store').Committed


class Kinds:

    def __init__(self) -> None:
        self.by_id: dict[bytes, str] = {}

    def add_content(self, kind, text):
        at = uuid.uuid7().bytes
        self.by_id[at] = kind
        return at

    def read_content(self, content):
        kind = self.by_id.get(content)
        return (kind, '', True) if kind is not None else ('', '', False)


class Nodes:

    def __init__(self, memory) -> None:
        self.memory = memory
        self._absent = import_module('modules.computer.memory.store.protocol.store').ABSENT

    def ensure(self, at: bytes) -> None:
        key = _m_record.key(at, 'task')
        result = self.memory.batch([(key, self._absent)], [(key, b'{}')])
        if not isinstance(result, Committed):
            raise AssertionError(result)


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.memory = Volatile()
        self.graph = Graph_Store(self.memory, LAYOUT_COMPACT)
        self.kinds = Kinds()
        self.nodes = Nodes(self.memory)
        self.timeline = timeline_graph.GraphTimeline(self.graph, self.memory, self.kinds)
        self.task = uuid.uuid7().bytes
        self.nodes.ensure(self.task)

    def place(self, kind: str, after: int = 0, placer: str = 'u', at: int = 1000) -> tuple[int, bytes]:
        content = self.kinds.add_content(kind, 'body\n')
        number = self.timeline.add_placement(self.task, content, kind, placer, at, after)
        return (number, content)


class Place(Fixture):

    def test_the_first_placement_is_number_one(self) -> None:
        number, content = self.place('plan')
        self.assertEqual(number, 1)
        latest = self.timeline.read_latest_placement(self.task, 'plan')
        self.assertEqual(latest, (1, content, True))

    def test_numbers_run_across_kinds(self) -> None:
        self.assertEqual(self.place('plan')[0], 1)
        self.assertEqual(self.place('report')[0], 2)
        self.assertEqual(self.place('plan', after=1)[0], 3)

    def test_after_refuses_when_a_later_of_the_same_kind_exists(self) -> None:
        self.place('plan')
        content = self.kinds.add_content('plan', 'x\n')
        with self.assertRaises(errors.Timeline_Error_Changed):
            self.timeline.add_placement(self.task, content, 'plan', 'u', 1000, 0)

    def test_a_missing_timeline_node_is_not_found(self) -> None:
        missing = uuid.uuid7().bytes
        content = self.kinds.add_content('plan', 'x\n')
        with self.assertRaises(errors.Timeline_Error_NotFound):
            self.timeline.add_placement(missing, content, 'plan', 'u', 1000, 0)

    def test_edge_fields_hold_number_placer_and_instant_not_kind(self) -> None:
        number, content = self.place('plan', placer='memar', at=1761868800)
        sides = self.graph.list_sides(_m_graph.Graph_ListSidesQuery(self.task, timeline_graph.EVENT_IS))
        self.assertEqual(len(sides), 1)
        fields = timeline_graph.fields_of(sides[0].Fields)
        self.assertEqual(fields['number'], number)
        self.assertEqual(fields['placer'], 'memar')
        self.assertEqual(fields['placed_at'], 1761868800)
        self.assertNotIn('kind', fields)
        self.assertEqual(sides[0].To, content)

    def test_list_sides_of_one_timeline_does_not_see_another(self) -> None:
        self.place('plan')
        other = uuid.uuid7().bytes
        self.nodes.ensure(other)
        other_timeline = timeline_graph.GraphTimeline(self.graph, self.memory, self.kinds)
        content = self.kinds.add_content('plan', 'y\n')
        other_timeline.add_placement(other, content, 'plan', 'u', 1000, 0)
        mine = self.graph.count_sides(self.task, timeline_graph.EVENT_IS)
        theirs = self.graph.count_sides(other, timeline_graph.EVENT_IS)
        self.assertEqual(mine, 1)
        self.assertEqual(theirs, 1)


if __name__ == '__main__':
    unittest.main()
