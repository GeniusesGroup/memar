#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import ast
import io
import json
import os
import sys
import tokenize
import unittest
import uuid
from importlib import import_module
from pathlib import Path
from typing import Any
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_files = import_module('modules-plugable.computer.memory.store.files.files')
_m_cases = import_module('modules-plugable.computer.memory.store.files.cases')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_record_tests = import_module('modules-plugable.computer.memory.store.record.tests.record')
Capability = _m_store.Capability
Committed = _m_store.Committed
Found = _m_store.Found
token = _m_store.token
address = _m_conformance.address
value = _m_conformance.value
TIER = 'system'
BUDGET_SECONDS = 180
BUDGET_SCALE = 10
SLOW = frozenset({'test_batch_visible_whole', 'test_kill_during_batch_is_atomic', 'test_model_equivalence', 'test_paused_live_writer_is_not_overtaken', 'test_many_nodes'})
MADE: list[tuple[Any, Path]] = []

def scratch_project() -> tuple[Path, Path]:
    folder = _m_scratch.suite_scratch() / f'files-store-{uuid.uuid4().hex[:12]}'
    project = folder / 'project'
    project.mkdir(parents=True)
    return (folder, project)

def make_local(**keywords: Any) -> Any:
    folder, project = scratch_project()
    root = folder / 'memory'
    adapter = _m_files.FilesAdapter(str(project), memory_root=str(root), **keywords)
    MADE.append((adapter, folder))
    return adapter

def clean_up() -> None:
    while MADE:
        adapter, folder = MADE.pop()
        if adapter is not None:
            adapter.close()
        if folder.exists():
            _m_scratch.remove_tree(folder)

def _only(base: type[unittest.TestCase], names: set[str], name: str) -> type[unittest.TestCase]:
    attributes: dict[str, Any] = {'tearDown': lambda self: clean_up()}
    attributes.update({each: getattr(base, each) for each in dir(base) if each in names})
    return type(name, (unittest.TestCase,), attributes)
_local = _m_conformance.test_case(make_local, _m_cases.CASES, budget_scale=BUDGET_SCALE)
Local = type('Local', (_local,), {'tearDown': lambda self: clean_up(), **dict.fromkeys(SLOW)})
_record = _m_record_tests.group(lambda: _m_record.RecordAdapter(make_local()), _m_record_tests.CASES)
LocalRecord = type('LocalRecord', (_record,), {'tearDown': lambda self: clean_up(), **dict.fromkeys(SLOW & {each for each in dir(_record) if each.startswith('test_')})})
BASES = {'Local': _local, 'LocalRecord': _record}
del _local, _record

