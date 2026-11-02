#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..errors.errors import GitFailed
from ._edge import guarded
from ._run import repository_flag, repository_root, run_captured, run_git

def _working_tree_dirty(root: Path) -> bool:
    porcelain = run_captured(['status', '--porcelain', '--untracked-files=normal'], cwd=root)
    return bool(porcelain.stdout.strip())

def cmd_stash(repository: Path, message: str | None) -> None:
    root = repository_root(repository)
    if not _working_tree_dirty(root):
        print('nothing to stash', file=sys.stderr)
        return
    args = ['stash', 'push', '--include-untracked']
    if message:
        args.extend(['-m', message])
    run_git(args, root)
    print('stashed tracked + untracked (not ignored).\nRecover with `git stash pop` / `git stash apply` when ready.\nIgnored paths were not included — commit those if they must survive.', file=sys.stderr)

def describe(verbs):
    p_stash = verbs.add_parser('stash', help='stash tracked+untracked WIP (not ignored); prefer over discard', description='Set uncommitted work aside where a later task can get it back.')
    repository_flag(p_stash)
    p_stash.add_argument('-m', '--message', default=None, help='optional stash message')
    return guarded(lambda a: cmd_stash(a.repository, a.message))
