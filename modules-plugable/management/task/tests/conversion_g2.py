#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import json
import sys
import tempfile
import unittest
import uuid
from importlib import import_module
from pathlib import Path
TESTS = Path(__file__).resolve().parent
TOP = next(p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir())
SCRIPTS = TOP / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS / 'services'))
sys.path.insert(1, str(SCRIPTS))
sys.path.insert(2, str(TOP))
sys.path.insert(3, str(TESTS))
sys.dont_write_bytecode = True
from machine.plugable_import import load as plugable_load
suite_scratch = plugable_load('computer.memory.filesystem.services.fs_test_scratch').suite_scratch
import earlier_shape
BUDGET_SECONDS = 60
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_files = import_module('modules-plugable.computer.memory.store.files.files')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
conversion = import_module('modules-plugable.management.task.services.task_conversion')
generation = import_module('modules-plugable.management.task.services.task_generation')
g2_encode = import_module('modules-plugable.management.task.services.task_g2_encode')
g2_convert = import_module('modules-plugable.management.task.services.task_conversion_g2')
task_files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
META_FOLDER = _m_files.META_FOLDER
record_key = _m_record.key
PLAN_BODY = '# T\n\n## Request\nDo the thing.\n\n## Why\nw\n\n## Steps\n- [ ] 1. a\n\n## Next\nn\n'
REPORT_BODY = '# Report\n\n## Result\nIt came to this.\n\n## Decisions needed\n- none\n'


class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.root = Path(self.scratch.name)
        self.project = self.root / 'project'
        self.project.mkdir()
        self.memory = self.root / 'memory'
        self.memory.mkdir()
        self._store = None

    def open_store(self):
        adapter = _m_files.FilesAdapter(str(self.project), memory_root=str(self.memory))
        self.addCleanup(adapter.close)
        self._store = adapter.open()
        return self._store

    def g1_yaml(self, name: str = 'T-1', status: str = 'queued', priority: int = 7, plan: bool = True, report: bool = True) -> Path:
        folder = self.root / name
        folder.mkdir()
        task_files.create_task(folder, name, 'A: title', None, None, Path('/work'), status, priority, None, None)
        if plan:
            timeline_files.add_text(folder, 'plan', PLAN_BODY, 'agent')
        if report:
            timeline_files.add_text(folder, 'report', REPORT_BODY, 'agent', fields={'status': 'complete'})
        return folder

    def g1_plan_md(self, name: str = 'T-old', status: str = 'active', priority: int = 5) -> Path:
        folder = self.root / name
        folder.mkdir()
        earlier_shape.create_plan_md(folder, name, 'A: title', None, None, Path('/work'), status, priority, None, None)
        return folder

    def convert(self, folder: Path) -> bytes:
        return g2_convert.convert_g1_folder(folder, self.open_store())

    def task_part(self, task_id: bytes) -> dict:
        return g2_convert.dump_task_part(self.open_store(), task_id)

    def node_id_files(self) -> list[Path]:
        return [path for path in self.memory.rglob('*') if path.is_file() and META_FOLDER not in path.parts]


class EqualAnswers(Fixture):

    def test_title_and_priority_on_task_status_as_label_edge(self) -> None:
        folder = self.g1_yaml(priority=9, status='active')
        before = conversion.answers(folder)
        task_id = self.convert(folder)
        part = self.task_part(task_id)
        self.assertEqual(part['title'], before['facts']['title'])
        self.assertEqual(part['priority'], int(before['facts']['priority']))
        self.assertNotIn('status', part)
        self.assertEqual(g2_convert.read_status_label(self.open_store(), task_id), before['facts']['status'])

    def test_plan_md_facts_match_the_adapter(self) -> None:
        folder = self.g1_plan_md(priority=3, status='complete')
        before = conversion.answers(folder)
        task_id = self.convert(folder)
        part = self.task_part(task_id)
        self.assertEqual(part['title'], before['facts']['title'])
        self.assertEqual(part['priority'], int(before['facts']['priority']))
        self.assertNotIn('status', part)
        self.assertEqual(g2_convert.read_status_label(self.open_store(), task_id), before['facts']['status'])