class EveryOwedCaseRuns(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_the_durable_group_applies_and_shared_does_not(self) -> None:
        store = make_local().open()
        durable = {each.name for each in _m_conformance.CASES if each.group == 'durable'}
        shared = {each.name for each in _m_conformance.CASES if each.group == 'shared'}
        applied = _m_conformance.applied(store)
        self.assertEqual(durable - applied, set())
        self.assertEqual(shared & applied, set())
        self.assertEqual([each.name for each in _m_conformance.CASES if each.owed], [])

    def test_declares_what_the_document_says(self) -> None:
        store = make_local().open()
        self.assertEqual(store.capabilities, frozenset({Capability.ATOMIC_BATCH, Capability.DURABLE}))
        self.assertNotIn(Capability.LEAVES_WORKING_TREE_UNTOUCHED, store.capabilities)
        self.assertNotIn(Capability.FALLBACK, store.capabilities)
        self.assertNotIn(Capability.REPLICATED, store.capabilities)

class PathEncoding(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_record_key_path_is_only_the_id_segment(self) -> None:
        identity = bytes.fromhex('0190000000007000800000000000000a')
        at = identity + b'task'
        relative = str(_m_files.Files_Path().relative_path(at))
        self.assertEqual(relative, '01900000-0000-7000-8000-00000000000a')
        self.assertEqual(_m_files.Files_Path().file_identity(relative), (identity, True))

    def test_other_addresses_use_hex_of_the_whole_address(self) -> None:
        at = b'k' + (1).to_bytes(4, 'big')
        relative = str(_m_files.Files_Path().relative_path(at))
        self.assertEqual(relative, at.hex())
        self.assertEqual(_m_files.Files_Path().file_identity(relative), (at, False))

    def test_sharding_inserts_hex_prefix_of_id_not_domain(self) -> None:
        identity = bytes.fromhex('0190000000007000800000000000000a')
        at = identity + b'task'
        relative = str(_m_files.Files_Path().relative_path(at, 4, True))
        self.assertEqual(relative, '0190/01900000-0000-7000-8000-00000000000a')
        self.assertEqual(_m_files.Files_Path().file_identity(relative), (identity, True))

    def test_no_media_suffix_is_forced(self) -> None:
        at = b'k' + (2).to_bytes(4, 'big')
        relative = str(_m_files.Files_Path().relative_path(at))
        self.assertFalse(relative.endswith('.md'))

class Medium(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_edge_and_reverse_are_two_addresses_in_one_batch(self) -> None:
        adapter = make_local()
        store = adapter.open()
        edge, reverse = (address(store, 10), address(store, 11))
        self.assertEqual(store.batch([], [(edge, b'e'), (reverse, b'r')]), Committed())
        self.assertEqual([each.get_file_data() for each in (adapter.file_at(edge), adapter.file_at(reverse))], [b'e', b'r'])

    def test_one_node_id_holds_many_domain_parts_in_one_file(self) -> None:
        adapter = make_local()
        store = adapter.open()
        identity = bytes.fromhex('0190000000007000800000000000000a')
        task, timeline = (identity + b'task', identity + b'timeline')
        self.assertEqual(store.batch([], [(task, b'T'), (timeline, b'L')]), Committed())
        self.assertEqual(adapter.file_at(task).host_path(), adapter.file_at(timeline).host_path())
        parts = _m_files.unpack_parts(adapter.file_at(task).get_file_data())
        self.assertEqual(parts, {b'task': b'T', b'timeline': b'L'})
        self.assertEqual(store.get([task, timeline]), [Found(b'T', token(b'T')), Found(b'L', token(b'L'))])

    def test_node_file_body_is_a_json_object_without_binary_length_prefix(self) -> None:
        adapter = make_local()
        store = adapter.open()
        identity = bytes.fromhex('0190000000007000800000000000000b')
        task, timeline = (identity + b'task', identity + b'timeline')
        task_value = b'{"Status":"Active","Title":"sample"}'
        timeline_value = b'[{"kind":"plan"}]'
        self.assertEqual(store.batch([], [(task, task_value), (timeline, timeline_value)]), Committed())
        body = adapter.file_at(task).get_file_data()
        self.assertTrue(body.startswith(b'{'))
        self.assertTrue(body.endswith(b'\n'))
        self.assertNotIn(b'\x00\x04task', body)
        on_disk = json.loads(body.decode('utf-8'))
        self.assertEqual(on_disk, {'task': {'Status': 'Active', 'Title': 'sample'}, 'timeline': [{'kind': 'plan'}]})
        self.assertNotIn(_m_files.BYTES_ENVELOPE, json.dumps(on_disk))
        self.assertNotIn(_m_files.TEXT_ENVELOPE, json.dumps(on_disk))
        canonical_task = json.dumps(on_disk['task'], separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        canonical_timeline = json.dumps(on_disk['timeline'], separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        self.assertEqual(store.get([task, timeline]), [Found(canonical_task, token(canonical_task)), Found(canonical_timeline, token(canonical_timeline))])

    def test_uses_storage_directory_and_file(self) -> None:
        adapter = make_local()
        storage = import_module('modules-plugable.computer.memory.filesystem.storage')
        self.assertIsInstance(adapter.get_memory_root(), storage.Storage_Directory)
        store = adapter.open()
        put_at = address(store, 1)
        self.assertEqual(store.batch([], [(put_at, value(store, 1))]), Committed())
        self.assertIsInstance(adapter.file_at(put_at), storage.Storage_File)

class Binding(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def project_with(self, block: str) -> Path:
        folder, project = scratch_project()
        MADE.append((None, folder))
        (project / 'manifest.yaml').write_text(block, encoding='utf-8')
        return project

    def test_memory_root_defaults_and_is_read_from_its_key(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=files, other=files\n  files-memory-root: other=memory/other\n')
        one, two = (_m_files.bind(project, 'work-records'), _m_files.bind(project, 'other'))
        self.assertTrue(str(one.get_memory_root().host_path()).endswith(str(Path('.agents') / 'memar' / 'memory')))
        self.assertTrue(str(two.get_memory_root().host_path()).endswith(str(Path('memory') / 'other')))
        self.assertTrue(one.same_store(_m_files.bind(project, 'work-records')))
        self.assertFalse(one.same_store(two))
        one.close()
        two.close()

    def test_nested_roots_are_refused_and_shared_roots_are_not(self) -> None:
        project = self.project_with('memar:\n  memory: a=files, b=files\n  files-memory-root: a=memory/a, b=memory/a/nested\n')
        first = _m_files.bind(project, 'a')
        first.close()
        with self.assertRaises(errors_module().RootCollision):
            _m_files.bind(project, 'b')
        shared = self.project_with('memar:\n  memory: a=files, b=files\n  files-memory-root: a=memory/shared, b=memory/shared\n')
        left, right = (_m_files.bind(shared, 'a'), _m_files.bind(shared, 'b'))
        self.assertTrue(left.same_store(right))
        left.close()
        right.close()

    def test_a_broken_parameter_is_refused(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=files\n  files-shard-threshold: work-records=nope\n')
        with self.assertRaises(errors_module().BadParameter):
            _m_files.bind(project, 'work-records')

class Errors(unittest.TestCase):

    def test_the_errors_are_in_the_errors_folder_and_say_what_they_are(self) -> None:
        errors = errors_module()
        raised = import_module('modules.computer.memory.store.errors.errors')
        for name in ('BadParameter', 'BadAddress', 'RootCollision', 'Lost'):
            with self.subTest(name=name):
                self.assertTrue(getattr(errors, name)().summary())
        self.assertEqual(errors.BadAddress().reason, raised.Refusal.MALFORMED)
        self.assertEqual(errors.RootCollision().reason, raised.Refusal.MALFORMED)
        self.assertEqual(errors.Lost().reason, raised.Unavailability.FAILED)

    def test_the_realization_makes_no_error_type_of_its_own(self) -> None:
        for module in (_m_files, _m_cases):
            own = sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and issubclass(each, BaseException)))
            self.assertEqual(own, [])

def errors_module() -> Any:
    return import_module('modules-plugable.computer.memory.store.files.errors.errors')

def bare(path: str) -> tuple[list[int], list[int]]:
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        here = Path(__file__).resolve().parent
        module = here.parent
        for path in (module / 'files.py', module / 'cases.py', module / 'errors' / 'errors.py', here / 'files.py'):
            with self.subTest(path=path.name):
                self.assertEqual(bare(str(path)), ([], []))

def tearDownModule() -> None:
    clean_up()
if __name__ == '__main__':
    unittest.main()
