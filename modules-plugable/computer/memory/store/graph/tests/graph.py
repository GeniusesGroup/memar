#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
import ast
import enum
import io
import sys
import tokenize
import unittest
from importlib import import_module
from pathlib import Path
from typing import Any
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_errors = import_module('modules-plugable.computer.memory.store.graph.errors.errors')
ABSENT = _m_store.ABSENT
Committed = _m_store.Committed
Conflict = _m_store.Conflict
Found = _m_store.Found
Parameters = _m_store.Parameters
Refusal = _m_store.Refusal
Refused = _m_store.Refused
token = _m_store.token
Volatile = _m_volatile.Volatile
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
Graph_GetSideQuery = _m_graph.Graph_GetSideQuery
Graph_Pattern = _m_graph.Graph_Pattern
Graph_Pattern_Step = _m_graph.Graph_Pattern_Step
Graph_Path_Query = _m_graph.Graph_Path_Query
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
LAYOUT_PER_EDGE = _m_graph.LAYOUT_PER_EDGE
DIRECTION_OUT = _m_graph.DIRECTION_OUT
DIRECTION_IN = _m_graph.DIRECTION_IN
DIRECTION_EITHER = _m_graph.DIRECTION_EITHER
PATH_TRAIL = _m_graph.PATH_TRAIL
PATH_ACYCLIC = _m_graph.PATH_ACYCLIC

def opened(layout: int=LAYOUT_COMPACT) -> Any:
    return Graph_Store(Volatile(), layout)

def edge(layout: int, frm: bytes, relation: bytes, to: bytes, reverse: bytes=b'', fields: bytes=b'', expect_from: bytes=b'', expect_to: bytes=b'') -> Any:
    return Graph_PutEdge(layout, frm, relation, to, reverse, fields, expect_from, expect_to)

