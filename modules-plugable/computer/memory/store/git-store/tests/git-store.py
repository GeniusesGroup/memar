#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import ast
import io
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import tokenize
import types
import unittest
import uuid
from importlib import import_module
from pathlib import Path
from typing import Any, Callable
TESTS = Path(__file__).resolve().parent
TOP = next((p for p in TESTS.parents if (p / 'modules-plugable').is_dir() and (p / 'bundles').is_dir()))
for _each in (TOP / 'bundles' / 'memar' / 'services', TOP):
    if str(_each) not in sys.path:
        sys.path.insert(0, str(_each))
sys.dont_write_bytecode = True
_m_store = import_module('modules.computer.memory.store.protocol.store')
_m_conformance = import_module('modules.computer.memory.conformance.conformance')
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_git_store = import_module('modules-plugable.computer.memory.store.git-store.git-store')
_m_cases = import_module('modules-plugable.computer.memory.store.git-store.cases')
_m_lockable = import_module('modules-plugable.computer.memory.store.lockable.lockable')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_record_tests = import_module('modules-plugable.computer.memory.store.record.tests.record')
Capability = _m_store.Capability
Committed = _m_store.Committed
OWED = _m_conformance.OWED
address = _m_conformance.address
value = _m_conformance.value
TIER = 'system'
BUDGET_SECONDS = 180
BUDGET_SCALE = 10
SLOW_LOCAL = frozenset({'test_batch_visible_whole', 'test_kill_during_batch_is_atomic', 'test_model_equivalence', 'test_paused_live_writer_is_not_overtaken'})
SLOW_RECORD = frozenset({'test_batch_visible_whole', 'test_many_nodes'})
MADE: list[tuple[Any, Path]] = []

def _git(where: Path, *args: str) -> None:
    subprocess.run(['git', '-C', str(where), '-c', 'user.name=suite', '-c', 'user.email=suite@example.invalid', *args], check=True, capture_output=True)

_PROJECT_TEMPLATE: list[Path] = []

def project_template() -> Path:
    if not _PROJECT_TEMPLATE:
        import atexit
        import tempfile
        holder = tempfile.TemporaryDirectory(dir=_m_scratch.suite_scratch(), prefix='git-store-template-', ignore_cleanup_errors=True)
        atexit.register(holder.cleanup)
        project = Path(holder.name) / 'project'
        project.mkdir()
        _git(project, 'init', '-q')
        (project / 'tracked.txt').write_bytes(b'tracked\n')
        (project / '.gitignore').write_bytes(b'ignored.txt\n')
        (project / 'ignored.txt').write_bytes(b'ignored\n')
        _git(project, 'add', 'tracked.txt', '.gitignore')
        _git(project, 'commit', '-q', '-m', 'scratch')
        _PROJECT_TEMPLATE.append(project)
    return _PROJECT_TEMPLATE[0]

def scratch_project() -> tuple[Path, Path, Path]:
    folder = _m_scratch.suite_scratch() / f'git-store-{uuid.uuid4().hex[:12]}'
    project, data = (folder / 'project', folder / 'data')
    folder.mkdir(parents=True)
    shutil.copytree(project_template(), project)
    data.mkdir()
    return (folder, project, data)

def make_local(**keywords: Any) -> Any:
    folder, project, data = scratch_project()
    adapter = _m_git_store.GitStoreAdapter(str(project), 'refs/memar/work-records', data_area=str(data), **keywords)
    MADE.append((adapter, folder))
    return adapter

