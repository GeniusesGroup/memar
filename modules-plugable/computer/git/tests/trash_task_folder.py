#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for closing a task in `modules-plugable/computer/git/services/close.py`.

    python modules-plugable/management/task/tests/close.py

The subject is `close`, named for the file that holds it per
[Test Naming](../../../../modules/process/test/rules/test-naming/test-naming.md),
in the `tests/` folder of the shelf that owns it per
[Test Placement](../../../../modules/process/test/rules/test-placement/test-placement.md).

Nothing here writes outside its scratch folder, and nothing reaches the
platform trash: the Memar root is patched onto a scratch folder and the trash
onto a stand-in inside it.

What is pinned, and what each pin is for:

  RecoverableClose  `close` hands the folder to recoverable storage instead of
                    destroying it, so a task closed by mistake costs one trip
                    to the trash; closing again says it is already closed; a
                    trash that fails leaves the folder where it was, because a
                    failed recovery is not a successful close. A task in a
                    recorded project location is closed there,
                    from any working folder, leaving the location itself; a
                    folder there that is not a task's is refused and
                    left, even in a location registered by hand that is a
                    project's top folder.
  OnlyItsFolder     Closing one task's folder reaches nothing beside it, the
                    lock directory included, and is recorded in the log of
                    the location it lay in: a project's own, else Memar's.
  RecordsMustBeArchived
                    `close` keeps nothing itself (owner, 2026-10-15): a folder
                    whose records are owed is closed only when they are on its
                    project's records branch as the folder holds them now, and
                    `close` says where; one not archived is not closed, and
                    `--discard-records` does not change that; one whose
                    records cannot be kept is not closed either, unless the
                    person says to close it without them. A project that keeps
                    no records owes none. A plan or report whose Status is
                    Queued is never closed.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_test_scratch = import_module('modules-plugable.computer.memory.filesystem.services.fs_test_scratch')
suite_scratch = _m_fs_test_scratch.suite_scratch
_m_fs_lock = import_module('modules-plugable.computer.memory.filesystem.services.fs_lock')
fs_lock = _m_fs_lock
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
memar_fs = _m_fs_memar
_m_fs_trash = import_module('modules-plugable.computer.memory.filesystem.services.fs_trash')
fs_trash = _m_fs_trash
import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path
TESTS = Path(__file__).resolve().parent
SCRIPTS = next(p for p in TESTS.parents if p.name == 'modules-plugable').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_archive = import_module('modules-plugable.computer.git.services.archive_task_records')
task_close = import_module('modules-plugable.computer.git.services.trash_task_folder')
from modules.process.project.services.registry import add_project
from modules.process.project.services.task_location import register
TASK_LOG_NAME = import_module('modules-plugable.computer.git.services.log').TASK_LOG_NAME
log_path = import_module('modules-plugable.computer.git.services.log').log_path

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        self.bin = self.fake_root / 'recycle-bin'
        self.bin.mkdir()

    def move_to_bin(self, source: Path) -> None:
        shutil.move(str(source), str(self.bin / Path(source).name))

    def task(self, sid: str) -> Path:
        path = memar_fs.task_dir(sid, create=True)
        (path / 'notes.md').write_text('# Keep me\n', encoding='utf-8', newline='\n')
        return path

