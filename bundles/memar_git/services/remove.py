#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

from __future__ import annotations
import argparse
from importlib import import_module
import subprocess
import sys
from pathlib import Path
from ..errors.errors import GitFailed, PathAbsent
from ._edge import guarded
from ._run import in_repo, repository_flag, repository_root, run_captured, run_git

def cmd_remove(repository: Path, paths: list[Path]) -> None:
    root = repository_root(repository)
    fs_py = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar').checkout_root() / 'modules-plugable' / 'computer' / 'memory' / 'filesystem' / 'services' / 'trash.py'
    for path in paths:
        named = in_repo(path, root)
        if not (root / named).exists() and (not _tracked(named, root)):
            raise PathAbsent(f'path does not exist and is not tracked: {path}')
        if (root / named).exists():
            completed = subprocess.run([sys.executable, str(fs_py), str(root / named)], check=False)
            if completed.returncode != 0:
                raise GitFailed(f'trashing {named} exited {completed.returncode}')
        run_git(['add', '-u', '--', named], root)
        print(f'removed (trashed + staged): {named}\nDo not use git rm — recovery from it is hard.', file=sys.stderr)

def _tracked(path: str, root: Path) -> bool:
    return run_captured(['ls-files', '--error-unmatch', path], cwd=root).returncode == 0

def describe(verbs):
    p_remove = verbs.add_parser('remove', help='trash working-tree path then git add -u (never git rm)', description='Stop tracking each PATH without deleting it: the file goes to the recycle\nbin, so it is still there if it turns out to be needed, and its\ndisappearance is staged.', formatter_class=argparse.RawDescriptionHelpFormatter)
    repository_flag(p_remove)
    p_remove.add_argument('paths', nargs='+', type=Path, help='paths to remove, relative to the repository or absolute')
    return guarded(lambda a: cmd_remove(a.repository, a.paths))
