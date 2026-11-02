#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.identity.thing.labels.Label_Queued import Label_Queued
import sys
import tempfile
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
from machine.plugable_import import load as plugable_load
suite_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch').suite_scratch
BUDGET_SECONDS = 30
_m_files = import_module('modules-plugable.computer.memory.store.files.files')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_attach = import_module('modules.knowledge.label.services.attach')
Graph_Store = _m_graph.Graph_Store
LAYOUT_COMPACT = _m_graph.LAYOUT_COMPACT

class Attach(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        root = Path(self.scratch.name)
        project = root / 'project'
        project.mkdir()
        memory = root / 'memory'
        memory.mkdir()
        adapter = _m_files.FilesAdapter(str(project), memory_root=str(memory))
        self.addCleanup(adapter.close)
        self.store = adapter.open()
        self.graph = Graph_Store(self.store, LAYOUT_COMPACT)

    def test_put_label_uses_label_relation_to_status_uuid(self) -> None:
        thing = uuid.uuid7().bytes
        queued = Label_Queued.label
        _attach.put_label(self.graph, thing, queued)
        held = _attach.list_label_ids(self.graph, thing)
        self.assertEqual(held, [_attach.id_bytes(queued)])
        self.assertEqual(self.graph.count_sides(thing, b'queued'), 0)

if __name__ == '__main__':
    unittest.main()