class Adjacency(unittest.TestCase):

    def test_put_edge_writes_reverse_in_one_batch(self) -> None:
        for layout in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            with self.subTest(layout=layout):
                g = opened(layout)
                ref = g.put_edge(edge(layout, b'a', b'knows', b'b', b'known-by', b'f1'))
                self.assertIsInstance(ref, bytes)
                self.assertTrue(ref)
                forward = g.get_side(Graph_GetSideQuery(b'a', b'knows', b'b'))
                reverse = g.get_side(Graph_GetSideQuery(b'b', b'known-by', b'a'))
                self.assertTrue(forward.Found)
                self.assertTrue(reverse.Found)
                self.assertEqual(forward.Fields, b'f1')
                self.assertEqual(reverse.Fields, b'f1')
                self.assertEqual(forward.Ref, ref)

    def test_put_edges_commits_n_in_one_batch(self) -> None:
        for layout in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            with self.subTest(layout=layout):
                g = opened(layout)
                edges = [edge(layout, b'a', b'r', bytes([i]), b'rr', bytes([i])) for i in range(5)]
                refs = g.put_edges(edges)
                self.assertEqual(len(refs), 5)
                self.assertTrue(all((isinstance(each, bytes) and each for each in refs)))
                self.assertEqual(g.count_sides(b'a', b'r'), 5)
                self.assertEqual(g.count_sides(b'\x00', b'rr'), 1)
                self.assertEqual(g.count_sides(b'\x04', b'rr'), 1)

    def test_compact_cas_conflict_when_expect_stale(self) -> None:
        g = opened(LAYOUT_COMPACT)
        ref = g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr', b'one'))
        got = g.get_side(Graph_GetSideQuery(b'a', b'r', b'b'))
        self.assertTrue(got.Found)
        stale = token(b'stale-not-held')
        answer = g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'c', b'rr', b'two', expect_from=stale))
        self.assertIsInstance(answer, Conflict)
        self.assertEqual(g.count_sides(b'a', b'r'), 1)
        self.assertEqual(g.get_side(Graph_GetSideQuery(b'a', b'r', b'b')).Ref, ref)

    def test_per_edge_list_pages_without_other_relations(self) -> None:
        g = opened(LAYOUT_PER_EDGE)
        for i in range(10):
            g.put_edge(edge(LAYOUT_PER_EDGE, b'v', b'alpha', bytes([i]), b'alpha-rev', b'a'))
            g.put_edge(edge(LAYOUT_PER_EDGE, b'v', b'beta', bytes([100 + i]), b'beta-rev', b'b'))
        page = g.list_sides(Graph_ListSidesQuery(b'v', b'alpha', b'', 4, False))
        self.assertEqual(len(page), 4)
        self.assertTrue(all((each.Fields == b'a' for each in page)))
        rest = g.list_sides(Graph_ListSidesQuery(b'v', b'alpha', page[-1].Ref, 100, False))
        self.assertEqual(len(rest), 6)
        all_alpha = list(page) + list(rest)
        self.assertEqual([each.To for each in all_alpha], sorted((each.To for each in all_alpha)))
        self.assertEqual(g.count_sides(b'v', b'alpha'), 10)
        self.assertEqual(g.count_sides(b'v', b'beta'), 10)

    def test_count_sides_equals_list_length(self) -> None:
        for layout in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            with self.subTest(layout=layout):
                g = opened(layout)
                for i in range(7):
                    g.put_edge(edge(layout, b's', b'r', bytes([i]), b'rr'))
                listed = g.list_sides(Graph_ListSidesQuery(b's', b'r', b'', 100, False))
                self.assertEqual(g.count_sides(b's', b'r'), len(listed))

    def test_set_side_fields_keeps_endpoints(self) -> None:
        for layout in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            with self.subTest(layout=layout):
                g = opened(layout)
                ref = g.put_edge(edge(layout, b'a', b'r', b'b', b'rr', b'old'))
                self.assertEqual(g.set_side_fields(ref, b'new', b''), Committed())
                got = g.get_side(Graph_GetSideQuery(b'a', b'r', b'b'))
                self.assertTrue(got.Found)
                self.assertEqual(got.Fields, b'new')
                self.assertEqual(got.Ref, ref)
                rev = g.get_side(Graph_GetSideQuery(b'b', b'rr', b'a'))
                self.assertTrue(rev.Found)
                self.assertEqual(rev.Fields, b'new')

    def test_end_edge_leaves_active_list(self) -> None:
        for layout in (LAYOUT_COMPACT, LAYOUT_PER_EDGE):
            with self.subTest(layout=layout):
                g = opened(layout)
                keep = g.put_edge(edge(layout, b'a', b'r', b'b', b'rr', b'keep'))
                gone = g.put_edge(edge(layout, b'a', b'r', b'c', b'rr', b'gone'))
                self.assertEqual(g.end_edge(gone, b''), Committed())
                listed = g.list_sides(Graph_ListSidesQuery(b'a', b'r', b'', 100, False))
                self.assertEqual([each.To for each in listed], [b'b'])
                self.assertEqual(listed[0].Ref, keep)
                self.assertFalse(g.get_side(Graph_GetSideQuery(b'a', b'r', b'c')).Found)
                self.assertTrue(g.get_side(Graph_GetSideQuery(b'a', b'r', b'b')).Found)
                self.assertFalse(g.get_side(Graph_GetSideQuery(b'c', b'rr', b'a')).Found)

    def test_layout_mix_on_same_relation_refused(self) -> None:
        mem = Volatile()
        compact = Graph_Store(mem, LAYOUT_COMPACT)
        self.assertIsInstance(compact.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr')), bytes)
        other = Graph_Store(mem, LAYOUT_PER_EDGE)
        answer = other.put_edge(edge(LAYOUT_PER_EDGE, b'a', b'r', b'c', b'rr'))
        self.assertEqual(answer, Refused(Refusal.MALFORMED))
        self.assertEqual(answer.detail, _m_errors.Bad.LAYOUT.summary())
        self.assertEqual(compact.count_sides(b'a', b'r'), 1)

class MatchPath(unittest.TestCase):

    def test_match_one_hop_returns_structured_rows(self) -> None:
        g = opened(LAYOUT_COMPACT)
        ref = g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr', b'x'))
        rows = g.match(Graph_Pattern(2, [Graph_Pattern_Step(DIRECTION_OUT, b'r', 0, 1, b'', False)], 0, b'a', True, 10))
        self.assertEqual(len(rows), 1)
        by_slot = {each.Slot: each for each in rows[0]}
        self.assertEqual(by_slot[0].Vertex, b'a')
        self.assertEqual(by_slot[1].Vertex, b'b')
        self.assertTrue(by_slot[1].HasSide)
        self.assertEqual(by_slot[1].Side, ref)

    def test_path_stops_at_max_hops_and_trail_skips_edge_repeat(self) -> None:
        g = opened(LAYOUT_COMPACT)
        g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr'))
        g.put_edge(edge(LAYOUT_COMPACT, b'b', b'r', b'c', b'rr'))
        g.put_edge(edge(LAYOUT_COMPACT, b'c', b'r', b'a', b'rr'))
        bounded = g.path(Graph_Path_Query(b'a', b'r', DIRECTION_OUT, 1, 2, PATH_TRAIL, 100))
        ends = {row[-1].Vertex for row in bounded}
        self.assertIn(b'b', ends)
        self.assertIn(b'c', ends)
        self.assertTrue(all((1 <= len([b for b in row if b.HasSide]) <= 2 for row in bounded)))
        cycle = g.path(Graph_Path_Query(b'a', b'r', DIRECTION_OUT, 3, 3, PATH_TRAIL, 100))
        self.assertEqual(len(cycle), 1)
        self.assertEqual([b.Vertex for b in cycle[0]], [b'a', b'b', b'c', b'a'])
        again = g.path(Graph_Path_Query(b'a', b'r', DIRECTION_OUT, 3, 3, PATH_ACYCLIC, 100))
        self.assertEqual(again, [])

    def test_exists_without_full_materialise(self) -> None:
        g = opened(LAYOUT_PER_EDGE)
        for i in range(20):
            g.put_edge(edge(LAYOUT_PER_EDGE, b'a', b'r', bytes([i]), b'rr'))
        self.assertTrue(g.exists(Graph_Pattern(2, [Graph_Pattern_Step(DIRECTION_OUT, b'r', 0, 1, b'', False)], 0, b'a', True, 1)))
        self.assertFalse(g.exists(Graph_Pattern(2, [Graph_Pattern_Step(DIRECTION_OUT, b'missing', 0, 1, b'', False)], 0, b'a', True, 1)))

    def test_expand_one_hop_from_vertex(self) -> None:
        g = opened(LAYOUT_COMPACT)
        g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr', b'1'))
        g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'c', b'rr', b'2'))
        rows = g.expand(b'a', b'r', DIRECTION_OUT, 10)
        tos = sorted((next((b.Vertex for b in row if b.Slot == 1)) for row in rows))
        self.assertEqual(tos, [b'b', b'c'])

    def test_direction_in_and_either(self) -> None:
        g = opened(LAYOUT_COMPACT)
        g.put_edge(edge(LAYOUT_COMPACT, b'a', b'r', b'b', b'rr'))
        inbound = g.expand(b'b', b'r', DIRECTION_IN, 10)
        self.assertEqual([row[1].Vertex for row in inbound], [b'a'])
        either = g.expand(b'b', b'r', DIRECTION_EITHER, 10)
        self.assertEqual(sorted((row[1].Vertex for row in either)), [b'a'])
        rows = g.match(Graph_Pattern(2, [Graph_Pattern_Step(DIRECTION_IN, b'r', 0, 1, b'', False)], 0, b'b', True, 10))
        self.assertEqual(rows[0][1].Vertex, b'a')

