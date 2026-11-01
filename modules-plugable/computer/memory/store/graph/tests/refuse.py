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
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_errors = import_module('modules-plugable.computer.memory.store.graph.errors.errors')
_m_side = import_module('modules-plugable.computer.memory.store.graph.side_structural')
Refusal = _m_store.Refusal
Refused = _m_store.Refused
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT
Bad = _m_errors.Bad
REL = uuid.UUID('01900000-0000-7000-8000-0000000000a1').bytes
REV = uuid.UUID('01900000-0000-7000-8000-0000000000a2').bytes
FIELD = str(uuid.UUID('01900000-0000-7000-8000-0000000000f1'))
FROM = uuid.UUID('01900000-0000-7000-8000-0000000000aa').bytes
TO = uuid.UUID('01900000-0000-7000-8000-0000000000bb').bytes

class RefuseNonGraph(unittest.TestCase):

    def test_ascii_relation_is_refused(self) -> None:
        g = Graph_Store(_m_volatile.Volatile(), LAYOUT_COMPACT)
        answer = g.put_edge(Graph_PutEdge(LAYOUT_COMPACT, FROM, b'knows', TO, b'known-by', b''))
        self.assertIsInstance(answer, Refused)
        self.assertEqual(answer.reason, Refusal.MALFORMED)
        self.assertEqual(answer.detail, Bad.RELATION.summary())

    def test_uuid_relation_with_english_field_keys_is_refused(self) -> None:
        g = Graph_Store(_m_volatile.Volatile(), LAYOUT_COMPACT)
        fields = json.dumps({'priority': 9}).encode('utf-8')
        answer = g.put_edge(Graph_PutEdge(LAYOUT_COMPACT, FROM, REL, TO, REV, fields))
        self.assertIsInstance(answer, Refused)
        self.assertEqual(answer.detail, Bad.FIELDS.summary())

    def test_uuid_relation_and_typeuuid_fields_commit(self) -> None:
        g = Graph_Store(_m_volatile.Volatile(), LAYOUT_COMPACT)
        fields = json.dumps({FIELD: 9}, separators=(',', ':')).encode('utf-8')
        answer = g.put_edge(Graph_PutEdge(LAYOUT_COMPACT, FROM, REL, TO, REV, fields))
        self.assertIsInstance(answer, bytes)

    def test_structural_type_uuids_are_stable(self) -> None:
        self.assertEqual(_m_side.SLOT_KEY, '14b8fadd-67f5-5560-b71a-e6f47c61ade7')
        self.assertEqual(_m_side.TO_KEY, '1a18347a-eecb-5a57-bdcb-23af66b3dc51')
        self.assertEqual(_m_side.FIELDS_KEY, 'b986aa4f-b3b8-56c6-8887-92ba94a91aa4')
        self.assertEqual(_m_side.ENDED_KEY, 'fd6b5b2a-f0f5-5fd9-bb92-d486e2b1cc51')

if __name__ == '__main__':
    unittest.main()
