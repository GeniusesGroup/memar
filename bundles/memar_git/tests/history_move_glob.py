#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import contextlib
import io
import os
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import tempfile
from _scratch import bundle, errors, git_in, suite_scratch

def move(*args, **keywords):
    return bundle('services.history_move_glob').history_move_glob(*args, **keywords)

def moved(*args, **keywords):
    advice = io.StringIO()
    with contextlib.redirect_stderr(advice):
        listing = move(*args, **keywords)
    return listing, advice.getvalue()

class ScratchRepository(unittest.TestCase):

    def setUp(self) -> None:
        scratch = tempfile.TemporaryDirectory(dir=suite_scratch(), prefix='tmp-git-move-', ignore_cleanup_errors=True)
        self.addCleanup(scratch.cleanup)
        self.root = Path(scratch.name)
        self.repo = self.root / 'repo'
        self.repo.mkdir()
        git_in(self.repo, 'init', '-q', '-b', 'main')
        git_in(self.repo, 'config', 'user.name', 'Test')
        git_in(self.repo, 'config', 'user.email', 'test@example.org')
        git_in(self.repo, 'config', 'core.autocrlf', 'false')
        body = ''.join((f'line {number}\n' for number in range(20)))
        for name in ('one.md', 'two.md', 'keep.txt'):
            (self.repo / name).write_text(body + name + '\n', encoding='utf-8', newline='\n')
        (self.repo / 'sub').mkdir()
        (self.repo / 'sub' / 'deep.md').write_text(body, encoding='utf-8', newline='\n')
        (self.repo / 'docs').mkdir()
        git_in(self.repo, 'add', '.')
        git_in(self.repo, 'commit', '-q', '-m', 'base')
        self.head = git_in(self.repo, 'rev-parse', 'HEAD')
        here = os.getcwd()
        os.chdir(self.repo)
        self.addCleanup(os.chdir, here)

class MoveListsUnlessApplied(ScratchRepository):

    def test_without_apply_it_lists_the_files_that_match_and_moves_nothing(self) -> None:
        listing, _ = moved('*.md', self.repo / 'docs')
        self.assertIn('one.md', listing)
        self.assertIn('two.md', listing)
        self.assertNotIn('keep.txt', listing)
        self.assertNotIn('deep.md', listing)
        self.assertTrue((self.repo / 'one.md').is_file())
        self.assertEqual(git_in(self.repo, 'status', '--porcelain'), '')

    def test_without_apply_the_advice_to_commit_the_renames_by_themselves_goes_to_the_error_stream(self) -> None:
        _, advice = moved('*.md', self.repo / 'docs')
        self.assertIn('apply', advice)
        self.assertIn('commit', advice)

    def test_without_apply_the_destination_need_not_exist(self) -> None:
        listing, _ = moved('*.md', self.repo / 'not-made-yet')
        self.assertIn('one.md', listing)

    def test_the_pattern_reaches_only_files_not_folders(self) -> None:
        listing, _ = moved('*', self.repo / 'docs')
        self.assertNotIn('sub\n', listing + '\n')
        self.assertIn('keep.txt', listing)

    def test_a_pattern_may_reach_into_a_subfolder_of_the_current_folder(self) -> None:
        listing, _ = moved('sub/*.md', self.repo / 'docs')
        self.assertIn('deep.md', listing)

class MoveApplies(ScratchRepository):

    def test_with_apply_each_match_is_moved_keeping_its_history_and_nothing_is_committed(self) -> None:
        moved('*.md', self.repo / 'docs', apply=True)
        self.assertFalse((self.repo / 'one.md').exists())
        self.assertTrue((self.repo / 'docs' / 'one.md').is_file())
        self.assertTrue((self.repo / 'docs' / 'two.md').is_file())
        self.assertTrue((self.repo / 'keep.txt').is_file())
        renames = [line for line in git_in(self.repo, 'diff', '--cached', '--name-status', '-M').splitlines() if line.startswith('R')]
        self.assertEqual(len(renames), 2)
        self.assertEqual(git_in(self.repo, 'rev-parse', 'HEAD'), self.head)

    def test_with_apply_the_advice_is_not_printed(self) -> None:
        _, advice = moved('*.md', self.repo / 'docs', apply=True)
        self.assertEqual(advice, '')

class MoveRefuses(ScratchRepository):

    def test_an_empty_pattern_is_refused(self) -> None:
        with self.assertRaises(errors().PatternMalformed):
            move('', self.repo / 'docs')

    def test_an_absolute_pattern_is_refused(self) -> None:
        with self.assertRaises(errors().PatternMalformed):
            move(str(self.repo / '*.md'), self.repo / 'docs')

    def test_when_applying_a_destination_that_is_not_a_folder_is_refused_and_nothing_moves(self) -> None:
        with self.assertRaises(errors().NotAFolder):
            move('*.md', self.repo / 'keep.txt', apply=True)
        with self.assertRaises(errors().NotAFolder):
            move('*.md', self.repo / 'absent', apply=True)
        self.assertTrue((self.repo / 'one.md').is_file())
        self.assertEqual(git_in(self.repo, 'status', '--porcelain'), '')

    def test_a_pattern_matching_no_file_is_refused(self) -> None:
        with self.assertRaises(errors().NoMatch):
            move('*.absent', self.repo / 'docs')
        with self.assertRaises(errors().NoMatch):
            move('*.absent', self.repo / 'docs', apply=True)

class MoveFails(ScratchRepository):

    def test_a_file_the_rename_cannot_move_is_a_failure_and_those_before_it_stay_moved(self) -> None:
        (self.repo / 'docs' / 'two.md').write_text('already here\n', encoding='utf-8', newline='\n')
        with self.assertRaises(errors().MoveFailed):
            move('*.md', self.repo / 'docs', apply=True)
        self.assertTrue((self.repo / 'docs' / 'one.md').is_file())
        self.assertFalse((self.repo / 'one.md').exists())
        self.assertTrue((self.repo / 'two.md').is_file())
if __name__ == '__main__':
    unittest.main(verbosity=2)
