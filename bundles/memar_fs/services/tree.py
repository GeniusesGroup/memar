#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from ..errors.errors import NotAFolder
from ._edge import guarded
LEFT_OUT = frozenset({'.git', '__pycache__', '.venv', 'node_modules'})

def tree(root: Path, dirs_only: bool=False) -> str:
    root = Path(root).resolve()
    if not root.is_dir():
        raise NotAFolder(f'not a folder: {root}')
    lines = [root.name]

    def walk(folder: Path, prefix: str) -> None:
        try:
            entries = sorted(folder.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        except OSError as error:
            print(f'{prefix}[error: {error}]', file=sys.stderr)
            return
        entries = [e for e in entries if e.name not in LEFT_OUT]
        for index, entry in enumerate(entries):
            last = index == len(entries) - 1
            branch = '`-- ' if last else '|-- '
            deeper = prefix + ('    ' if last else '|   ')
            if entry.is_dir():
                lines.append(f'{prefix}{branch}{entry.name}/')
                walk(entry, deeper)
            elif not dirs_only:
                lines.append(f'{prefix}{branch}{entry.name}')
    walk(root, '')
    return '\n'.join(lines)

def describe(verbs):
    parser = verbs.add_parser('tree', help='list a directory tree with ASCII branches', description='Lists a directory with ASCII box characters, similar intent to Windows `tree /F /A`.')
    parser.add_argument('root', nargs='?', type=Path, default=Path('.'), help='directory to list (default: .)')
    parser.add_argument('--dirs-only', action='store_true', help='list directories only')
    return guarded(lambda a: print(tree(a.root, dirs_only=a.dirs_only)))
