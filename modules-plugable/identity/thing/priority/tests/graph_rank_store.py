#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
import json
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP / 'bundles' / 'memar' / 'services'))
sys.path.insert(1, str(TOP / 'bundles' / 'memar'))
sys.path.insert(2, str(TOP))
sys.dont_write_bytecode = True
_m_label = import_module('modules.knowledge.label.primitive.label')
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_rank = import_module('modules-plugable.identity.thing.priority.primitive.rank')
_m_priority_label = import_module('modules-plugable.identity.thing.priority.labels.Priority')
_m_primitive = import_module('modules-plugable.identity.thing.priority.services.graph_priority_ops')
_m_errors = import_module('modules-plugable.identity.thing.priority.errors.errors')
_m_label_ops = import_module('modules-plugable.knowledge.label.services.graph_label_ops')
Label = _m_label.Label
Labels = _m_label.Labels
Conflict = _m_store.Conflict
Refused = _m_store.Refused
Unavailable = _m_store.Unavailable
Refusal = _m_store.Refusal
Unavailability = _m_store.Unavailability
Volatile = _m_volatile.Volatile
Graph_Store = _m_graph.Graph_Store
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
Priority_Rank = _m_rank.Priority_Rank
Label_Priority = _m_priority_label.Label_Priority
priority_on_graph = _m_primitive.priority_on_graph
PRIORITY = _m_primitive.PRIORITY
PRIORITY_OF = _m_primitive.PRIORITY_OF
VERTEX = _m_primitive.VERTEX
GraphRank_Error_Changed = _m_errors.GraphRank_Error_Changed
GraphRank_Error_Refused = _m_errors.GraphRank_Error_Refused
labels_on_graph = _m_label_ops.labels_on_graph
LABEL = _m_label_ops.LABEL
THING = uuid.UUID('01900000-0000-7000-8000-0000000000e1').bytes
OTHER = uuid.UUID('01900000-0000-7000-8000-0000000000e2').bytes
ID_A = '01900000-0000-7000-8000-0000000000a1'
A = Label('Alpha', ID_A)


def title_of(label_id: str) -> str | None:
    return {ID_A: 'Alpha'}.get(label_id)


class Counting(Volatile):

    def __init__(self) -> None:
        super().__init__()
        self.batches = 0

    def batch(self, expect, write):
        self.batches += 1
        return super().batch(expect, write)


class Interfering(Volatile):

    def __init__(self) -> None:
        super().__init__()
        self.competing = None

    def batch(self, expect, write):
        competing, self.competing = (self.competing, None)
        if competing is not None:
            competing()
        return super().batch(expect, write)


class Conflicting(Volatile):

    def __init__(self) -> None:
        super().__init__()
        self.conflicting = False

    def batch(self, expect, write):
        if self.conflicting:
            return Conflict(0)
        return super().batch(expect, write)


class Answering(Volatile):

    def __init__(self) -> None:
        super().__init__()
        self.answer = None

    def batch(self, expect, write):
        if self.answer is not None:
            return self.answer
        return super().batch(expect, write)


def ranked(volatile=None) -> tuple:
    volatile = volatile if volatile is not None else Volatile()
    graph = Graph_Store(volatile, LAYOUT_COMPACT)
    return (priority_on_graph(graph), graph, volatile)


def sides(graph, thing: bytes, relation: bytes) -> list:
    return list(graph.list_sides(Graph_ListSidesQuery(thing, relation)))


