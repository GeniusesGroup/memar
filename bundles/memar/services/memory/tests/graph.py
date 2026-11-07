#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'unit'
BUDGET_SECONDS = 60
import os
import subprocess
import sys
import tempfile
import types
import unittest
import unittest.mock
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next((p for p in TESTS.parents if p.name == 'memar' and p.parent.name == 'bundles'))
TOP = SCRIPTS.parent.parent
for _folder in (TOP, SCRIPTS, SCRIPTS / 'services'):
    if str(_folder) not in sys.path:
        sys.path.insert(0, str(_folder))
sys.dont_write_bytecode = True
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_graph = import_module('modules-plugable.computer.memory.store.graph.graph')
_m_preferences = import_module('modules.computer.software.edges.manifest.services.preferences')
memory = import_module('bundles.memar.services.memory.memory')
Needs = import_module('modules-plugable.computer.memory.store.record.record').Needs
OpeningRefusal = memory.OpeningRefusal
OpenRefused = memory.OpenRefused
Graph_Store = _m_graph.Graph_Store
Graph_PutEdge = _m_graph.Graph_PutEdge
Graph_ListSidesQuery = _m_graph.Graph_ListSidesQuery
REL = uuid.UUID('01900000-0000-7000-8000-000000000001').bytes
REV = uuid.UUID('01900000-0000-7000-8000-000000000002').bytes
FROM = uuid.UUID('019a2000-0000-7000-8000-000000000001')
TO = uuid.UUID('019a2000-0000-7000-8000-000000000002')

class StandIn:

    def __init__(self, parameters) -> None:
        self.store = 'stand-in'
        self.volatile = _m_volatile.Volatile(parameters, _m_store.Limits())

    def open(self):
        return self.volatile.open()

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=_m_test_scratch.suite_scratch())
        self.addCleanup(scratch.cleanup)
        self.addCleanup(self.release_media)
        self.project = Path(scratch.name).resolve() / 'orchard'
        self.project.mkdir()
        self.parameters = _m_store.Parameters()
        self.media: list = []

    def release_media(self) -> None:
        for each in self.media:
            each.close()

    def open_graph(self):
        files = import_module('modules-plugable.computer.memory.store.files.files')
        opened = memory.open_graph(self.project, Needs())
        self.media.extend(files._OPEN.values())
        return opened

    def stand_in(self) -> None:
        module = types.SimpleNamespace(bind=lambda project, class_name: StandIn(self.parameters))
        patch = unittest.mock.patch.object(memory, 'adapter_module', lambda name: module if name == 'stand-in' else import_module('modules-plugable.computer.memory.store.files.files') if name == 'files' else None)
        patch.start()
        self.addCleanup(patch.stop)

    def prefer(self, *lines: str) -> None:
        body = ''.join((f'  {each}\n' for each in lines))
        _m_preferences.preferences_path(self.project).write_text(f'name: orchard\n{_m_preferences.BLOCK_KEY}:\n{body}', encoding='utf-8', newline='\n')

    def refused(self, reason) -> str:
        answer = memory.open_graph(self.project, Needs())
        self.assertIsInstance(answer, OpenRefused)
        self.assertEqual(answer.reason, reason)
        self.assertIn(_m_graph.GRAPH_BINDING, answer.detail)
        return answer.detail