class RecoverableClose(Fixture):

    def test_close_moves_the_folder_with_its_contents_to_recoverable_storage(self) -> None:
        path = self.task('s-recover')
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin) as trash:
            self.assertEqual(task_close.close_task('s-recover')[:3], ('s-recover', path, True))
            trash.assert_called_once_with(path)
            self.assertFalse(path.exists())
            self.assertEqual((self.bin / 's-recover' / 'notes.md').read_text(encoding='utf-8'), '# Keep me\n')
            self.assertEqual(task_close.close_task('s-recover')[:3], ('s-recover', path, False))
            trash.assert_called_once()

    def test_close_says_what_it_did(self) -> None:
        self.task('s-said')
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin):
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                task_close.close('s-said')
                task_close.close('s-said')
        self.assertIn('closed: s-said', out.getvalue())
        self.assertIn('already closed: s-said', out.getvalue())

    def test_failed_trash_leaves_the_folder_in_place(self) -> None:
        path = self.task('s-failed')
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=OSError('trash unavailable')):
            with self.assertRaises(OSError):
                task_close.close_task('s-failed')
        self.assertTrue(path.is_dir())

    def test_a_task_in_a_project_location_is_closed_where_it_is(self) -> None:
        location = self.fake_root / 'project' / 'tasks'
        folder = location / '20261009-T120000Z-43'
        folder.mkdir(parents=True)
        register(location)
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin) as trash:
            self.assertEqual(task_close.close_task(folder.name)[:3], (folder.name, folder, True))
        trash.assert_called_once_with(folder)
        self.assertTrue(location.is_dir())

    def test_a_named_task_in_a_project_location_is_closed_where_it_is(self) -> None:
        location = self.fake_root / 'project' / 'tasks'
        folder = location / 'my-task'
        folder.mkdir(parents=True)
        (folder / 'plan.md').write_text('---\nTitle: T\nStatus: Complete\nOpened: x\n---\n# T\n', encoding='utf-8', newline='\n')
        register(location)
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin) as trash:
            self.assertEqual(task_close.close_task('my-task')[:3], ('my-task', folder, True))
        trash.assert_called_once_with(folder)

    def test_a_folder_in_a_project_location_that_is_not_a_task_is_refused(self) -> None:
        project = self.fake_root / 'project'
        own = project / '.agents'
        own.mkdir(parents=True)
        (own / 'keep.md').write_text('# Keep\n', encoding='utf-8', newline='\n')
        register(project)
        with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
            with self.assertRaises(SystemExit) as raised:
                task_close.close_task('.agents')
        trash.assert_not_called()
        self.assertIn('is not a task folder', str(raised.exception.code))
        self.assertTrue((own / 'keep.md').is_file())

    def test_a_path_is_refused_as_an_id(self) -> None:
        for bad in ('a/b', '..', ''):
            with self.subTest(bad=bad):
                with self.assertRaises(SystemExit):
                    task_close.close_task(bad)

class OnlyItsFolder(Fixture):

    def test_closing_leaves_the_lock_root_alone_and_is_recorded(self) -> None:
        path = self.task('s-3')
        lock_dir = memar_fs.scratch_root() / fs_lock.EDIT_LOCK_DIR_NAME
        lock_dir.mkdir()
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin) as trash:
            task_close.close_task('s-3')
        trash.assert_called_once_with(path)
        self.assertTrue(lock_dir.is_dir())
        events = [line.split('\t')[1:3] for line in log_path().read_text(encoding='utf-8').splitlines()]
        self.assertIn(['closed', 's-3'], events)

    def test_closing_a_task_in_a_project_location_is_recorded_in_that_locations_log(self) -> None:
        location = self.fake_root / 'project' / 'tasks'
        folder = location / '20261009-T120000Z-44'
        folder.mkdir(parents=True)
        register(location)
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin):
            task_close.close_task(folder.name)
        events = [line.split('\t')[1:3] for line in (location / TASK_LOG_NAME).read_text(encoding='utf-8').splitlines()]
        self.assertEqual(events, [['closed', folder.name]])
        self.assertFalse(log_path().is_file())