class GraphPriorityOpsTests(unittest.TestCase):

    def test_get_on_unknown_thing_is_none(self) -> None:
        store, _, _ = ranked()
        self.assertIsNone(store.get_rank(THING))

    def test_set_then_get_returns_the_rank(self) -> None:
        store, _, _ = ranked()
        store.put_rank(THING, Priority_Rank(7))
        found = store.get_rank(THING)
        self.assertEqual(int(found), 7)
        self.assertIsInstance(found, Priority_Rank)

    def test_replace_keeps_one_edge_and_returns_the_new_rank(self) -> None:
        store, graph, _ = ranked()
        store.put_rank(THING, Priority_Rank(7))
        store.put_rank(THING, Priority_Rank(2))
        self.assertEqual(int(store.get_rank(THING)), 2)
        self.assertEqual(len(sides(graph, THING, PRIORITY)), 1)

    def test_ranks_of_two_things_are_apart(self) -> None:
        store, _, _ = ranked()
        store.put_rank(THING, Priority_Rank(7))
        store.put_rank(OTHER, Priority_Rank(3))
        self.assertEqual(int(store.get_rank(THING)), 7)
        self.assertEqual(int(store.get_rank(OTHER)), 3)

    def test_the_edge_goes_to_the_priority_vertex_with_the_rank_in_its_field_and_a_reverse_edge(self) -> None:
        store, graph, _ = ranked()
        store.put_rank(THING, Priority_Rank(7))
        held = sides(graph, THING, PRIORITY)
        self.assertEqual([side.To for side in held], [VERTEX])
        self.assertEqual(VERTEX, uuid.UUID(Label_Priority.id).bytes)
        self.assertEqual(json.loads(held[0].Fields), {Priority_Rank.TYPE_UUID: 7})
        self.assertEqual([side.To for side in sides(graph, VERTEX, PRIORITY_OF)], [THING])

    def test_an_equal_rank_writes_nothing(self) -> None:
        counting = Counting()
        store, _, _ = ranked(counting)
        store.put_rank(THING, Priority_Rank(7))
        before = counting.batches
        store.put_rank(THING, Priority_Rank(7))
        self.assertEqual(counting.batches, before)

    def test_rank_is_independent_from_the_label_sides_of_the_same_thing(self) -> None:
        store, graph, _ = ranked()
        labels = labels_on_graph(graph, title_of)
        labels.put(THING, Labels((A,)))
        store.put_rank(THING, Priority_Rank(7))
        self.assertEqual(labels.get(THING), Labels((A,)))
        labels.put(THING, Labels())
        self.assertEqual(int(store.get_rank(THING)), 7)
        self.assertEqual(sides(graph, THING, LABEL), [])
        labels.put(THING, Labels((A,)))
        self.assertEqual(int(store.get_rank(THING)), 7)

    def test_a_rank_can_be_set_without_the_priority_label_attached(self) -> None:
        store, graph, _ = ranked()
        store.put_rank(THING, Priority_Rank(4))
        self.assertEqual(sides(graph, THING, LABEL), [])
        self.assertEqual(int(store.get_rank(THING)), 4)

    def test_competing_write_between_read_and_write_is_retried(self) -> None:
        interfering = Interfering()
        store, _, _ = ranked(interfering)
        store.put_rank(THING, Priority_Rank(3))
        rival = Graph_Store(interfering, LAYOUT_COMPACT)

        def compete() -> None:
            held = sides(rival, THING, PRIORITY)[0]
            rival.set_side_fields(held.Ref, json.dumps({Priority_Rank.TYPE_UUID: 9}).encode('utf-8'), held.Token)
        interfering.competing = compete
        store.put_rank(THING, Priority_Rank(5))
        self.assertEqual(int(store.get_rank(THING)), 5)
        self.assertIsNone(interfering.competing)

    def test_five_consecutive_conflicts_raise_changed_and_write_nothing(self) -> None:
        conflicting = Conflicting()
        store, _, _ = ranked(conflicting)
        store.put_rank(THING, Priority_Rank(3))
        conflicting.conflicting = True
        with self.assertRaises(GraphRank_Error_Changed):
            store.put_rank(THING, Priority_Rank(8))
        conflicting.conflicting = False
        self.assertEqual(int(store.get_rank(THING)), 3)

    def test_conflicts_on_the_first_write_raise_changed_and_leave_none(self) -> None:
        conflicting = Conflicting()
        store, _, _ = ranked(conflicting)
        conflicting.conflicting = True
        with self.assertRaises(GraphRank_Error_Changed):
            store.put_rank(THING, Priority_Rank(8))
        conflicting.conflicting = False
        self.assertIsNone(store.get_rank(THING))

    def test_refused_and_unavailable_raise_the_refusal_error(self) -> None:
        for answer in (Refused(Refusal.MALFORMED), Unavailable(Unavailability.FAILED)):
            with self.subTest(answer=answer):
                answering = Answering()
                store, _, _ = ranked(answering)
                answering.answer = answer
                with self.assertRaises(GraphRank_Error_Refused):
                    store.put_rank(THING, Priority_Rank(5))


if __name__ == '__main__':
    unittest.main()