class Events(Fixture):

    def test_each_g1_content_is_an_event_is_side_without_filenames(self) -> None:
        folder = self.g1_yaml()
        task_id = self.convert(folder)
        store = self.open_store()
        sides = g2_convert.list_event_is(store, task_id)
        self.assertEqual(len(sides), 2)
        self.assertEqual([part['number'] for part in sides], [1, 2])
        for side in sides:
            self.assertNotIn('kind', side)
            self.assertNotIn('.md', json.dumps(side))
            content_id = uuid.UUID(side['to']).bytes
            held = store.get([record_key(content_id, g2_encode.CONTENT)])[0]
            self.assertIsInstance(held, _m_store.Found)
            content_part = json.loads(held.value.decode('utf-8'))
            text_id = uuid.UUID(content_part['text']).bytes
            text = store.get([record_key(text_id, g2_encode.TEXT)])[0]
            self.assertIsInstance(text, _m_store.Found)
            self.assertTrue(text.value.startswith(b'# '))
        kinds = [json.loads(store.get([record_key(uuid.UUID(side['to']).bytes, g2_encode.CONTENT)])[0].value)['kind'] for side in sides]
        self.assertEqual(kinds, ['plan', 'report'])

    def test_plan_only_has_one_event_is_side(self) -> None:
        folder = self.g1_yaml(report=False)
        task_id = self.convert(folder)
        sides = g2_convert.list_event_is(self.open_store(), task_id)
        self.assertEqual(len(sides), 1)
        content = json.loads(self.open_store().get([record_key(uuid.UUID(sides[0]['to']).bytes, g2_encode.CONTENT)])[0].value)
        self.assertEqual(content['kind'], 'plan')


class Layout(Fixture):

    def test_record_nodes_are_addressable_without_counting_adapter_files(self) -> None:
        folder = self.g1_yaml()
        task_id = self.convert(folder)
        store = self.open_store()
        self.assertIsInstance(store.get([record_key(task_id, g2_encode.TASK)])[0], _m_store.Found)
        sides = g2_convert.list_event_is(store, task_id)
        self.assertEqual(len(sides), len(timeline_files.read_contents(folder)))
        for side in sides:
            content_id = uuid.UUID(side['to']).bytes
            self.assertIsInstance(store.get([record_key(content_id, g2_encode.CONTENT)])[0], _m_store.Found)


class Legacy(Fixture):

    def test_the_g1_folder_name_is_kept_as_legacy_id(self) -> None:
        folder = self.g1_yaml(name='20261019-T170853Z-4740')
        task_id = self.convert(folder)
        part = self.task_part(task_id)
        self.assertEqual(part['legacy_id'], '20261019-T170853Z-4740')
        self.assertTrue(_m_record.is_id(task_id))


class TypeStamp(Fixture):

    def test_the_task_part_carries_type_uuid(self) -> None:
        task_id = self.convert(self.g1_yaml())
        part = self.task_part(task_id)
        self.assertEqual(part['type_uuid'], generation.G2_TYPE_UUID)
        self.assertNotIn('writer', part)


class Inspection(Fixture):

    def test_no_homemade_domains_dump_helper(self) -> None:
        self.assertFalse(hasattr(g2_convert, 'dump_sample'))

    def test_inspect_via_graph_and_store_services(self) -> None:
        task_id = self.convert(self.g1_yaml())
        store = self.open_store()
        part = g2_convert.dump_task_part(store, task_id)
        status = g2_convert.read_status_label(store, task_id)
        sides = g2_convert.list_event_is(store, task_id)
        self.assertNotIn('domains', part)
        self.assertNotIn('placements', part)
        self.assertNotIn('status', part)
        self.assertIn(status, ('queued', 'active', 'blocked', 'complete'))
        self.assertEqual(len(sides), 2)
        for side in sides:
            self.assertNotIn('relation', side)
            self.assertNotIn('reverse', side)

    def test_conversion_writes_no_labels_record_part(self) -> None:
        task_id = self.convert(self.g1_yaml())
        answer = self.open_store().get([record_key(task_id, g2_encode.LABELS)])[0]
        self.assertNotIsInstance(answer, _m_store.Found)


if __name__ == '__main__':
    unittest.main()
