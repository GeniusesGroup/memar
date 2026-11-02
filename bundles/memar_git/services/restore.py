#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..errors.errors import NotConfirmed, NotNamed
from ._edge import guarded
from ._run import in_repo, repository_flag, repository_root, run_git
DISCARD_CONFIRM = 'DISCARD-UNCOMMITTED'

def cmd_restore(repository: Path, paths: list[Path], confirm: str | None) -> None:
    if confirm != DISCARD_CONFIRM:
        raise NotConfirmed(f'refusing to discard uncommitted work.\nTo tidy status without losing WIP: commit, or run `memar git stash --repository PATH`.\ngitignore does not hide tracked modifications.\nIrreversible discard requires --confirm {DISCARD_CONFIRM} (do not pass that casually).')
    if not paths:
        raise NotNamed('restore requires one or more paths')
    root = repository_root(repository)
    named = [in_repo(p, root) for p in paths]
    run_git(['restore', '--source=HEAD', '--worktree', '--'] + named, root)
    print(f'discarded working-tree changes for the named paths (confirmed {DISCARD_CONFIRM}).', file=sys.stderr)

def describe(verbs):
    p_restore = verbs.add_parser('restore', help='refuse discard by default; needs --confirm DISCARD-UNCOMMITTED', description='Discard uncommitted changes to each PATH, and refuse unless --confirm is\ngiven: "tidy the status" is how uncommitted work is most often lost. If\nyou want the work set aside, `stash` is the command for that.', formatter_class=argparse.RawDescriptionHelpFormatter)
    repository_flag(p_restore)
    p_restore.add_argument('paths', nargs='+', type=Path, help='paths to discard changes of, relative to the repository or absolute')
    p_restore.add_argument('--confirm', default=None, help=f'must be exactly {DISCARD_CONFIRM} to discard')
    return guarded(lambda a: cmd_restore(a.repository, a.paths, a.confirm))
