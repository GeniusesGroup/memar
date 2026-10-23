#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Shared helpers for path-invoked filesystem constraint scripts.

There is deliberately no command here that prints the operating system's
temporary directory. Task scratch has one home under the checkout; a command
whose output is that path invites the failure the rule exists to stop.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_trash = import_module('modules-plugable.computer.filesystem.services.fs_trash')
soft_delete = _m_fs_trash.soft_delete
import os
import subprocess
import sys
from pathlib import Path
PACKAGE = 'modules-plugable.computer.filesystem.services'

def bootstrap_repo() -> Path:
    """Put the checkout and launcher shelf on the path; return the repo root."""
    from importlib import import_module
    repo = Path(__file__).resolve().parents[4]
    launcher = import_module('modules-plugable.computer.filesystem.services.fs_memar').LAUNCHER_RELATIVE
    for folder in (repo, repo / launcher):
        if str(folder) not in sys.path:
            sys.path.insert(0, str(folder))
    return repo

def cmd_tree(root: Path, *, files: bool=True) -> None:
    root = root.resolve()
    if not root.is_dir():
        sys.exit(f'error: not a directory: {root}')
    print(root.name)

    def walk(directory: Path, prefix: str) -> None:
        try:
            entries = sorted(directory.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError as exc:
            print(f'{prefix}[error: {exc}]', file=sys.stderr)
            return
        entries = [e for e in entries if e.name not in {'.git', '__pycache__', '.venv', 'node_modules'}]
        for index, entry in enumerate(entries):
            last = index == len(entries) - 1
            branch = '`-- ' if last else '|-- '
            next_prefix = prefix + ('    ' if last else '|   ')
            if entry.is_dir():
                print(f'{prefix}{branch}{entry.name}/')
                walk(entry, next_prefix)
            elif files:
                print(f'{prefix}{branch}{entry.name}')
    walk(root, '')

def cmd_trash(paths: list[Path]) -> None:
    for path in paths:
        soft_delete(path)

def ensure_dir_link(link: Path, target: Path, *, replace: bool=False) -> None:
    target = target.resolve()
    if not target.is_dir():
        sys.exit(f'error: link target is not a directory: {target}')
    link = Path(link)
    if link.exists() or link.is_symlink():
        try:
            if link.resolve() == target:
                return
        except OSError:
            pass
        if not replace:
            sys.exit(f'error: {link} already exists')
        soft_delete(link)
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(str(target), str(link), target_is_directory=True)
    except OSError:
        if os.name != 'nt':
            raise
        completed = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            err = (completed.stderr or completed.stdout or '').strip()
            sys.exit(f'error: could not link {link} -> {target}\n{err}')
    print(f'linked {link} -> {target}', file=sys.stderr)

def host_git_cli() -> Path:
    return Path(__file__).resolve().parents[2] / 'git' / 'services' / '_host_git_cli.py'
