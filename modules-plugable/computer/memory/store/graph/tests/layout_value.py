#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 30
import sys
import unittest
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
sys.path.insert(0, str(TOP))
sys.dont_write_bytecode = True
_m_codec = import_module('modules-plugable.computer.memory.store.graph.codecs.layout_value')
Graph_Default_Layout_Value_Codec = _m_codec.Graph_Default_Layout_Value_Codec
Stored_Side = _m_codec.Stored_Side
Stored_Edge_Value = _m_codec.Stored_Edge_Value

class LayoutValueRoundTrip(unittest.TestCase):

    def test_compact_sides_round_trip_keeps_opaque_fields(self) -> None:
        codec = Graph_Default_Layout_Value_Codec()
        sides = [Stored_Side(1, b'to-a', b'\xfffields', False, b'rev', b'in'), Stored_Side(2, b'to-b', b'{}', True, b'', b'')]
        value = codec.pack_compact(sides)
        self.assertIsInstance(value, bytes)
        self.assertTrue(value)
        back = codec.unpack_compact(value)
        self.assertEqual(len(back), 2)
        self.assertEqual(back[0].slot, 1)
        self.assertEqual(back[0].to, b'to-a')
        self.assertEqual(back[0].fields, b'\xfffields')
        self.assertFalse(back[0].ended)
        self.assertEqual(back[0].reverse_ref, b'rev')
        self.assertEqual(back[0].inbound_ref, b'in')
        self.assertEqual(back[1].slot, 2)
        self.assertTrue(back[1].ended)

    def test_per_edge_value_round_trip_keeps_opaque_fields(self) -> None:
        codec = Graph_Default_Layout_Value_Codec()
        edge = Stored_Edge_Value(b'far', b'\x00\x01', False, b'out', b'inb')
        value = codec.pack_per_edge(edge)
        back = codec.unpack_per_edge(value)
        self.assertEqual(back.to, b'far')
        self.assertEqual(back.fields, b'\x00\x01')
        self.assertFalse(back.ended)
        self.assertEqual(back.reverse_ref, b'out')
        self.assertEqual(back.inbound_ref, b'inb')

if __name__ == '__main__':
    unittest.main()
