#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..errors.errors import GitFailed, PathAbsent
from ._edge import guarded
from ._run import in_repo, repository_flag, repository_root, run_captured, run_git

def cmd_undelete(repository: Path, paths: list[Path], source: str) -> None:
    root = repository_root(repository)
    for given in paths:
        path = in_repo(given, root)
        listed = run_captured(['ls-tree', source, '--', path], cwd=root)
        if listed.returncode != 0 or not listed.stdout.strip():
            raise PathAbsent(f'{path} is not in {source}, so there is nothing to bring back')
        state = run_captured(['ls-files', '--stage', '--', path], cwd=root).stdout.strip()
        before = state if state else 'absent from index'
        print(f'recovering {path} from {source} (index was: {before})', file=sys.stderr)
        run_git(['restore', f'--source={source}', '--staged', '--worktree', '--', path], root)
        after = run_captured(['ls-files', '--stage', '--', path], cwd=root).stdout.strip()
        if not after:
            raise GitFailed(f'{path} did not come back into the index')
        print(f'recovered: {after}', file=sys.stderr)
    print('Recovered into the index and the working tree. Nothing was committed, and\nnothing else in the index or the tree was touched.', file=sys.stderr)

def describe(verbs):
    p_undelete = verbs.add_parser('undelete', help='bring a deleted path back from a commit, into index and worktree', description='Bring each deleted or untracked-back PATH back from a commit; it says what it recovered.')
    repository_flag(p_undelete)
    p_undelete.add_argument('paths', nargs='+', type=Path, help='paths to bring back, relative to the repository or absolute')
    p_undelete.add_argument('--from', dest='source', default='HEAD', metavar='REV', help='the commit to bring the path back from (default: HEAD)')
    return guarded(lambda a: cmd_undelete(a.repository, a.paths, a.source))
