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
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
_m_files = import_module('modules-plugable.computer.memory.store.files.files')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_errors = import_module('modules-plugable.computer.memory.store.files.errors.errors')
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
BadBody = _m_errors.BadBody
REL = uuid.UUID('01900000-0000-7000-8000-0000000000a1').bytes
REV = uuid.UUID('01900000-0000-7000-8000-0000000000a2').bytes
FIELD = str(uuid.UUID('01900000-0000-7000-8000-0000000000f1'))
LEFT = uuid.UUID('01900000-0000-7000-8000-0000000000aa').bytes
RIGHT = uuid.UUID('01900000-0000-7000-8000-0000000000bb').bytes
MADE: list = []

def make_local():
    folder = _m_scratch.suite_scratch() / f'files-refuse-{uuid.uuid4().hex[:12]}'
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

class RefuseBody(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_disk_side_uses_structural_type_uuids(self) -> None:
        adapter, root = make_local()
        store = adapter.open()
        graph = Graph_Store(store, LAYOUT_COMPACT)
        fields = json.dumps({FIELD: 1}, separators=(',', ':')).encode('utf-8')
        ref = graph.put_edge(Graph_PutEdge(LAYOUT_COMPACT, LEFT, REL, RIGHT, REV, fields))
        self.assertIsInstance(ref, bytes)
        left_body = json.loads((root / str(uuid.UUID(bytes=LEFT))).read_text(encoding='utf-8'))
        rel_key = str(uuid.UUID(bytes=REL))
        self.assertIn(rel_key, left_body)
        side = left_body[rel_key][0]
        self.assertEqual(set(side.keys()), set(_m_side.SIDE_KEYS))
        self.assertEqual(side[_m_side.TO_KEY], str(uuid.UUID(bytes=RIGHT)))
        self.assertEqual(side[_m_side.FIELDS_KEY], {FIELD: 1})
        self.assertNotIn('slot', side)
        self.assertNotIn('fields', side)

    def test_task_blob_part_is_refused(self) -> None:
        adapter, root = make_local()
        store = adapter.open()
        with self.assertRaises(BadBody):
            store.batch([], [(LEFT + b'task', json.dumps({'Title': 'x'}).encode('utf-8'))])

if __name__ == '__main__':
    unittest.main()
