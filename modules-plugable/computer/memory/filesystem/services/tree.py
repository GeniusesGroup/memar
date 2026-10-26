#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/memory/filesystem/services/tree.py — list a directory tree with ASCII branches."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
_REPO = next(p for p in Path(__file__).resolve().parents if p.name == 'modules-plugable').parent
if __package__ in (None, ''):
    for _folder in (_REPO, _REPO / 'bundles' / 'memar'):
        if str(_folder) not in sys.path:
            sys.path.insert(0, str(_folder))
    __package__ = 'modules-plugable.computer.memory.filesystem.services'
from ._fs_common import cmd_tree
DESCRIPTION = 'modules-plugable/computer/memory/filesystem/services/tree.py — directory tree (agent-log friendly)\n\nLists a directory with ASCII box characters, similar intent to Windows `tree /F /A`.\n'

def main() -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('root', nargs='?', type=Path, default=Path('.'), help='directory to list (default: .)')
    parser.add_argument('--dirs-only', action='store_true', help='list directories only')
    args = parser.parse_args()
    cmd_tree(args.root, files=not args.dirs_only)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
