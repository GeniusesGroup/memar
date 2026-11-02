#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchRepository, bundle, errors

class TheRepositoryIsTheOneNamed(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.run_module = bundle('services._run')
        self.errors = errors()

    def test_the_root_is_the_top_of_the_repository_a_folder_in_it_names(self) -> None:
        (self.repo / 'deep').mkdir()
        self.assertEqual(self.run_module.repository_root(self.repo / 'deep'), self.repo.resolve())

    def test_a_place_that_is_not_a_folder_is_not_a_repository(self) -> None:
        with self.assertRaises(self.errors.NotARepository):
            self.run_module.repository_root(self.repo / 'no-such-folder')

    def test_a_folder_outside_any_repository_is_not_a_repository(self) -> None:
        import tempfile
        from _scratch import suite_scratch
        with tempfile.TemporaryDirectory(dir=suite_scratch(), ignore_cleanup_errors=True) as plain:
            if subprocess.run(['git', '-C', plain, 'rev-parse'], capture_output=True, timeout=60).returncode == 0:
                self.skipTest('the scratch folder lies inside a repository')
            with self.assertRaises(self.errors.NotARepository):
                self.run_module.repository_root(Path(plain))

    def test_a_missing_git_is_git_not_installed(self) -> None:
        with unittest.mock.patch.object(self.run_module.shutil, 'which', return_value=None):
            with self.assertRaises(self.errors.GitNotInstalled):
                self.run_module.repository_root(self.repo)

    def test_a_path_is_given_as_git_names_it_from_the_top(self) -> None:
        self.assertEqual(self.run_module.in_repo(Path('mine.md'), self.repo.resolve()), 'mine.md')
        self.assertEqual(self.run_module.in_repo(self.repo.resolve() / 'mine.md', self.repo.resolve()), 'mine.md')

    def test_a_path_outside_the_repository_is_not_named(self) -> None:
        with self.assertRaises(self.errors.NotNamed):
            self.run_module.in_repo(self.elsewhere / 'other.md', self.repo.resolve())

    def test_a_failing_git_step_is_a_git_failure_carrying_what_git_said(self) -> None:
        with self.assertRaises(self.errors.GitFailed) as raised:
            self.run_module.plumb(['rev-parse', '--verify', 'no-such-revision^{commit}'], self.repo.resolve())
        self.assertIn('rev-parse', str(raised.exception))

    def test_a_revision_that_is_not_there_is_not_a_success(self) -> None:
        with self.assertRaises(self.errors.Error):
            self.run_module.plumb(['cat-file', '-p', '0' * 40], self.repo.resolve())

class TheLocksAreWaitedForUnderOneDeadline(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.lock_module = bundle('services._lock')
        self.errors = errors()
        self.lock = self.repo / '.git' / 'index.lock'
        self.addCleanup(lambda: self.lock.exists() and self.lock.unlink())

    def test_the_shared_locks_are_those_of_the_index_the_head_and_the_branch(self) -> None:
        names = {path.name for path in self.lock_module.shared_locks(self.repo.resolve())}
        self.assertIn('index.lock', names)
        self.assertIn('HEAD.lock', names)
        self.assertIn('main.lock', names)

    def test_free_locks_answer_none_at_once(self) -> None:
        deadline = self.lock_module.lock_deadline()
        self.assertIsNone(self.lock_module.locks_free(self.lock_module.shared_locks(self.repo.resolve()), 'moving HEAD', deadline))

    def test_a_lock_still_held_past_the_deadline_is_answered_and_never_removed(self) -> None:
        self.lock.write_text('', encoding='utf-8')
        with unittest.mock.patch.object(self.lock_module, 'LOCK_WAIT_SECONDS', 0.3), unittest.mock.patch.object(self.lock_module, 'LOCK_FIRST_PAUSE_SECONDS', 0.05):
            held = self.lock_module.locks_free([self.lock], 'moving HEAD', self.lock_module.lock_deadline())
        self.assertEqual(held, self.lock)
        self.assertTrue(self.lock.exists())

    def test_stopping_is_the_locked_error_with_the_stage_the_lock_and_what_to_do(self) -> None:
        self.lock.write_text('', encoding='utf-8')
        with self.assertRaises(self.errors.Locked) as raised:
            self.lock_module.stopped('the commit object was written, but HEAD was not moved.', 'Nothing to undo. Once the lock is free, rerun the same command.', lock=self.lock)
        said = str(raised.exception)
        self.assertIn('HEAD was not moved', said)
        self.assertIn(str(self.lock), said)
        self.assertIn('rerun the same command', said)
        self.assertTrue(self.lock.exists())

if __name__ == '__main__':
    unittest.main()
