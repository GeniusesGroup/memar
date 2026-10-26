#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that `git-store` keeps the store contract, the groups it declares, and `record`'s group laid over it.

    python modules-plugable/computer/memory/store/git-store/tests/git-store.py

The subject is `git-store.py`, named for the file that holds it per
[Test Naming](../../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the
module that owns it per [Test Placement](../../../../../../modules/process/test/rules/test-placement/test-placement.md).
Its expectations are [Memory Git Store](../git-store.md) and the cases of
[Memory Conformance](../../../../../../modules/computer/memory/conformance/conformance.md), run through the suite's
runner with the groups of [`cases.py`](../cases.py), `lockable`'s, and `record`'s group:

  Local          the kernel suite (core, model, durable, shared) and the fallback, working-tree and lockable groups,
                 on a scratch repository whose working tree has a tracked and an ignored file.
  Replicated     the replicated group, with a scratch bare repository as the shared store.
  LocalRecord    `record`'s group on `record` laid over the store, its cross-process case included.
  Medium         what the document says of the medium: one pack per batch, no reference but the class's and the
                 acknowledged one, a stale `<reference>.lock` removed and a fresh one waited for.
  Binding        `bind` reads the adapter's keys, and `open` lays `record` over the bound store.

Every scratch folder is made under the suite's scratch folder (`fs_test_scratch`) and removed whole after its test.
"""
from __future__ import annotations
import os
import subprocess
import sys
import threading
import time
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
MADE: list[tuple[Any, Path]] = []

def _git(where: Path, *args: str) -> None:
    subprocess.run(['git', '-C', str(where), '-c', 'user.name=suite', '-c', 'user.email=suite@example.invalid', *args], check=True, capture_output=True)

def scratch_project() -> tuple[Path, Path, Path]:
    """A new scratch folder holding a project repository with a tracked and an ignored file, and a data area."""
    folder = _m_scratch.suite_scratch() / f'git-store-{uuid.uuid4().hex[:12]}'
    project, data = (folder / 'project', folder / 'data')
    project.mkdir(parents=True)
    data.mkdir()
    _git(project, 'init', '-q')
    (project / 'tracked.txt').write_bytes(b'tracked\n')
    (project / '.gitignore').write_bytes(b'ignored.txt\n')
    (project / 'ignored.txt').write_bytes(b'ignored\n')
    _git(project, 'add', 'tracked.txt', '.gitignore')
    _git(project, 'commit', '-q', '-m', 'scratch')
    return (folder, project, data)

def make_local(**keywords: Any) -> Any:
    folder, project, data = scratch_project()
    adapter = _m_git_store.GitStoreAdapter(str(project), 'refs/memory/work-records', data_area=str(data), **keywords)
    MADE.append((adapter, folder))
    return adapter

def make_replicated() -> Any:
    folder, project, data = scratch_project()
    shared = folder / 'shared.git'
    subprocess.run(['git', 'init', '-q', '--bare', str(shared)], check=True, capture_output=True)
    adapter = _m_git_store.GitStoreAdapter(str(project), 'refs/memory/work-records', data_area=str(data), shared=str(shared))
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
    """A TestCase class holding only the tests of BASE that NAMES names, each with its scratch removed after it."""
    attributes: dict[str, Any] = {'tearDown': lambda self: clean_up()}
    attributes.update({each: getattr(base, each) for each in dir(base) if each in names})
    return type(name, (unittest.TestCase,), attributes)
_local = _m_conformance.test_case(make_local, _m_cases.CASES + _m_lockable.CASES)
Local = type('Local', (_local,), {'tearDown': lambda self: clean_up()})
_replicated = _m_conformance.test_case(make_replicated, _m_cases.REPLICATED_CASES)
Replicated = _only(_replicated, {'test_' + each.check.__name__ for each in _m_cases.REPLICATED_CASES}, 'Replicated')
_record = _m_record_tests.group(lambda: _m_record.RecordAdapter(make_local()), _m_record_tests.CASES)
LocalRecord = type('LocalRecord', (_record,), {'tearDown': lambda self: clean_up()})
del _local, _replicated, _record

class EveryOwedCaseRuns(unittest.TestCase):
    """The cases that waited for this store, the `durable` and `shared` groups and `record`'s cross-process case, apply
    to it, so they run here, and none still carries the owed mark."""

    def tearDown(self) -> None:
        clean_up()

    def test_the_durable_and_shared_groups_apply(self) -> None:
        store = make_local().open()
        waited = {each.name for each in _m_conformance.CASES if each.group in ('durable', 'shared')}
        self.assertEqual(len(waited), 8)
        self.assertEqual(waited - _m_conformance.applied(store), set())
        self.assertEqual([each.name for each in _m_conformance.CASES if OWED in (each.check.__doc__ or '')], [])

    def test_records_cross_process_case_applies(self) -> None:
        store = _m_record.RecordAdapter(make_local()).open()
        crossing = [each for each in _m_record_tests.CASES if each.group == 'record-shared']
        self.assertEqual(len(crossing), 1)
        self.assertTrue(crossing[0].applies(store))
        self.assertNotIn(OWED, crossing[0].check.__doc__)

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
    """What [Memory Git Store](../git-store.md) says of the medium, beyond the contract."""

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
        self.assertEqual([each for each in references(project) if not each.startswith('refs/heads/')], ['refs/memory/work-records'])

    def test_a_stale_reference_lock_is_removed_and_a_fresh_one_waited_for(self) -> None:
        adapter = make_local()
        project = Path(adapter.repository)
        store = adapter.open()
        lock = project / '.git' / 'refs' / 'memory' / 'work-records.lock'
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
    """`bind(project, class_name)` reads the adapter's own keys, and `open` lays `record` over the store it names. The
    user's data area is pointed into the scratch folder, so that nothing is saved outside it."""

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
        project = self.project_with('memar:\n  memory: work-records=git-store, other=git-store\n  git-store-reference: other=refs/memory/elsewhere\n')
        one, two = (_m_git_store.bind(project, 'work-records'), _m_git_store.bind(project, 'other'))
        self.assertEqual((one.reference, two.reference), ('refs/memory/work-records', 'refs/memory/elsewhere'))
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

    def test_open_lays_record_over_the_bound_store(self) -> None:
        project = self.project_with('memar:\n  memory: work-records=git-store\n')
        memory = import_module('bundles.memar.services.memory.memory')
        opened = memory.open(project, 'work-records', _m_record.Needs(capabilities=frozenset({Capability.ATOMIC_BATCH})))
        self.assertIsInstance(opened, _m_record.Record)
        node = bytes.fromhex('0190000000007000800000000000000a')
        self.assertEqual(opened.batch([], [(_m_record.key(node, 'alpha'), b'a')]), Committed())
        self.assertEqual(opened.parts([node])[0][0][0], 'alpha')
        opened.store.close()

def tearDownModule() -> None:
    clean_up()
if __name__ == '__main__':
    unittest.main()