class Forms(unittest.TestCase):

    def test_store_seam_is_forwarded(self) -> None:
        mem = Volatile()
        g = Graph_Store(mem, LAYOUT_COMPACT)
        self.assertEqual(g.batch([], [(b'raw', b'v')]), Committed())
        self.assertEqual(g.get([b'raw']), [Found(b'v', token(b'v'))])
        self.assertIn(b'raw', g.list())
        self.assertEqual(g.state(), mem.state())


    def test_not_layable_over_fixed_address_length(self) -> None:
        with self.assertRaises(_m_errors.NotLayable):
            Graph_Store(Volatile(Parameters(address_length=4)), LAYOUT_COMPACT)

    def test_put_edge_layout_must_match_laid(self) -> None:
        g = opened(LAYOUT_COMPACT)
        answer = g.put_edge(edge(LAYOUT_PER_EDGE, b'a', b'r', b'b'))
        self.assertEqual(answer, Refused(Refusal.MALFORMED))
        self.assertEqual(answer.detail, _m_errors.Bad.LAYOUT.summary())

def bare(path):
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

def own_error_types(module):
    return sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and (issubclass(each, (BaseException, enum.Enum)) or 'Refus' in name)))

class ErrorsFolder(unittest.TestCase):

    def test_the_errors_are_declared_in_the_errors_folder(self) -> None:
        self.assertEqual([each.name for each in _m_errors.Bad], ['LAYOUT', 'LIMIT', 'REF', 'PATTERN', 'EDGE'])
        self.assertTrue(all((each.summary() for each in _m_errors.Bad)))
        self.assertTrue(issubclass(_m_errors.NotLayable, ValueError))

    def test_graph_defines_no_error_type_of_its_own(self) -> None:
        self.assertEqual(own_error_types(_m_graph), [])

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        for path in (_m_graph.__file__, _m_errors.__file__, __file__):
            with self.subTest(path=Path(path).name):
                self.assertEqual(bare(path), ([], []))
if __name__ == '__main__':
    unittest.main()
