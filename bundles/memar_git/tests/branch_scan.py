#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Tests for the whole-branch read in `bundles/memar_git/services/branch.py`.

    python bundles/memar_git/tests/branch_scan.py

What is pinned:

  OneReadForAll  `read_named_of_all` answers the named files of every task the branch holds, and
                 starts git a fixed number of times however many tasks there are.
"""
from __future__ import annotations
TIER = 'system'
BUDGET_SECONDS = 60
from importlib import import_module
import subprocess
import sys
import unittest
from pathlib import Path
_m_test_scratch = import_module('modules.process.test.services.test_scratch')
remove_tree = _m_test_scratch.remove_tree
suite_scratch = _m_test_scratch.suite_scratch
branch = import_module('bundles.memar_git.services.branch')
task_store = import_module('bundles.memar_git.services.task_store')
GIT_STARTS_AT_MOST = 3

class OneReadForAll(unittest.TestCase):

    def setUp(self) -> None:
        import tempfile
        self.repo = Path(tempfile.mkdtemp(dir=suite_scratch()))
        subprocess.run(['git', '-C', str(self.repo), 'init', '-q'], check=True)
        subprocess.run(['git', '-C', str(self.repo), 'config', 'user.email', 'test@example.com'], check=True)
        subprocess.run(['git', '-C', str(self.repo), 'config', 'user.name', 'test'], check=True)
        (self.repo / 'seed.txt').write_text('seed', encoding='utf-8')
        subprocess.run(['git', '-C', str(self.repo), 'add', '.'], check=True)
        subprocess.run(['git', '-C', str(self.repo), 'commit', '-q', '-m', 'seed'], check=True)
        self.addCleanup(remove_tree, self.repo)

    def test_every_task_is_answered_with_a_fixed_number_of_git_starts(self):
        for number in range(5):
            task_store.put_files(f'20261101-T00000{number}Z-{number}', {'task.yaml': f'title: t{number}\n'.encode(), 'content.00001.md': b'long text'}, self.repo)
        starts = []
        original = branch._git
        branch._git = lambda project, args, data=None: (starts.append(args[0]), original(project, args, data))[1]
        try:
            found = branch.read_named_of_all(self.repo, ('task.yaml',))
        finally:
            branch._git = original
        self.assertEqual(sorted(found), [f'20261101-T00000{number}Z-{number}' for number in range(5)])
        self.assertEqual(found['20261101-T0000003Z-3'] if '20261101-T0000003Z-3' in found else found['20261101-T000003Z-3'], {'task.yaml': b'title: t3\n'})
        self.assertLessEqual(len(starts), GIT_STARTS_AT_MOST + 1)

if __name__ == '__main__':
    unittest.main()
