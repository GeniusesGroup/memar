#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 120
import contextlib
import io
import os
import sys
import time
import unittest
import unittest.mock
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _scratch import ScratchRepository, bundle, errors

class UncommitKeepsTheWork(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.put('mine.md', 'mine\n')
        self.put('shared.md', 'shared\n')
        self.git('commit', '-q', '-am', 'second')
        self.second = self.git('rev-parse', 'HEAD')

    def uncommit(self, expect: str):
        return self.verb('uncommit', '--expect', expect)

    def test_head_goes_back_and_the_work_stays_in_the_tree_unstaged(self) -> None:
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        done = self.uncommit(self.second[:12])
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual((self.repo / 'mine.md').read_text(encoding='utf-8'), 'mine\n')
        self.assertEqual(self.git('diff', '--name-only'), 'mine.md\nshared.md')
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'theirs.md')
        self.assertIn('reflog', done.stderr)
        self.assertIn(self.second, done.stderr)
        self.assertIn(self.second, self.git('reflog', '-n', '2', '--format=%H'))

    def test_the_verb_refuses_to_run_without_a_repository(self) -> None:
        refused = self.verb('uncommit', '--expect', self.second, repository=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('--repository', refused.stderr)

    def test_a_commit_that_is_not_head_is_refused_by_the_cli(self) -> None:
        done = self.uncommit(self.base)
        self.assertNotEqual(done.returncode, 0)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.second)

class UncommitRefusesWithItsOwnError(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.module = bundle('services.uncommit')
        self.errors = errors()
        self.put('mine.md', 'mine\n')
        self.put('shared.md', 'shared\n')
        self.git('commit', '-q', '-am', 'second')
        self.second = self.git('rev-parse', 'HEAD')

    def refused(self, error, expect: str):
        before = self.git('rev-parse', 'HEAD')
        with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(error) as raised:
                self.module.cmd_uncommit(self.repo, expect)
        self.assertEqual(self.git('rev-parse', 'HEAD'), before)
        return str(raised.exception)

    def test_a_name_instead_of_an_id_is_not_named(self) -> None:
        self.refused(self.errors.NotNamed, 'HEAD')

    def test_a_commit_that_is_not_the_head_is_not_head(self) -> None:
        self.refused(self.errors.NotHead, self.base)

    def test_a_merge_has_not_one_parent(self) -> None:
        self.git('checkout', '-q', '-b', 'side', self.base)
        self.put('theirs.md', 'side\n')
        self.git('commit', '-q', '-am', 'side')
        self.git('checkout', '-q', 'main')
        self.git('merge', '-q', '--no-ff', '--no-edit', 'side')
        merge = self.git('rev-parse', 'HEAD')
        self.assertIn('2 parents', self.refused(self.errors.NotOneParent, merge))

    def test_a_root_commit_has_not_one_parent(self) -> None:
        self.git('checkout', '-q', '--orphan', 'fresh')
        self.git('commit', '-q', '-m', 'root')
        root = self.git('rev-parse', 'HEAD')
        self.assertIn('0 parents', self.refused(self.errors.NotOneParent, root))

    def test_a_commit_already_upstream_is_published_history(self) -> None:
        self.git('branch', 'published')
        self.git('branch', '--set-upstream-to=published')
        self.refused(self.errors.PublishedHistory, self.second)

    def test_a_path_of_the_commit_with_its_own_staged_change_is_staged_by_others(self) -> None:
        self.put('mine.md', 'mine, and more\n')
        self.git('add', 'mine.md')
        self.refused(self.errors.StagedByOthers, self.second)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'mine.md')

class UncommitWaitsOutALock(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.module = bundle('services.uncommit')
        self.lock_module = bundle('services._lock')
        self.run_module = bundle('services._run')
        self.errors = errors()
        self.lock = self.repo / '.git' / 'index.lock'
        self.addCleanup(lambda: self.lock.exists() and self.lock.unlink())
        self.put('mine.md', 'mine\n')
        self.git('commit', '-q', '-am', 'second')
        self.second = self.git('rev-parse', 'HEAD')

    def here(self, *patches) -> str:
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_WAIT_SECONDS', 0.5))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_FIRST_PAUSE_SECONDS', 0.05))
            for patch in patches:
                stack.enter_context(patch)
            with self.assertRaises(self.errors.Locked) as raised:
                self.module.cmd_uncommit(self.repo, self.second)
        return str(raised.exception)

    def test_a_lock_held_past_the_wait_changes_nothing(self) -> None:
        self.lock.write_text('', encoding='utf-8')
        hour_ago = time.time() - 3600
        os.utime(self.lock, (hour_ago, hour_ago))
        stopped = self.here()
        self.assertIn(f'nothing was changed: HEAD is still {self.second}', stopped)
        self.assertIn(str(self.lock.resolve()), stopped)
        self.assertIn('rerun the same command', stopped)
        self.assertTrue(self.lock.exists())
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.second)

    def test_a_lock_taken_after_head_moved_names_the_reindex_calls(self) -> None:
        real = self.run_module.attempt

        def grabbed(args, root, env=None, data=None):
            done = real(args, root, env, data)
            if args[0] == 'update-ref':
                self.lock.write_text('', encoding='utf-8')
            return done
        stopped = self.here(unittest.mock.patch.object(self.run_module, 'attempt', grabbed))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertIn(f'HEAD moved from {self.second} back to its parent {self.base}', stopped)
        self.assertIn(f'reindex --repository {self.repo} --from {self.base} --was {self.second} -- mine.md', stopped)
        self.assertIn(f'reindex --repository {self.repo} --undo --from {self.base} --was {self.second} -- mine.md', stopped)

if __name__ == '__main__':
    unittest.main()
