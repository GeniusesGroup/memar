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

class ReindexFinishesOrUndoesAStoppedCommit(ScratchRepository):

    def setUp(self) -> None:
        super().setUp()
        self.commit_module = bundle('services.commit')
        self.reindex_module = bundle('services.reindex')
        self.run_module = bundle('services._run')
        self.lock_module = bundle('services._lock')
        self.errors = errors()
        self.lock = self.repo / '.git' / 'index.lock'
        self.addCleanup(lambda: self.lock.exists() and self.lock.unlink())
        self.put('mine.md', 'mine\n')

    def stopped_after_head_moved(self, paths=('mine.md',)) -> str:
        real = self.run_module.attempt

        def grabbed(args, root, env=None, data=None):
            done = real(args, root, env, data)
            if args[0] == 'update-ref':
                self.lock.write_text('', encoding='utf-8')
            return done
        with contextlib.ExitStack() as stack:
            stack.enter_context(contextlib.redirect_stderr(io.StringIO()))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_WAIT_SECONDS', 0.5))
            stack.enter_context(unittest.mock.patch.object(self.lock_module, 'LOCK_FIRST_PAUSE_SECONDS', 0.05))
            stack.enter_context(unittest.mock.patch.object(self.run_module, 'attempt', grabbed))
            with self.assertRaises(self.errors.Locked):
                self.commit_module.cmd_commit(self.repo, [Path(p) for p in paths], [], [], 0, self.message, tasks=[], no_task=True)
        self.lock.unlink()
        return self.git('rev-parse', 'HEAD')

    def test_the_finish_gives_the_shared_index_the_landed_entries(self) -> None:
        made = self.stopped_after_head_moved()
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'mine.md')
        finished = self.verb('reindex', '--from', made, '--was', self.base, '--', 'mine.md')
        self.assertEqual(finished.returncode, 0, finished.stderr)
        self.assertEqual(self.git('status', '--porcelain', '--', 'mine.md'), '')

    def test_the_undo_moves_head_back_and_leaves_the_index_as_it_was(self) -> None:
        made = self.stopped_after_head_moved()
        undone = self.verb('reindex', '--undo', '--from', made, '--was', self.base, '--', 'mine.md')
        self.assertEqual(undone.returncode, 0, undone.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')
        self.assertEqual(self.git('diff', '--name-only'), 'mine.md')

    def test_the_undo_twice_is_a_head_that_moved(self) -> None:
        made = self.stopped_after_head_moved()
        self.assertEqual(self.verb('reindex', '--undo', '--from', made, '--was', self.base, '--', 'mine.md').returncode, 0)
        with self.assertRaises(self.errors.ReindexHeadMoved) as raised:
            self.reindex_module.cmd_reindex(self.repo, [Path('mine.md')], made, self.base, True)
        self.assertIn('it has moved since', str(raised.exception))
        self.assertIn('Nothing was changed', str(raised.exception))
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)

    def test_the_undo_after_the_finish_is_an_index_that_changed(self) -> None:
        made = self.stopped_after_head_moved()
        self.assertEqual(self.verb('reindex', '--from', made, '--was', self.base, '--', 'mine.md').returncode, 0)
        with self.assertRaises(self.errors.IndexChanged) as raised:
            self.reindex_module.cmd_reindex(self.repo, [Path('mine.md')], made, self.base, True)
        self.assertIn('Nothing was changed', str(raised.exception))
        self.assertEqual(self.git('rev-parse', 'HEAD'), made)

    def test_the_finish_after_head_moved_since_is_a_head_that_moved(self) -> None:
        made = self.stopped_after_head_moved()
        self.git('update-ref', 'HEAD', self.base)
        with self.assertRaises(self.errors.ReindexHeadMoved):
            self.reindex_module.cmd_reindex(self.repo, [Path('mine.md')], made, self.base, False)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(self.git('diff', '--cached', '--name-only'), '')

    def test_a_path_staged_since_is_staged_by_others(self) -> None:
        self.put('theirs.md', 'theirs\n')
        self.git('add', 'theirs.md')
        with self.assertRaises(self.errors.StagedByOthers) as raised:
            self.reindex_module.cmd_reindex(self.repo, [Path('theirs.md')], 'HEAD', 'HEAD', False)
        self.assertIn('Nothing was changed', str(raised.exception))
        self.assertEqual(self.git('diff', '--cached', '--name-only'), 'theirs.md')

    def test_the_undo_of_a_staged_rename_leaves_it_staged(self) -> None:
        self.put('mine.md', 'base\n')
        self.assertEqual(self.verb('rename', 'mine.md', 'moved.md').returncode, 0)
        made = self.stopped_after_head_moved(('mine.md', 'moved.md'))
        undone = self.verb('reindex', '--undo', '--from', made, '--was', self.base, '--', 'mine.md', 'moved.md')
        self.assertEqual(undone.returncode, 0, undone.stderr)
        self.assertEqual(self.git('rev-parse', 'HEAD'), self.base)
        self.assertEqual(self.git('diff', '--cached', '-M', '--name-status'), 'R100\tmine.md\tmoved.md')

    def test_the_verb_refuses_to_run_without_a_repository(self) -> None:
        refused = self.verb('reindex', '--from', self.base, '--was', self.base, 'mine.md', repository=False)
        self.assertNotEqual(refused.returncode, 0)
        self.assertIn('--repository', refused.stderr)

if __name__ == '__main__':
    unittest.main()
