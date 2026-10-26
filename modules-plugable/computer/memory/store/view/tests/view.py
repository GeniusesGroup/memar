#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests that the builder of `view.py` builds the view [Memory View](../view.md) states, over `volatile` and over `git-store`.

    python modules-plugable/computer/memory/store/view/tests/view.py

The subject is `view.py`, named for the file that holds it per
[Test Naming](../../../../../../modules/process/test/rules/test-naming/test-naming.md), in the `tests/` folder of the
module that owns it per [Test Placement](../../../../../../modules/process/test/rules/test-placement/test-placement.md).
Each case of the document is a test of `Cases`, named by the case, and runs twice: `OverVolatile` builds over `record`
laid over `volatile`, `OverGitStore` over `record` laid over `git-store` on a scratch repository. The presentation is
the test's own (`present`): a node's folder is its id in hexadecimal, and each part is a file named by its domain key.
Every view is built in a folder of a scratch repository that ignores `view/`, and every scratch folder is made under
the suite's scratch folder (`fs_test_scratch`) and removed whole after its test.
"""
from __future__ import annotations
import os
import stat
import subprocess
import sys
import time
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
_m_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
_m_volatile = import_module('modules.computer.memory.volatile.volatile')
_m_record = import_module('modules-plugable.computer.memory.store.record.record')
_m_git_store = import_module('modules-plugable.computer.memory.store.git-store.git-store')
_m_view = import_module('modules-plugable.computer.memory.store.view.view')
Committed = import_module('modules.computer.memory.store.protocol.store').Committed
VIEW = 'view'

def node_id(i: int) -> bytes:
    """The id of the I-th node of a test: a UUID version 7 of a fixed instant."""
    return bytes.fromhex(f'019000000000700080000000{i:08x}')

def present(node: Any) -> dict[str, bytes]:
    """The test presentation: one folder per node, named by its id, holding one file per part, named by its domain key."""
    return {f'{node.id.hex()}/{domain_key}.txt': value for domain_key, value in node.parts.items()}

def git(where: Path, *args: str) -> str:
    done = subprocess.run(['git', '-C', str(where), '-c', 'user.name=suite', '-c', 'user.email=suite@example.invalid', *args], check=True, capture_output=True, text=True)
    return done.stdout

def scratch_repository(ignored: bool=True) -> Path:
    """A new scratch folder that is a repository with one commit, ignoring `view/` when IGNORED."""
    folder = _m_scratch.suite_scratch() / f'view-{uuid.uuid4().hex[:12]}'
    folder.mkdir(parents=True)
    git(folder, 'init', '-q')
    (folder / '.gitignore').write_bytes(b'view/\nother-view/\n' if ignored else b'other/\n')
    git(folder, 'add', '.gitignore')
    git(folder, 'commit', '-q', '-m', 'scratch')
    return folder

def files(folder: Path) -> dict[str, tuple[bytes, int]]:
    """Every file under FOLDER, by its path relative to it, with its bytes and its modification time."""
    if not folder.exists():
        return {}
    return {each.relative_to(folder).as_posix(): (each.read_bytes(), each.stat().st_mtime_ns) for each in folder.rglob('*') if each.is_file()}

def write(record: Any, i: int, **parts: bytes) -> None:
    answer = record.batch([], [(_m_record.key(node_id(i), name), value) for name, value in parts.items()])
    assert answer == Committed(), answer

class Cases:
    """The cases of [Memory View → The cases](../view.md#the-cases); `make()` gives a `record` and its scratch repository."""

    def setUp(self) -> None:
        self.made: list[Path] = []
        self.closing: list[Any] = []

    def tearDown(self) -> None:
        for each in self.closing:
            each.close()
        for folder in self.made:
            _m_scratch.remove_tree(folder)

    def make(self, ignored: bool=True) -> tuple[Any, Path]:
        raise NotImplementedError

    def three_nodes(self) -> tuple[Any, Path]:
        record, folder = self.make()
        write(record, 1, alpha=b'one alpha\n', beta=b'one beta\n')
        write(record, 2, alpha=b'two alpha\n')
        write(record, 3, gamma=b'three gamma\n')
        return (record, folder / VIEW)

    def build(self, record: Any, folder: Path) -> Any:
        return _m_view.build(record, present, folder)

    def test_view_is_deterministic(self) -> None:
        """view-is-deterministic: two builds with no change in between leave every file's bytes and modification time as they were."""
        record, folder = self.three_nodes()
        first = self.build(record, folder)
        self.assertIsInstance(first, _m_view.Built)
        self.assertEqual(first.written, 4)
        before = files(folder)
        time.sleep(0.05)
        second = self.build(record, folder)
        self.assertEqual((second.written, second.removed, second.drift, second.unchanged), (0, 0, 0, 4))
        self.assertEqual(files(folder), before)

    def test_view_rebuild_identical(self) -> None:
        """view-rebuild-identical: a build after the folder is deleted gives the same set of paths and bytes."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        before = {path: data for path, (data, _) in files(folder).items()}
        _m_scratch.remove_tree(folder)
        self.assertIsInstance(self.build(record, folder), _m_view.Built)
        self.assertEqual({path: data for path, (data, _) in files(folder).items()}, before)

    def test_view_changed_node_rewrites_only_its_files(self) -> None:
        """view-changed-node-rewrites-only-its-files: after one node changes, exactly the files that show it are rewritten.
        The builder's own list of the files it wrote shows no node, and is left out of the comparison."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        before = files(folder)
        time.sleep(0.05)
        write(record, 2, alpha=b'two alpha changed\n', delta=b'two delta\n')
        built = self.build(record, folder)
        after = files(folder)
        touched = {path for path in set(before) | set(after) if before.get(path) != after.get(path)} - {_m_view.LIST_NAME}
        shown = {path for path in present(_m_view.Node(node_id(2), {'alpha': b'', 'delta': b''}))}
        self.assertEqual(touched, shown)
        self.assertEqual((built.written, built.removed, built.drift), (2, 0, 0))

    def test_view_refuses_unignored_folder(self) -> None:
        """view-refuses-unignored-folder: in a working tree under version control, a folder that version control does not
        ignore is refused and nothing is written."""
        record, repository = self.make(ignored=False)
        write(record, 1, alpha=b'one\n')
        refused = self.build(record, repository / VIEW)
        self.assertIsInstance(refused, _m_view.ViewRefused)
        self.assertEqual(refused.reason, _m_view.ViewRefusal.UNIGNORED_FOLDER)
        self.assertFalse((repository / VIEW).exists())
        self.assertEqual(git(repository, 'status', '--porcelain'), '')

    def test_view_files_read_only(self) -> None:
        """view-files-read-only: every file the builder wrote carries the operating system's read-only attribute."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        written = [each for each in folder.rglob('*') if each.is_file()]
        self.assertEqual(len(written), 5)
        for each in written:
            with self.subTest(path=each.name):
                self.assertFalse(each.stat().st_mode & stat.S_IWRITE)

    def test_view_drift_is_rewritten_and_counted(self) -> None:
        """view-drift-is-rewritten-and-counted: a file changed by hand is restored by the next build, which reports one drift."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        changed = folder / node_id(1).hex() / 'alpha.txt'
        was = changed.read_bytes()
        os.chmod(changed, stat.S_IWRITE | stat.S_IREAD)
        changed.write_bytes(b'edited by hand\n')
        built = self.build(record, folder)
        self.assertEqual((built.drift, built.written), (1, 1))
        self.assertEqual(changed.read_bytes(), was)
        self.assertFalse(changed.stat().st_mode & stat.S_IWRITE)

    def test_view_refuses_foreign_files(self) -> None:
        """view-refuses-foreign-files: a folder holding a file the builder did not write is refused and nothing is written
        or removed."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        foreign = folder / 'notes.txt'
        foreign.write_bytes(b'mine\n')
        write(record, 3, gamma=b'three gamma changed\n')
        before = files(folder)
        refused = self.build(record, folder)
        self.assertIsInstance(refused, _m_view.ViewRefused)
        self.assertEqual(refused.reason, _m_view.ViewRefusal.FOREIGN_FILES)
        self.assertEqual(files(folder), before)
        fresh = folder.parent / 'other-view'
        fresh.mkdir()
        (fresh / 'kept.txt').write_bytes(b'kept\n')
        self.assertEqual(self.build(record, fresh).reason, _m_view.ViewRefusal.FOREIGN_FILES)
        self.assertEqual(sorted((each.name for each in fresh.iterdir())), ['kept.txt'])

    def test_view_removes_the_files_of_a_node_no_longer_shown(self) -> None:
        """A path the presentation no longer gives is removed with the folders it leaves empty: the view is a function of
        the state, and a file it once wrote is the builder's to take away."""
        record, folder = self.three_nodes()
        self.build(record, folder)
        shown = {'alpha'}
        built = _m_view.build(record, lambda node: {path: data for path, data in present(node).items() if path.split('/')[1][:-4] in shown}, folder)
        self.assertEqual((built.written, built.removed), (0, 2))
        self.assertFalse((folder / node_id(3).hex()).exists())

    def test_view_refuses_a_path_outside_the_folder(self) -> None:
        """A presentation that gives a path leaving the folder, or one path for two nodes, is refused and nothing is written."""
        record, folder = self.three_nodes()
        for wrong in (lambda node: {'../outside.txt': b'x'}, lambda node: {'same.txt': node.id}):
            with self.subTest():
                refused = _m_view.build(record, wrong, folder)
                self.assertIsInstance(refused, _m_view.ViewRefused)
                self.assertEqual(refused.reason, _m_view.ViewRefusal.MALFORMED_PATH)
                self.assertFalse(folder.exists())

class OverVolatile(Cases, unittest.TestCase):

    def make(self, ignored: bool=True) -> tuple[Any, Path]:
        repository = scratch_repository(ignored)
        self.made.append(repository)
        return (_m_record.Record(_m_volatile.Volatile()), repository)

class OverGitStore(Cases, unittest.TestCase):

    def make(self, ignored: bool=True) -> tuple[Any, Path]:
        repository = scratch_repository(ignored)
        self.made.append(repository)
        data = repository.parent / f'{repository.name}-data'
        data.mkdir()
        self.made.append(data)
        adapter = _m_git_store.GitStoreAdapter(str(repository), 'refs/memory/notes', data_area=str(data))
        self.closing.append(adapter)
        return (_m_record.RecordAdapter(adapter).open(), repository)

class Preference(unittest.TestCase):
    """The key `view` is this module's, read in the form the preferences module declares once; a project defines at most one view."""

    def setUp(self) -> None:
        self.folder = _m_scratch.suite_scratch() / f'view-preference-{uuid.uuid4().hex[:12]}'
        self.folder.mkdir()

    def tearDown(self) -> None:
        _m_scratch.remove_tree(self.folder)

    def with_block(self, block: str) -> Path:
        (self.folder / 'manifest.yaml').write_text(block, encoding='utf-8')
        return self.folder

    def test_the_key_names_one_class_and_its_folder(self) -> None:
        self.assertEqual(_m_view.VIEW_KEY, 'view')
        self.assertEqual(_m_view.view_preference(self.with_block('memar:\n  view: work-records=.agents/view\n')), {'work-records': '.agents/view'})
        self.assertEqual(_m_view.view_preference(self.with_block('memar:\n  tasks: work\n')), {})

    def test_two_views_or_a_broken_form_is_none(self) -> None:
        self.assertIsNone(_m_view.view_preference(self.with_block('memar:\n  view: one=a, two=b\n')))
        self.assertIsNone(_m_view.view_preference(self.with_block('memar:\n  view: one\n')))

    def test_a_presentation_is_registered_for_a_class(self) -> None:
        name = f'test-{uuid.uuid4().hex[:8]}'
        self.assertIsNone(_m_view.presentation(name))
        _m_view.register(name, present)
        self.assertIs(_m_view.presentation(name), present)

class NeverReadByVerbs(unittest.TestCase):
    """view-never-read-by-verbs: a scan of the verbs' source finds no read of the view's folder.

    The folder is reached only through the key `view` (`view_preference`, or the key's name read by the preferences
    module's reader) and is known by the list the builder keeps in it; a source that names neither cannot find it. So
    every Python file under `modules/`, `modules-plugable/` and `bundles/` is scanned for those names, outside this module
    and the verb that builds the view. A read through a path typed by hand is beyond what a scan of names can see."""

    def test_no_verb_names_the_views_folder(self) -> None:
        builder = TOP / 'modules-plugable' / 'computer' / 'memory' / 'store' / 'view'
        verb = TOP / 'bundles' / 'memar' / 'services' / 'view'
        names = ('view_preference', 'VIEW_KEY', _m_view.LIST_NAME, "preference(project, 'view')", 'preference(project, "view")')
        found = []
        for root in ('modules', 'modules-plugable', 'bundles'):
            for each in (TOP / root).rglob('*.py'):
                if builder in each.parents or verb in each.parents:
                    continue
                text = each.read_text(encoding='utf-8', errors='replace')
                found.extend((f'{each.relative_to(TOP).as_posix()}: {name}' for name in names if name in text))
        self.assertEqual(found, [])
if __name__ == '__main__':
    unittest.main()
