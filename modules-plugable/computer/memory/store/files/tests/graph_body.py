#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import sys
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
BUDGET_SECONDS = 60
_m_files = import_module('modules-plugable.computer.memory.store.files.files')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_store = import_module('modules.computer.memory.store.protocol.store')
Committed = _m_store.Committed
Found = _m_store.Found
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
DIRECTION_IN = _m_graph.DIRECTION_IN
REL = uuid.UUID('01900000-0000-7000-8000-0000000000a1').bytes
REV = uuid.UUID('01900000-0000-7000-8000-0000000000a2').bytes
FIELD = str(uuid.UUID('01900000-0000-7000-8000-0000000000f1'))
MADE: list = []

def make_local():
    folder = _m_scratch.suite_scratch() / f'files-graph-{uuid.uuid4().hex[:12]}'
    project = folder / 'project'
    project.mkdir(parents=True)
    root = folder / 'memory'
    adapter = _m_files.FilesAdapter(str(project), memory_root=str(root))
    MADE.append((adapter, folder))
    return adapter, root

def clean_up() -> None:
    while MADE:
        adapter, folder = MADE.pop()
        if adapter is not None:
            adapter.close()
        if folder.exists():
            _m_scratch.remove_tree(folder)

class GraphInVertexFile(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_compact_edges_land_as_relation_arrays_on_vertex_uuid_file(self) -> None:
        adapter, root = make_local()
        store = adapter.open()
        graph = Graph_Store(store, LAYOUT_COMPACT)
        left = uuid.UUID('01900000-0000-7000-8000-0000000000aa').bytes
        right = uuid.UUID('01900000-0000-7000-8000-0000000000bb').bytes
        fields = json.dumps({FIELD: 1}, separators=(',', ':')).encode('utf-8')
        ref = graph.put_edge(Graph_PutEdge(LAYOUT_COMPACT, left, REL, right, REV, fields))
        self.assertIsInstance(ref, bytes)
        names = sorted(path.name for path in root.iterdir() if path.is_file())
        self.assertEqual(names, [
            '01900000-0000-7000-8000-0000000000aa',
            '01900000-0000-7000-8000-0000000000bb',
        ])
        left_body = json.loads((root / names[0]).read_text(encoding='utf-8'))
        rel_key = str(uuid.UUID(bytes=REL))
        self.assertIn(rel_key, left_body)
        self.assertNotIn('domains', left_body)
        self.assertNotIn('task', left_body)
        self.assertIsInstance(left_body[rel_key], list)
        side = left_body[rel_key][0]
        self.assertEqual(set(side.keys()), set(_m_side.SIDE_KEYS))
        self.assertEqual(side[_m_side.TO_KEY], '01900000-0000-7000-8000-0000000000bb')
        self.assertEqual(side[_m_side.FIELDS_KEY], {FIELD: 1})
        self.assertNotIn('inbound_ref', side)
        self.assertNotIn('reverse_ref', side)
        right_body = json.loads((root / names[1]).read_text(encoding='utf-8'))
        rev_key = str(uuid.UUID(bytes=REV))
        self.assertIn(rev_key, right_body)
        for body in (left_body, right_body):
            for key in body:
                self.assertFalse(key.startswith('@') or key.startswith('<'), key)
        listed = graph.list_sides(Graph_ListSidesQuery(left, REL))
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0].To, right)
        self.assertEqual(json.loads(listed[0].Fields.decode('utf-8')), {FIELD: 1})
        inbound = graph.expand(right, REL, DIRECTION_IN, 0)
        self.assertEqual(len(inbound), 1)
        self.assertEqual(inbound[0][1].Vertex, left)

    def test_reload_round_trips_graph_sides(self) -> None:
        adapter, root = make_local()
        store = adapter.open()
        graph = Graph_Store(store, LAYOUT_COMPACT)
        left = uuid.UUID('01900000-0000-7000-8000-0000000000cc').bytes
        right = uuid.UUID('01900000-0000-7000-8000-0000000000dd').bytes
        graph.put_edge(Graph_PutEdge(LAYOUT_COMPACT, left, REL, right, REV, b''))
        adapter.close()
        MADE.clear()
        again = _m_files.FilesAdapter(str(root.parent / 'project'), memory_root=str(root))
        MADE.append((again, root.parent))
        store2 = again.open()
        graph2 = Graph_Store(store2, LAYOUT_COMPACT)
        listed = graph2.list_sides(Graph_ListSidesQuery(left, REL))
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0].To, right)

if __name__ == '__main__':
    unittest.main()
