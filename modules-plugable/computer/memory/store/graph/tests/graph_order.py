# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
COST = {'subprocesses': 0, 'writes_files': False, 'clock_waits': False}
SUBJECT = 'Graph field-order query'
CONTRACT = 'modules-plugable/computer/memory/store/graph/protocol'
import json
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_types = import_module('modules.computer.types.types')
Refused = _m_store.Refused
Volatile = _m_volatile.Volatile
Types = _m_types.Types
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUTS = (_m_graph.LAYOUT_COMPACT, _m_graph.LAYOUT_PER_EDGE)
REL = uuid.UUID('01900000-0000-7000-8000-000000000001').bytes
REV = uuid.UUID('01900000-0000-7000-8000-000000000002').bytes
NUMBER = uuid.UUID('01900000-0000-7000-8000-0000000000f1').bytes
UNORDERED = uuid.UUID('01900000-0000-7000-8000-0000000000f2').bytes
UNREGISTERED = uuid.UUID('01900000-0000-7000-8000-0000000000f3').bytes

class Number:
    type_id = NUMBER

    def values_equal(self, a: bytes, b: bytes) -> bool:
        return self._number(a) == self._number(b)

    def compare_values(self, a: bytes, b: bytes) -> int:
        x, y = (self._number(a), self._number(b))
        return (x > y) - (x < y)

    def _number(self, value: bytes) -> int:
        return int(value.decode('ascii'))

class Unordered:
    type_id = UNORDERED

    def values_equal(self, a: bytes, b: bytes) -> bool:
        return a == b

def fields_of(field: bytes, value) -> bytes:
    return json.dumps({str(uuid.UUID(bytes=field)): value}, separators=(',', ':')).encode('utf-8')

def bound(layout: int) -> Graph_Store:
    types = Types()
    types.register(Number())
    types.register(Unordered())
    g = Graph_Store(Volatile(), layout).bind_types(types)
    for to, value in ((b'c', 10), (b'a', 2), (b'b', 33)):
        assert isinstance(g.put_edge(Graph_PutEdge(layout, b'v', REL, to, REV, fields_of(NUMBER, value))), bytes)
    assert isinstance(g.put_edge(Graph_PutEdge(layout, b'v', REL, b'd', REV, fields_of(UNORDERED, 'x'))), bytes)
    return g

def tos(sides) -> list[bytes]:
    return [each.To for each in sides]

class OrderByField(unittest.TestCase):

    def test_malformed_order_identity_is_refused_through_owner_boundary(self) -> None:
        for layout in LAYOUTS:
            for identity in (bytes(8), bytes(17), bytearray(16), NUMBER.hex(), 7):
                with self.subTest(layout=layout, identity=identity):
                    answer = bound(layout).list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=identity))
                    self.assertIsInstance(answer, Refused)

    def test_sides_are_ordered_by_the_order_the_type_declares_and_not_by_the_bytes(self) -> None:
        for layout in LAYOUTS:
            with self.subTest(layout=layout):
                sides = bound(layout).list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=NUMBER))
                self.assertEqual(tos(sides)[:3], [b'a', b'c', b'b'])

    def test_descending_reverses_the_typed_order(self) -> None:
        for layout in LAYOUTS:
            with self.subTest(layout=layout):
                sides = bound(layout).list_sides(Graph_ListSidesQuery(b'v', REL, Descending=True, OrderField=NUMBER))
                self.assertEqual(tos(sides)[:3], [b'b', b'c', b'a'])

    def test_a_side_without_the_field_comes_last_in_both_directions(self) -> None:
        for layout in LAYOUTS:
            with self.subTest(layout=layout):
                g = bound(layout)
                self.assertEqual(tos(g.list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=NUMBER)))[-1], b'd')
                self.assertEqual(tos(g.list_sides(Graph_ListSidesQuery(b'v', REL, Descending=True, OrderField=NUMBER)))[-1], b'd')

    def test_the_limit_applies_after_the_order(self) -> None:
        sides = bound(_m_graph.LAYOUT_COMPACT).list_sides(Graph_ListSidesQuery(b'v', REL, Limit=2, OrderField=NUMBER))
        self.assertEqual(tos(sides), [b'a', b'c'])

    def test_a_field_whose_type_is_not_registered_is_refused(self) -> None:
        answer = bound(_m_graph.LAYOUT_COMPACT).list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=UNREGISTERED))
        self.assertIsInstance(answer, Refused)

    def test_a_field_whose_type_declares_no_order_is_refused(self) -> None:
        answer = bound(_m_graph.LAYOUT_COMPACT).list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=UNORDERED))
        self.assertIsInstance(answer, Refused)

    def test_an_order_without_a_bound_registry_is_refused(self) -> None:
        g = Graph_Store(Volatile(), _m_graph.LAYOUT_COMPACT)
        g.put_edge(Graph_PutEdge(_m_graph.LAYOUT_COMPACT, b'v', REL, b'a', REV, fields_of(NUMBER, 1)))
        self.assertIsInstance(g.list_sides(Graph_ListSidesQuery(b'v', REL, OrderField=NUMBER)), Refused)

    def test_a_cursor_with_an_order_field_is_refused(self) -> None:
        answer = bound(_m_graph.LAYOUT_COMPACT).list_sides(Graph_ListSidesQuery(b'v', REL, After=b'x', OrderField=NUMBER))
        self.assertIsInstance(answer, Refused)

    def test_no_order_field_keeps_the_order_by_side_ref(self) -> None:
        g = bound(_m_graph.LAYOUT_COMPACT)
        refs = [each.Ref for each in g.list_sides(Graph_ListSidesQuery(b'v', REL))]
        self.assertEqual(refs, sorted(refs))

if __name__ == '__main__':
    unittest.main()
