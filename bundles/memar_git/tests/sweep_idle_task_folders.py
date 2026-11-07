#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for daily flush/verify of the records branch (former complete-status sweep).

Complete-status trash is retired; this suite pins flush of materialized folders
and the once-a-day guard.
"""
from __future__ import annotations
from importlib import import_module
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
suite_scratch = _m_test_scratch.suite_scratch
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
memar_fs = _m_memar_location
_m_fs_trash = import_module('bundles.memar_fs.services.fs_trash')
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
SCRIPTS = next(p for p in TESTS.parents if p.name == 'bundles').parent / 'bundles' / 'memar'
sys.path.insert(0, str(SCRIPTS))
sys.path.insert(1, str(SCRIPTS.parent.parent))
sys.dont_write_bytecode = True
task_gc = import_module('bundles.memar_git.services.sweep_idle_task_folders')
task_store = import_module('bundles.memar_git.services.task_store')
TASK_LOG_NAME = import_module('bundles.memar_git.services.log').TASK_LOG_NAME
log_path = import_module('bundles.memar_git.services.log').log_path
task_files = import_module('modules-plugable.management.task.services.task_files')
timeline_files = import_module('modules.management.timeline.services.timeline_files')
SID = '20261001-T000000Z-1111'

class Fixture(unittest.TestCase):

    def setUp(self) -> None:
        self.scratch = tempfile.TemporaryDirectory(dir=suite_scratch())
        self.addCleanup(self.scratch.cleanup)
        self.fake_root = Path(self.scratch.name)
        patched = unittest.mock.patch.object(memar_fs, 'memar_root', return_value=self.fake_root)
        patched.start()
        self.addCleanup(patched.stop)
        for args in (['init', '-q', '-b', 'main'], ['config', 'user.name', 'Test'], ['config', 'user.email', 't@example.org']):
            subprocess.run(['git', '-C', str(self.fake_root), *args], check=True, capture_output=True)
        (self.fake_root / 'README').write_text('x\n', encoding='utf-8')
        subprocess.run(['git', '-C', str(self.fake_root), 'add', 'README'], check=True, capture_output=True)
        subprocess.run(['git', '-C', str(self.fake_root), 'commit', '-qm', 'init'], check=True, capture_output=True)

    def materialize(self, sid: str=SID) -> Path:
        folder = memar_fs.task_dir(sid, create=True)
        task_files.create_task(folder, sid, 'T', None, None, self.fake_root, 'active', None, None)
        timeline_files.add_text(folder, 'plan', '# T\n\n## Request\nWork.\n', 'agent')
        timeline_files.add_text(folder, 'report', '# Report\nDone.\n', 'agent')
        return folder

class DailyFlush(Fixture):

    def test_flush_records_writes_materialization_onto_the_branch(self) -> None:
        self.materialize()
        swept = task_gc.flush_records()
        self.assertIn(SID, swept.flushed)
        self.assertTrue(swept.tip)
        held = import_module('bundles.memar_git.services.branch').held(self.fake_root, SID)
        self.assertIn(task_files.TASK_FACTS_NAME, held)

    def test_gc_prints_flushed_and_tip(self) -> None:
        self.materialize()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            task_gc.collect(None, None)
        said = out.getvalue()
        self.assertIn(f'flushed to {memar_fs.RECORDS_BRANCH}: {SID}', said)
        self.assertIn('tip:', said)

    def test_own_task_is_skipped(self) -> None:
        self.materialize()
        swept = task_gc.flush_records(keep=SID)
        self.assertEqual(swept.flushed, [])

    def test_once_a_day_runs_only_first_call(self) -> None:
        self.materialize()
        marker = memar_fs.tasks_root() / task_gc.SWEPT_MARKER_NAME
        marker.unlink(missing_ok=True)
        task_gc.reap_once_a_day(keep='other')
        tip_after = task_store.verify_tip(self.fake_root)
        self.materialize('20261002-T000000Z-2222')
        task_gc.reap_once_a_day(keep='other')
        self.assertEqual(task_store.verify_tip(self.fake_root), tip_after)

class LogTrimmed(Fixture):

    def test_old_log_lines_are_moved_aside(self) -> None:
        log = log_path()
        log.parent.mkdir(parents=True, exist_ok=True)
        log.write_text('2000-01-01T00:00:00+00:00\told\n2099-10-01T00:00:00+00:00\tnew\n', encoding='utf-8')
        trashed: list[Path] = []

        def move_aside(path: Path) -> None:
            trashed.append(Path(path))
            if Path(path).is_file():
                Path(path).unlink(missing_ok=True)
        with unittest.mock.patch.object(fs_trash, 'soft_delete', side_effect=move_aside):
            task_gc.trim_log()
        text = log.read_text(encoding='utf-8') if log.is_file() else ''
        self.assertNotIn('\told\n', text.replace('\r\n', '\n'))
        self.assertIn('new', text)

if __name__ == '__main__':
    unittest.main(verbosity=2)