class Opens(Fixture):

    def test_a_bound_graph_opens_as_a_graph_store_with_the_compact_layout_when_no_layout_is_named(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=stand-in')
        opened = memory.open_graph(self.project, Needs())
        self.assertIsInstance(opened, Graph_Store)
        self.assertEqual(opened.layout, _m_graph.LAYOUT_COMPACT)
        ref = opened.put_edge(Graph_PutEdge(opened.layout, FROM.bytes, REL, TO.bytes, REV))
        self.assertIsInstance(ref, bytes)
        self.assertEqual([each.To for each in opened.list_sides(Graph_ListSidesQuery(FROM.bytes, REL))], [TO.bytes])

    def test_the_layout_key_names_the_layout_of_the_graph(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=stand-in', 'graph-layout: graph=per-edge')
        self.assertEqual(memory.open_graph(self.project, Needs()).layout, _m_graph.LAYOUT_PER_EDGE)

class Refuses(Fixture):

    def test_a_project_whose_memory_key_does_not_bind_the_graph_is_not_bound(self) -> None:
        self.stand_in()
        self.prefer('memory: other=stand-in')
        self.assertIn(f'{_m_preferences.MEMORY_KEY}: other=stand-in, graph=', self.refused(OpeningRefusal.NOT_BOUND))

    def test_a_layout_word_that_is_not_one_of_the_two_is_malformed(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=stand-in', 'graph-layout: graph=fast')
        self.assertIn('fast', self.refused(OpeningRefusal.MALFORMED))

    def test_a_layout_key_that_is_not_name_value_pairs_is_malformed(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=stand-in', 'graph-layout: per-edge')
        self.refused(OpeningRefusal.MALFORMED)

    def test_a_store_that_is_not_sparse_of_any_length_is_less_than_needed(self) -> None:
        self.stand_in()
        self.parameters = _m_store.Parameters(address_length=8)
        self.prefer('memory: graph=stand-in')
        self.refused(OpeningRefusal.LESS_THAN_NEEDED)

class OverFiles(Fixture):

    def test_the_edges_stand_in_a_file_per_vertex_named_by_the_bare_uuid_and_survive_a_reopen(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=files')
        opened = self.open_graph()
        self.assertIsInstance(opened.put_edge(Graph_PutEdge(opened.layout, FROM.bytes, REL, TO.bytes, REV)), bytes)
        opened.close()
        names = sorted((each.name for each in self.project.rglob('*') if each.is_file() and each.name in (str(FROM), str(TO))))
        self.assertEqual(names, sorted([str(FROM), str(TO)]))
        again = self.open_graph()
        self.assertEqual([each.To for each in again.list_sides(Graph_ListSidesQuery(FROM.bytes, REL))], [TO.bytes])

    def test_the_absent_side_holds_over_the_files_medium(self) -> None:
        self.stand_in()
        self.prefer('memory: graph=files')
        opened = self.open_graph()
        self.assertIsInstance(opened.put_edge(Graph_PutEdge(opened.layout, FROM.bytes, REL, TO.bytes, REV)), bytes)
        step = _m_graph.Graph_Pattern_Step(_m_graph.DIRECTION_OUT, REL, 0, 1, b'', False, True)
        alone = uuid.UUID(int=TO.int + 9).bytes
        rows = opened.match(_m_graph.Graph_Pattern(2, [step], 0, alone, True, 5))
        self.assertEqual([[each.Slot for each in row] for row in rows], [[0]])
        self.assertEqual(opened.match(_m_graph.Graph_Pattern(2, [step], 0, FROM.bytes, True, 5)), [])

class OverMemarGit(Fixture):

    def git(self, *args: str) -> str:
        done = subprocess.run(['git', '-C', str(self.project), *args], capture_output=True, text=True)
        return done.stdout.strip()

    def setUp(self) -> None:
        super().setUp()
        self.git('init', '-q')
        self.data = tempfile.TemporaryDirectory(dir=_m_test_scratch.suite_scratch())
        self.addCleanup(self.data.cleanup)
        patch = unittest.mock.patch.dict(os.environ, {'LOCALAPPDATA': self.data.name, 'XDG_DATA_HOME': self.data.name})
        patch.start()
        self.addCleanup(patch.stop)

    def reopen(self):
        opened = memory.open_graph(self.project, Needs())
        self.assertIsInstance(opened, Graph_Store)
        self.addCleanup(opened.close)
        return opened

    def test_the_edges_survive_a_reopen_and_leave_the_working_tree_and_every_branch_alone(self) -> None:
        self.prefer('memory: graph=memar-git')
        opened = self.reopen()
        self.assertIsInstance(opened.put_edge(Graph_PutEdge(opened.layout, FROM.bytes, REL, TO.bytes, REV)), bytes)
        opened.close()
        again = self.reopen()
        self.assertEqual([each.To for each in again.list_sides(Graph_ListSidesQuery(FROM.bytes, REL))], [TO.bytes])
        self.assertEqual([each for each in self.project.rglob('*') if each.is_file() and each.name in (str(FROM), str(TO))], [])
        self.assertEqual(self.git('for-each-ref', '--format=%(refname)', 'refs/heads'), '')
        self.assertEqual(self.git('for-each-ref', '--format=%(refname)', 'refs/memar'), 'refs/memar/graph')

if __name__ == '__main__':
    unittest.main()