class RecordsMustBeArchived(Fixture):

    def project_repository(self) -> Path:
        project = self.fake_root / 'work' / 'example'
        project.mkdir(parents=True)
        for args in (['init', '-q', '-b', 'main'], ['config', 'user.name', 'Test'], ['config', 'user.email', 't@example.org']):
            subprocess.run(['git', '-C', str(project), *args], check=True, capture_output=True)
        add_project('example', project)
        return project

    def finished(self, sid: str, project: Path, *, status: str='Complete', report_status: str | None=None) -> Path:
        path = memar_fs.task_dir(sid, create=True)
        (path / 'plan.md').write_text(f'---\nTitle: T\nStatus: {status}\nOpened: x\nProject: {project}\n---\n# T\n', encoding='utf-8', newline='\n')
        if report_status is not None:
            (path / 'report.md').write_text(f'---\nTitle: T\nStatus: {report_status}\n---\n# Report\n', encoding='utf-8', newline='\n')
        return path

    def archive(self, path: Path) -> None:
        self.assertEqual(task_archive.keep_records([path])[0].outcome, task_archive.Outcome.KEPT)

    def test_an_archived_task_is_closed_and_close_says_where_its_records_are(self) -> None:
        project = self.project_repository()
        path = self.finished('s-kept', project)
        self.archive(path)
        out = io.StringIO()
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin), contextlib.redirect_stdout(out):
            task_close.close('s-kept')
        self.assertFalse(path.exists())
        self.assertIn(f"records: {task_archive.reference('s-kept')}", out.getvalue())

    def test_a_task_not_archived_is_not_closed_and_close_keeps_nothing_itself(self) -> None:
        project = self.project_repository()
        path = self.finished('s-waiting', project)
        with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
            with self.assertRaises(SystemExit) as raised:
                task_close.close_task('s-waiting')
        trash.assert_not_called()
        self.assertTrue(path.is_dir())
        said = str(raised.exception.code)
        self.assertIn('not closed', said)
        self.assertIn('not archived', said)
        self.assertIn('memar git archive-task-records --task-id s-waiting', said)
        branches = subprocess.run(['git', '-C', str(project), 'branch', '--list'], capture_output=True, text=True).stdout
        self.assertEqual(branches.strip(), '')

    def test_a_change_after_archiving_makes_it_not_archived_again(self) -> None:
        path = self.finished('s-changed', self.project_repository())
        self.archive(path)
        (path / 'report.md').write_text('---\nTitle: T\nStatus: Complete\n---\n# Report\nLater.\n', encoding='utf-8', newline='\n')
        with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
            with self.assertRaises(SystemExit):
                task_close.close_task('s-changed')
        trash.assert_not_called()

    def test_discard_records_does_not_close_a_task_that_is_only_not_archived(self) -> None:
        path = self.finished('s-waiting-too', self.project_repository())
        with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
            with self.assertRaises(SystemExit):
                task_close.close_task('s-waiting-too', discard_records=True)
        trash.assert_not_called()
        self.assertTrue(path.is_dir())

    def test_a_task_whose_project_keeps_no_records_is_closed(self) -> None:
        project = self.project_repository()
        (project / 'manifest.yaml').write_text('memar:\n  records: off\n', encoding='utf-8', newline='\n')
        path = self.finished('s-off', project)
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin):
            self.assertTrue(task_close.close_task('s-off').removed)
        self.assertFalse(path.exists())

    def test_a_folder_whose_records_cannot_be_kept_is_not_closed(self) -> None:
        path = self.finished('s-stuck', self.fake_root / 'elsewhere')
        with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
            with self.assertRaises(SystemExit) as raised:
                task_close.close_task('s-stuck')
        trash.assert_not_called()
        self.assertTrue(path.is_dir())
        self.assertIn('not closed', str(raised.exception.code))

    def test_the_person_may_close_it_without_its_records_when_they_cannot_be_kept(self) -> None:
        path = self.finished('s-dropped', self.fake_root / 'elsewhere')
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=self.move_to_bin):
            closed = task_close.close_task('s-dropped', discard_records=True)
        self.assertTrue(closed.removed)
        self.assertFalse(path.exists())

    def test_a_queued_plan_or_report_is_never_closed(self) -> None:
        project = self.project_repository()
        for sid, status, report_status in (('s-queued-plan', 'Queued', None), ('s-queued-report', 'Complete', 'Queued')):
            with self.subTest(sid=sid):
                path = self.finished(sid, project, status=status, report_status=report_status)
                for without in (False, True):
                    with unittest.mock.patch.object(fs_trash, 'soft_delete') as trash:
                        with self.assertRaises(SystemExit) as raised:
                            task_close.close_task(sid, discard_records=without)
                    trash.assert_not_called()
                    self.assertIn('Queued', str(raised.exception.code))
                self.assertTrue(path.is_dir())
if __name__ == '__main__':
    unittest.main(verbosity=2)