def make_replicated() -> Any:
    folder, project, data = scratch_project()
    shared = folder / 'shared.git'
    subprocess.run(['git', 'init', '-q', '--bare', str(shared)], check=True, capture_output=True)
    adapter = _m_git_store.GitStoreAdapter(str(project), 'refs/memar/work-records', data_area=str(data), shared=str(shared))
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
_local = _m_conformance.test_case(make_local, _m_cases.CASES + _m_lockable.CASES, budget_scale=BUDGET_SCALE)
Local = type('Local', (_local,), {'tearDown': lambda self: clean_up(), **dict.fromkeys(SLOW_LOCAL)})
_replicated = _m_conformance.test_case(make_replicated, _m_cases.REPLICATED_CASES)
Replicated = _only(_replicated, {'test_' + each.check.__name__ for each in _m_cases.REPLICATED_CASES}, 'Replicated')
_record = _m_record_tests.group(lambda: _m_record.RecordAdapter(make_local()), _m_record_tests.CASES)
LocalRecord = type('LocalRecord', (_record,), {'tearDown': lambda self: clean_up(), **dict.fromkeys(SLOW_RECORD)})
BASES = {'Local': _local, 'LocalRecord': _record}
del _local, _replicated, _record

class EveryOwedCaseRuns(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_the_durable_and_shared_groups_apply(self) -> None:
        store = make_local().open()
        waited = {each.name for each in _m_conformance.CASES if each.group in ('durable', 'shared')}
        self.assertEqual(len(waited), 8)
        self.assertEqual(waited - _m_conformance.applied(store), set())
        self.assertEqual([each.name for each in _m_conformance.CASES if each.owed], [])

    def test_records_cross_process_case_applies(self) -> None:
        store = _m_record.RecordAdapter(make_local()).open()
        crossing = [each for each in _m_record_tests.CASES if each.group == 'record-shared']
        self.assertEqual(len(crossing), 1)
        self.assertTrue(crossing[0].applies(store))
        self.assertFalse(crossing[0].owed)

    def test_declares_what_the_document_says(self) -> None:
        local = make_local().open()
        self.assertEqual(local.capabilities, frozenset({Capability.ATOMIC_BATCH, Capability.DURABLE, Capability.SHARED_BETWEEN_PROCESSES, Capability.FALLBACK, Capability.LEAVES_WORKING_TREE_UNTOUCHED}))
        self.assertIn(Capability.REPLICATED, make_replicated().open().capabilities)

def packs(project: Path) -> set[str]:
    return {each.name for each in (project / '.git' / 'objects' / 'pack').glob('*.pack')}

def loose_objects(project: Path) -> set[str]:
    folders = [each for each in (project / '.git' / 'objects').iterdir() if len(each.name) == 2]
    return {f'{folder.name}{each.name}' for folder in folders for each in folder.iterdir()}

def references(project: Path) -> list[str]:
    listed = subprocess.run(['git', '-C', str(project), 'for-each-ref', '--format=%(refname)'], capture_output=True, text=True, check=True)
    return listed.stdout.split()

class Medium(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_a_batch_writes_one_pack_and_no_other_reference(self) -> None:
        adapter = make_local()
        project = Path(adapter.repository)
        store = adapter.open()
        before, loose = (packs(project), loose_objects(project))
        self.assertEqual(store.batch([], [(address(store, i), value(store, i)) for i in range(50)]), Committed())
        self.assertEqual(len(packs(project) - before), 1)
        self.assertEqual(loose_objects(project), loose)
        self.assertEqual([each for each in references(project) if not each.startswith('refs/heads/')], ['refs/memar/work-records'])

    def test_a_stale_reference_lock_is_removed_and_a_fresh_one_waited_for(self) -> None:
        adapter = make_local()
        project = Path(adapter.repository)
        store = adapter.open()
        lock = project / '.git' / 'refs' / 'memar' / 'work-records.lock'
        lock.parent.mkdir(parents=True, exist_ok=True)
        lock.write_bytes(b'')
        old = time.time() - 60
        os.utime(lock, (old, old))
        self.assertEqual(store.batch([], [(address(store, 1), value(store, 1))]), Committed())
        self.assertFalse(lock.exists())
        lock.write_bytes(b'')
        threading.Timer(1.0, lock.unlink).start()
        started = time.monotonic()
        self.assertEqual(store.batch([], [(address(store, 2), value(store, 2))]), Committed())
        self.assertGreaterEqual(time.monotonic() - started, 0.9)

    def test_the_index_is_kept_in_the_data_area_and_nothing_in_the_working_tree(self) -> None:
        adapter = make_local()
        store = adapter.open()
        _m_conformance.write_in_batches(self, store, [(address(store, i), value(store, i)) for i in range(300)])
        self.assertTrue(any(Path(adapter.data_area).iterdir()))
        store.drop_derived_structures()
        self.assertFalse(any(Path(adapter.data_area).iterdir()))
        self.assertEqual(len(store.list()), 300)

class Binding(unittest.TestCase):

    def setUp(self) -> None:
        folder = _m_scratch.suite_scratch() / f'git-store-data-{uuid.uuid4().hex[:12]}'
        folder.mkdir()
        MADE.append((None, folder))
        self.saved = {name: os.environ.get(name) for name in ('LOCALAPPDATA', 'XDG_DATA_HOME')}
        os.environ['LOCALAPPDATA'] = os.environ['XDG_DATA_HOME'] = str(folder)

    def tearDown(self) -> None:
        for name, was in self.saved.items():
            if was is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = was
        clean_up()

    def project_with(self, block: str) -> Path:
        folder, project, data = scratch_project()
        MADE.append((None, folder))
        (project / 'manifest.yaml').write_text(block, encoding='utf-8')
        return project

    def test_the_reference_defaults_to_the_class_and_is_read_from_its_key(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=git-store, other=git-store\n  git-store-reference: other=refs/memar/elsewhere\n')
        one, two = (_m_git_store.bind(project, 'work-records'), _m_git_store.bind(project, 'other'))
        self.assertEqual((one.reference, two.reference), ('refs/memar/work-records', 'refs/memar/elsewhere'))
        self.assertNotEqual(one.store, two.store)
        self.assertEqual(one.store, _m_git_store.bind(project, 'work-records').store)
        self.assertNotIn(Capability.REPLICATED, one.open().capabilities)
        one.close()
        two.close()

    def test_shared_and_publish_are_read_from_their_keys(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=git-store\n  git-store-shared: work-records=../shared.git\n  git-store-publish: work-records=now\n')
        adapter = _m_git_store.bind(project, 'work-records')
        self.assertEqual((adapter.shared, adapter.publish), ('../shared.git', 'now'))
        self.assertIn(Capability.REPLICATED, adapter.open().capabilities)
        adapter.close()

    def test_a_class_whose_reference_is_a_folder_of_anothers_is_refused(self) -> None:
        project = self.project_with('memar:\n  memory: a=git-store, a/b=git-store\n')
        first = _m_git_store.bind(project, 'a')
        first.close()
        with self.assertRaises(errors_module().ReferenceCollision):
            _m_git_store.bind(project, 'a/b')

    def test_custom_references_that_collide_are_refused_and_siblings_are_not(self) -> None:
        project = self.project_with('memar:\n  memory: one=git-store, two=git-store, ab=git-store, a=git-store\n  git-store-reference: one=refs/memar/x, two=refs/memar/x/y\n')
        with self.assertRaises(errors_module().ReferenceCollision):
            _m_git_store.bind(project, 'two')
        for name in ('one', 'a', 'ab'):
            _m_git_store.bind(project, name).close()

    def test_a_key_in_the_private_namespace_or_of_a_broken_form_is_refused(self) -> None:
        errors = errors_module()
        project = self.project_with('memar:\n  memory: work-records=git-store\n  git-store-reference: work-records=refs/memar-local/published/x\n')
        with self.assertRaises(errors.BadReference):
            _m_git_store.bind(project, 'work-records')
        project = self.project_with('memar:\n  memory: work-records=git-store\n  git-store-publish: work-records=sometimes\n')
        with self.assertRaises(errors.BadParameter):
            _m_git_store.bind(project, 'work-records')
        project = self.project_with('memar:\n  memory: work-records=git-store\n  git-store-shared: work-records\n')
        with self.assertRaises(errors.BadParameter):
            _m_git_store.bind(project, 'work-records')

    def test_open_lays_record_over_the_bound_store(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=git-store\n')
        memory = import_module('bundles.memar.services.memory.memory')
        opened = memory.open(project, 'work-records', _m_record.Needs(capabilities=frozenset({Capability.ATOMIC_BATCH})))
        self.assertIsInstance(opened, _m_record.Record)
        node = bytes.fromhex('0190000000007000800000000000000a')
        self.assertEqual(opened.batch([], [(_m_record.key(node, 'alpha'), b'a')]), Committed())
        self.assertEqual(opened.parts([node])[0][0][0], 'alpha')
        opened.store.close()

def errors_module() -> Any:
    return import_module('modules-plugable.computer.memory.store.git-store.errors.errors')

def bare(path: str) -> tuple[list[int], list[int]]:
    source = Path(path).read_text(encoding='utf-8')
    comments = [t.start[0] for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT and t.start[0] > 2]
    documented = [getattr(n, 'lineno', 0) for n in ast.walk(ast.parse(source)) if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(n, clean=False) is not None]
    return (comments, documented)

def scratch_adapter(reference: str, **keywords: Any) -> Any:
    folder, project, data = scratch_project()
    adapter = _m_git_store.GitStoreAdapter(str(project), reference, data_area=str(data), **keywords)
    MADE.append((adapter, folder))
    return adapter

class Namespace(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_the_public_and_private_prefixes_are_the_adapters_own(self) -> None:
        self.assertEqual((_m_git_store.NAMESPACE, _m_git_store.PUBLISHED_NAMESPACE, _m_git_store.PENDING_BRANCH), ('refs/memar/', 'refs/memar-local/published/', 'refs/memar-local/pending/batch'))

    def test_the_published_reference_of_a_class_is_private_and_a_custom_one_falls_back(self) -> None:
        self.assertEqual(_m_git_store.published_reference('refs/memar/work-records'), 'refs/memar-local/published/work-records')
        self.assertEqual(_m_git_store.published_reference('refs/custom/notes'), 'refs/memar-local/published/custom/notes')

    def test_a_replicated_store_leaves_its_reference_and_the_acknowledged_one_only(self) -> None:
        adapter = make_replicated()
        store = adapter.open()
        self.assertEqual(store.batch([], [(address(store, 1), value(store, 1))]), Committed())
        self.assertTrue(_m_cases._settles(store, adapter))
        kept = sorted((each for each in references(Path(adapter.repository)) if not each.startswith('refs/heads/')))
        self.assertEqual(kept, ['refs/memar-local/published/work-records', 'refs/memar/work-records'])

    def test_a_reference_outside_the_public_namespace_keeps_working(self) -> None:
        adapter = scratch_adapter('refs/custom/notes')
        store = adapter.open()
        self.assertEqual(store.batch([], [(address(store, 1), value(store, 1))]), Committed())
        self.assertEqual([each for each in references(Path(adapter.repository)) if not each.startswith('refs/heads/')], ['refs/custom/notes'])

    def test_a_reference_the_adapter_may_not_keep_a_store_in_is_refused(self) -> None:
        bad = errors_module().BadReference
        folder, project, data = scratch_project()
        MADE.append((None, folder))
        for name in ('refs/memar-local/mine', 'refs/memar-local/published/x', 'refs/memar-local', 'heads/x', 'refs/a..b', 'refs/a/', 'refs/a.lock'):
            with self.subTest(name=name):
                with self.assertRaises(bad):
                    _m_git_store.GitStoreAdapter(str(project), name)

class ReferenceType(unittest.TestCase):

    def test_a_reference_names_itself_and_says_whether_it_is_public(self) -> None:
        Reference = _m_git_store.Reference
        public, custom = (Reference.named('refs/memar/work-records'), Reference.named('refs/custom/notes'))
        self.assertEqual((public.get_name(), public.is_public(), custom.is_public()), ('refs/memar/work-records', True, False))
        self.assertEqual(public, Reference.of_class('work-records'))

    def test_a_reference_is_a_folder_of_another_when_the_other_lies_under_it(self) -> None:
        Reference = _m_git_store.Reference
        a, ab, a_b = (Reference.of_class('a'), Reference.of_class('ab'), Reference.of_class('a/b'))
        self.assertTrue(a.is_folder_of(a_b))
        self.assertFalse(a_b.is_folder_of(a))
        self.assertFalse(a.is_folder_of(ab))
        self.assertFalse(a.is_folder_of(a))

    def test_a_class_that_makes_no_reference_is_refused(self) -> None:
        for name in ('', 'a..b', 'a/', 'a.lock'):
            with self.subTest(name=name):
                with self.assertRaises(errors_module().BadReference):
                    _m_git_store.Reference.of_class(name)

class Errors(unittest.TestCase):

    def tearDown(self) -> None:
        clean_up()

    def test_the_errors_are_in_the_errors_folder_and_say_what_they_are(self) -> None:
        errors = errors_module()
        raised = import_module('modules.computer.memory.store.errors.errors')
        for name in ('BadReference', 'ReferenceCollision', 'NotInRepository', 'BadParameter', 'Lost', 'NotFastForward'):
            with self.subTest(name=name):
                self.assertTrue(getattr(errors, name)().summary())
        self.assertEqual((errors.BadReference().reason, errors.ReferenceCollision().reason), (raised.Refusal.MALFORMED, raised.Refusal.MALFORMED))
        self.assertEqual(errors.Lost().reason, raised.Unavailability.FAILED)
        self.assertTrue(all((issubclass(getattr(errors, name), raised.Raised) for name in ('BadReference', 'ReferenceCollision', 'Lost'))))

    def test_the_realization_makes_no_error_type_of_its_own(self) -> None:
        for module in (_m_git_store, _m_cases):
            own = sorted((name for name, each in vars(module).items() if isinstance(each, type) and each.__module__ == module.__name__ and issubclass(each, BaseException)))
            self.assertEqual(own, [])
        self.assertFalse(hasattr(_m_git_store, '_Lost'))

    def test_a_project_outside_a_repository_raises_not_in_repository(self) -> None:
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as plain:
            adapter = _m_git_store.GitStoreAdapter(plain, 'refs/memar/work-records', data_area=str(Path(plain) / 'data'))
            with self.assertRaises(errors_module().NotInRepository):
                adapter.open()

    def test_a_lost_git_process_raises_lost_and_a_read_answers_failed(self) -> None:
        adapter = make_local()
        store = adapter.open()
        medium = adapter._medium_of()
        gone = types.SimpleNamespace(stdin=io.BytesIO(), stdout=io.BytesIO(), poll=lambda: None)
        medium._long_lived = lambda name, args, errors=None: gone
        with self.assertRaises(errors_module().Lost):
            medium.object_id('refs/memar/work-records')
        self.assertEqual(store.get([address(store, 1)]), [_m_store.Unavailable(_m_store.Unavailability.FAILED)])

    def test_an_unknown_publish_value_is_a_bad_parameter(self) -> None:
        folder, project, data = scratch_project()
        MADE.append((None, folder))
        with self.assertRaises(errors_module().BadParameter):
            _m_git_store.GitStoreAdapter(str(project), 'refs/memar/x', publish='sometimes')

class NoComments(unittest.TestCase):

    def test_the_files_carry_no_comment_and_no_docstring(self) -> None:
        here = Path(__file__).resolve().parent
        module = here.parent
        for path in (module / 'git-store.py', module / 'cases.py', module / 'services' / '_benchmark.py', module / 'errors' / 'errors.py', here / 'git-store.py', here / 'git-store-slow.py'):
            with self.subTest(path=path.name):
                self.assertEqual(bare(str(path)), ([], []))

def tearDownModule() -> None:
    clean_up()
if __name__ == '__main__':
    unittest.main()
