#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import contextlib
import io
import sys
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchRepository, bundle, errors

class EveryWorkingVerbTakesTheRepository(ScratchRepository):

    def test_each_of_them_requires_the_repository_flag(self) -> None:
        for verb, rest in (('rename', ['mine.md', 'moved.md']), ('remove', ['mine.md']), ('stash', []), ('restore', ['mine.md']), ('undelete', ['mine.md'])):
            with self.subTest(verb=verb):
                done = self.verb(verb, *rest, repository=False)
                self.assertNotEqual(done.returncode, 0)
                self.assertIn('--repository', done.stderr)
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_a_rename_moves_inside_the_repository_named_with_relative_paths(self) -> None:
        done = self.verb('rename', 'mine.md', 'moved.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue((self.repo / 'moved.md').exists())
        self.assertFalse((self.repo / 'mine.md').exists())
        self.assertIn('R  mine.md -> moved.md', self.git('status', '--porcelain'))

    def test_a_remove_sends_the_path_to_the_recycle_bin_and_stages_the_disappearance(self) -> None:
        done = self.verb('remove', 'mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertFalse((self.repo / 'mine.md').exists())
        self.assertIn('D  mine.md', self.git('status', '--porcelain'))

    def test_a_stash_sets_aside_the_work_of_the_repository_named(self) -> None:
        self.put('mine.md', 'edited\n')
        self.put('untracked.md', 'new\n')
        done = self.verb('stash')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertIn('stash@{0}', self.git('stash', 'list'))

    def test_a_clean_tree_is_not_stashed_at_all(self) -> None:
        done = self.verb('stash')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn('nothing to stash', done.stderr)
        self.assertEqual(self.git('stash', 'list'), '')

    def test_a_restore_discards_only_with_the_confirmation(self) -> None:
        self.put('mine.md', 'edited\n')
        refused = self.verb('restore', 'mine.md')
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('M mine.md', self.git('status', '--porcelain'))
        done = self.verb('restore', '--confirm', 'DISCARD-UNCOMMITTED', 'mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_an_undelete_brings_a_path_back_into_the_index_and_the_tree(self) -> None:
        (self.repo / 'mine.md').unlink()
        done = self.verb('undelete', 'mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual((self.repo / 'mine.md').read_text(encoding='utf-8'), 'base\n')
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_a_path_outside_the_repository_is_refused_and_left_alone(self) -> None:
        done = self.verb('remove', str(self.elsewhere / 'other.md'))
        self.assertNotEqual(done.returncode, 0)
        self.assertTrue((self.elsewhere / 'other.md').exists())

class WorkingVerbsRefuseWithTheirOwnError(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.errors = errors()

    def call(self, module: str, function: str, *arguments):
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            return getattr(bundle(f'services.{module}'), function)(self.repo, *arguments)

    def test_a_rename_of_a_source_that_does_not_exist_is_a_path_absent(self) -> None:
        with self.assertRaises(self.errors.PathAbsent):
            self.call('rename', 'cmd_rename', Path('nowhere.md'), Path('moved.md'))
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_a_remove_of_a_path_neither_there_nor_tracked_is_a_path_absent(self) -> None:
        with self.assertRaises(self.errors.PathAbsent):
            self.call('remove', 'cmd_remove', [Path('nowhere.md')])

    def test_a_remove_of_a_path_outside_the_repository_is_not_named(self) -> None:
        with self.assertRaises(self.errors.NotNamed):
            self.call('remove', 'cmd_remove', [self.elsewhere / 'other.md'])
        self.assertTrue((self.elsewhere / 'other.md').exists())

    def test_an_undelete_from_a_revision_that_does_not_hold_the_path_is_a_path_absent(self) -> None:
        with self.assertRaises(self.errors.PathAbsent):
            self.call('undelete', 'cmd_undelete', [Path('nowhere.md')], 'HEAD')

    def test_an_undelete_from_a_revision_git_does_not_know_is_a_git_failure_or_an_absent_path(self) -> None:
        with self.assertRaises((self.errors.GitFailed, self.errors.PathAbsent)):
            self.call('undelete', 'cmd_undelete', [Path('mine.md')], 'no-such-revision')

    def test_a_restore_without_the_confirmation_is_not_confirmed_and_names_the_word_and_stash(self) -> None:
        self.put('mine.md', 'edited\n')
        with self.assertRaises(self.errors.NotConfirmed) as raised:
            self.call('restore', 'cmd_restore', [Path('mine.md')], None)
        self.assertIn('DISCARD-UNCOMMITTED', str(raised.exception))
        self.assertIn('stash', str(raised.exception))
        self.assertEqual((self.repo / 'mine.md').read_text(encoding='utf-8'), 'edited\n')

    def test_a_restore_with_a_wrong_word_is_not_confirmed(self) -> None:
        self.put('mine.md', 'edited\n')
        with self.assertRaises(self.errors.NotConfirmed):
            self.call('restore', 'cmd_restore', [Path('mine.md')], 'yes')
        self.assertEqual((self.repo / 'mine.md').read_text(encoding='utf-8'), 'edited\n')

    def test_a_restore_naming_no_path_is_refused(self) -> None:
        with self.assertRaises((self.errors.NotNamed, self.errors.NotConfirmed)):
            self.call('restore', 'cmd_restore', [], 'DISCARD-UNCOMMITTED')

    def test_a_clean_tree_stashes_nothing_and_succeeds(self) -> None:
        stash = bundle('services.stash')
        said = io.StringIO()
        with contextlib.redirect_stderr(said), contextlib.redirect_stdout(io.StringIO()):
            stash.cmd_stash(self.repo, None)
        self.assertIn('nothing to stash', said.getvalue())

    def test_a_rename_onto_an_existing_destination_is_a_git_failure(self) -> None:
        with self.assertRaises(self.errors.GitFailed):
            self.call('rename', 'cmd_rename', Path('mine.md'), Path('theirs.md'))

if __name__ == '__main__':
    unittest.main()
