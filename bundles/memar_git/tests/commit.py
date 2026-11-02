#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import contextlib
import io
import os
import subprocess
import sys
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchRepository, bundle, errors

class CommitTakesOnlyWhatItNames(ScratchRepository):

    def test_a_named_path_is_committed_and_another_tasks_staging_stays_staged(self) -> None:
        self.put('mine.md', 'mine\n')
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        done = self.commit('mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('show', '--name-only', '--format=', 'HEAD'), 'mine.md')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'theirs.md')
        self.assertEqual(self.git('status', '--porcelain', '--', 'mine.md'), '')

    def test_a_path_someone_else_staged_is_refused(self) -> None:
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        done = self.commit('theirs.md')
        self.assertNotEqual(done.returncode, 0)
        self.assertIn('staged change', done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_a_move_staged_by_rename_is_committed_with_an_edit_that_keeps_the_rename(self) -> None:
        body = self.a_file_long_enough_to_keep_a_rename()
        moved = self.verb('rename', 'mine.md', 'moved.md')
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put('moved.md', '/* license */\n\n' + body)
        done = self.commit('mine.md', 'moved.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertTrue(self.git('show', 'HEAD:moved.md').startswith('/* license */'))
        self.assertRegex(self.git('diff-tree', '-r', '-M', '--name-status', 'HEAD^', 'HEAD'), '^R\\d+\\tmine.md\\tmoved.md$')
        self.assertEqual(self.git('status', '--porcelain', '--', 'mine.md', 'moved.md'), '')

    def test_a_move_whose_edit_loses_the_rename_is_refused(self) -> None:
        moved = self.verb('rename', 'mine.md', 'moved.md')
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put('moved.md', 'something else entirely\n')
        done = self.commit('mine.md', 'moved.md')
        self.assertNotEqual(done.returncode, 0)
        self.assertIn('no longer sees mine.md -> moved.md as a rename', done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(self.git('diff', '--cached', '-M', '--name-status'), 'R100\tmine.md\tmoved.md')

    def test_a_staged_move_named_at_one_end_only_is_refused(self) -> None:
        self.verb('rename', 'mine.md', 'moved.md')
        done = self.commit('moved.md')
        self.assertNotEqual(done.returncode, 0)
        self.assertIn('staged change', done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_a_staged_move_edited_since_is_committed_alone_through_as(self) -> None:
        moved = self.verb('rename', 'mine.md', 'moved.md')
        self.assertEqual(moved.returncode, 0, moved.stderr)
        self.put('moved.md', 'base\nedited\n')
        staged = self.repo / '.git' / 'moved.staged'
        staged.write_text('base\n', encoding='utf-8', newline='\n')
        done = self.commit('mine.md', '--as', f'moved.md={staged}')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('diff-tree', '-r', '-M100%', '--name-status', 'HEAD^', 'HEAD'), 'R100\tmine.md\tmoved.md')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.git('diff', '--name-only'), 'moved.md')

    def test_a_removal_staged_by_remove_is_committed(self) -> None:
        (self.repo / 'mine.md').unlink()
        self.git('rm', '-q', '--cached', 'mine.md')
        done = self.commit('mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('ls-tree', '--name-only', 'HEAD', 'mine.md'), '')

    def test_a_staged_removal_of_a_file_still_there_is_refused(self) -> None:
        self.git('rm', '-q', '--cached', 'mine.md')
        done = self.commit('mine.md')
        self.assertNotEqual(done.returncode, 0)
        self.assertIn('staged change', done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_a_fold_replaces_the_last_commit_and_leaves_out_a_change_unstaged(self) -> None:
        self.put('mine.md', 'mine\n')
        self.put('shared.md', 'shared\n')
        self.git('commit', '-q', '-am', 'second')
        done = self.commit('--fold', '1', '--leave-out', 'shared.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD^'), self.base)
        self.assertEqual(self.git('show', 'HEAD:mine.md'), 'mine')
        self.assertEqual(self.git('show', 'HEAD:shared.md'), 'base')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.git('diff', '--name-only'), 'shared.md')

    def test_a_prepared_file_commits_only_its_own_hunk(self) -> None:
        self.put('shared.md', 'base\nmine\ntheirs\n')
        prepared = self.repo / '.git' / 'shared.prepared'
        prepared.write_text('base\nmine\n', encoding='utf-8', newline='\n')
        done = self.commit('--as', f'shared.md={prepared}')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('show', 'HEAD:shared.md'), 'base\nmine')
        self.assertEqual((self.repo / 'shared.md').read_text(encoding='utf-8'), 'base\nmine\ntheirs\n')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')

    def test_the_shared_index_gets_spaces_unicode_modes_additions_and_removals_in_one_write(self) -> None:
        def listed(*args: str) -> list[str]:
            out = subprocess.run(['git', '-C', str(self.repo), *args], capture_output=True, check=True, timeout=60).stdout
            return sorted((entry for entry in out.decode('utf-8').split('\x00') if entry))
        odd = 'dir with space/ünïcode.md'
        (self.repo / 'dir with space').mkdir()
        self.put(odd, 'odd\n')
        self.put('run.sh', 'echo base\n')
        os.chmod(self.repo / 'run.sh', 493)
        self.put('gone.md', 'gone\n')
        self.git('add', '--', odd, 'run.sh', 'gone.md')
        self.git('update-index', '--chmod=+x', 'run.sh')
        self.git('commit', '-q', '-m', 'second')
        self.put(odd, 'odd\nedited\n')
        self.put('run.sh', 'echo edited\n')
        self.put('new file.md', 'new\n')
        (self.repo / 'gone.md').unlink()
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        named = (odd, 'run.sh', 'new file.md', 'gone.md')
        done = self.commit(*named)
        self.assertEqual(done.returncode, 0, done.stderr)
        in_head = listed('ls-tree', '-r', '-z', 'HEAD', '--', *named)
        self.assertEqual(sorted((entry.split('\t')[1] for entry in in_head)), sorted([odd, 'new file.md', 'run.sh']))
        self.assertIn('100755 blob', next((entry for entry in in_head if entry.endswith('\trun.sh'))))
        in_index = listed('ls-files', '-s', '-z', '--', *named)
        self.assertEqual(sorted((entry.replace(' blob ', ' ') for entry in in_head)), sorted((entry.replace(' 0\t', '\t') for entry in in_index)))
        self.assertEqual(listed('status', '--porcelain', '-z'), ['M  theirs.md'])

class CommitKnowsItsRepositoryAndKeepsItsOwnIndex(ScratchRepository):

    def test_the_repository_is_the_one_named_never_the_folder_it_is_run_from(self) -> None:
        self.put('mine.md', 'mine\n')
        done = self.commit('mine.md')
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('show', '--name-only', '--format=', 'HEAD'), 'mine.md')

    def test_the_verb_refuses_to_run_without_a_repository(self) -> None:
        refused = self.verb('commit', '-F', str(self.message), '--no-task', 'mine.md', repository=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('--repository', refused.stderr)

    def test_no_index_is_left_behind(self) -> None:
        self.put('mine.md', 'mine\n')
        self.assertEqual(self.commit('mine.md').returncode, 0)
        self.assertEqual([entry.name for entry in (self.repo / '.git').glob('memar-*')], [])

    def test_two_commits_at_once_do_not_share_an_index(self) -> None:
        import threading
        for name in ('a.md', 'b.md'):
            self.put(name, f'{name}\n')
            self.message.with_name(f'{name}.msg').write_text(f'add {name}\n', encoding='utf-8', newline='\n')
        done: dict[str, subprocess.CompletedProcess] = {}

        def commit(name: str) -> None:
            done[name] = self.verb('commit', '-F', str(self.message.with_name(f'{name}.msg')), '--no-task', name)
        threads = [threading.Thread(target=commit, args=(name,)) for name in ('a.md', 'b.md')]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=120)
        landed = [name for name, result in done.items() if result.returncode == 0]
        self.assertTrue(landed, {name: result.stderr for name, result in done.items()})
        for commit_id in self.git('rev-list', f'{self.base}..HEAD').split():
            self.assertEqual(len(self.git('show', '--name-only', '--format=', commit_id).split()), 1)

class CommitRefusesWithItsOwnError(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.module = bundle('services.commit')
        self.errors = errors()
        self.put('mine.md', 'mine\n')

    def commit_here(self, paths=('mine.md',), prepared=(), leave_out=(), fold=0, tasks=(), no_task=True):
        return self.module.cmd_commit(self.repo, [Path(p) for p in paths], list(prepared), [Path(p) for p in leave_out], fold, self.message, tasks=list(tasks), no_task=no_task)

    def refused(self, error, **given):
        before = self.git('rev-parse', 'HEAD')
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(error) as raised:
                self.commit_here(**given)
        self.assertEqual(self.git('rev-parse', 'HEAD'), before)
        return str(raised.exception)

    def test_nothing_named_is_nothing_to_commit(self) -> None:
        self.refused(self.errors.NothingToCommit, paths=())

    def test_a_result_equal_to_the_parent_is_nothing_to_commit(self) -> None:
        self.put('mine.md', 'base\n')
        self.refused(self.errors.NothingToCommit)

    def test_a_negative_fold_is_a_misused_fold(self) -> None:
        self.refused(self.errors.FoldMisused, fold=-1)

    def test_a_leave_out_outside_a_fold_is_a_misused_fold(self) -> None:
        self.refused(self.errors.FoldMisused, leave_out=('shared.md',))

    def test_a_fold_over_a_merge_is_refused(self) -> None:
        self.git('checkout', '-q', '-b', 'side', self.base)
        self.put('theirs.md', 'side\n')
        self.git('commit', '-q', '-am', 'side')
        self.git('checkout', '-q', 'main')
        self.git('merge', '-q', '--no-ff', '--no-edit', 'side')
        self.refused(self.errors.MergeInFold, fold=1)

    def test_a_fold_reaching_upstream_is_published_history(self) -> None:
        self.git('commit', '-q', '-am', 'second')
        self.git('branch', 'published')
        self.git('branch', '--set-upstream-to=published')
        self.refused(self.errors.PublishedHistory, fold=1)

    def test_an_empty_message_is_refused(self) -> None:
        self.message.write_text('\n', encoding='utf-8', newline='\n')
        self.refused(self.errors.EmptyMessage)

    def test_a_replacement_that_is_not_path_equals_file_is_refused(self) -> None:
        self.refused(self.errors.ReplacementMalformed, paths=(), prepared=('mine.md',))

    def test_a_replacement_whose_source_is_not_a_file_is_refused(self) -> None:
        self.refused(self.errors.ReplacementMalformed, paths=(), prepared=(f'mine.md={self.repo / "nowhere"}',))

    def test_a_path_outside_the_repository_is_not_named(self) -> None:
        self.refused(self.errors.NotNamed, paths=(str(self.elsewhere / 'other.md'),))

    def test_a_path_someone_else_staged_is_staged_by_others(self) -> None:
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        self.refused(self.errors.StagedByOthers, paths=('theirs.md',))

    def test_an_edit_that_loses_a_staged_move_is_a_move_that_would_not_be_a_rename(self) -> None:
        self.assertEqual(self.verb('rename', 'mine.md', 'moved.md').returncode, 0)
        self.put('moved.md', 'something else entirely\n')
        said = self.refused(self.errors.MoveWouldNotBeRename, paths=('mine.md', 'moved.md'))
        self.assertIn('mine.md', said)

    def test_a_folder_that_is_no_repository_is_refused(self) -> None:
        with self.assertRaises(self.errors.NotARepository):
            self.module.cmd_commit(self.repo / 'no-such-folder', [Path('x')], [], [], 0, self.message, tasks=[], no_task=True)

class CommitWaitsOutALock(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.module = bundle('services.commit')
        self.lock_module = bundle('services._lock')
        self.run_module = bundle('services._run')
        self.errors = errors()
        self.lock = self.repo / '.git' / 'index.lock'
        self.addCleanup(lambda: self.lock.exists() and self.lock.unlink())
        self.put('mine.md', 'mine\n')

    def here(self, *patches):
        said = io.StringIO()
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stderr(said))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_WAIT_SECONDS', 0.5))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_FIRST_PAUSE_SECONDS', 0.05))
            for patch in patches:
                stack.enter_context(patch)
            try:
                self.module.cmd_commit(self.repo, [Path('mine.md')], [], [], 0, self.message, tasks=[], no_task=True)
            except self.errors.Locked as stopped:
                return (str(stopped), said.getvalue())
        return (None, said.getvalue())

    def grabbed_after_update_ref(self):
        real = self.run_module.attempt

        def grabbed(args, root, env=None, data=None):
            done = real(args, root, env, data)
            if args[0] == 'update-ref':
                self.lock.write_text('', encoding='utf-8')
            return done
        return unittest.mock.patch.object(self.run_module, 'attempt', grabbed)

    def held_for_an_hour(self) -> None:
        import time
        self.lock.write_text('', encoding='utf-8')
        hour_ago = time.time() - 3600
        os.utime(self.lock, (hour_ago, hour_ago))

    def test_a_lock_let_go_within_the_wait_is_waited_for_and_the_commit_finishes(self) -> None:
        self.lock.write_text('', encoding='utf-8')
        released = unittest.mock.patch.object(self.lock_module.time, 'sleep', side_effect=lambda seconds: self.lock.unlink(missing_ok=True))
        stopped, said = self.here(released)
        self.assertIsNone(stopped, said)
        self.assertIn('waiting up to', said)
        self.assertIn('index.lock', said)
        self.assertEqual(self.git('rev-parse', 'HEAD^'), self.base)

    def test_a_lock_held_past_the_wait_is_locked_before_head_moves(self) -> None:
        self.held_for_an_hour()
        stopped, _ = self.here()
        self.assertIsNotNone(stopped)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertIn('HEAD was not moved', stopped)
        self.assertIn(str(self.lock.resolve()), stopped)
        self.assertRegex(stopped, 'last written 36\\d\\d s ago')
        self.assertIn('never does', stopped)
        self.assertIn('rerun the same command', stopped)
        self.assertTrue(self.lock.exists())

    def test_a_lock_taken_after_head_moved_says_how_to_finish_and_how_to_undo(self) -> None:
        stopped, _ = self.here(self.grabbed_after_update_ref())
        self.assertIsNotNone(stopped)
        made = self.git('rev-parse', 'HEAD')
        self.assertEqual(self.git('rev-parse', 'HEAD^'), self.base)
        self.assertIn(f'HEAD moved from {self.base} to the commit {made}', stopped)
        self.assertIn(f'reindex --repository {self.repo} --from {made} --was {self.base} -- mine.md', stopped)
        self.assertIn(f'reindex --repository {self.repo} --undo --from {made} --was {self.base} -- mine.md', stopped)
        self.assertNotIn('update-ref HEAD', stopped)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'mine.md')

    def test_a_failure_that_is_not_a_lock_is_a_git_failure_and_is_not_retried(self) -> None:
        real, calls = (self.run_module.attempt, [])

        def refused(args, root, env=None, data=None):
            if args[0] != 'update-ref':
                return real(args, root, env, data)
            calls.append(args)
            return subprocess.CompletedProcess(['git', '-C', str(root), *args], 128, b'', b"fatal: update_ref failed for ref 'HEAD': cannot lock ref 'HEAD': is at 1234 but expected 5678\n")
        said = io.StringIO()
        with contextlib.redirect_stderr(said), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises((self.errors.GitFailed, self.errors.Locked)) as raised:
                with unittest.mock.patch.object(self.run_module, 'attempt', refused):
                    self.module.cmd_commit(self.repo, [Path('mine.md')], [], [], 0, self.message, tasks=[], no_task=True)
        self.assertEqual(len(calls), 1)
        self.assertNotIn('waiting', said.getvalue())
        self.assertIn('is at 1234 but expected 5678', str(raised.exception))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

if __name__ == '__main__':
    unittest.main()
