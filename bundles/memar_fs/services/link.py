#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/memory/filesystem/services/link.py — directory symlink (junction on Windows)."""
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
from ._fs_common import ensure_dir_link
DESCRIPTION = 'modules-plugable/computer/memory/filesystem/services/link.py — directory link\n\nMake a directory symlink from LINK to TARGET. With --replace, trash LINK first if it\nalready exists and does not resolve to TARGET.\n'

def main() -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('link', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--replace', action='store_true', help='trash LINK first when it exists and is not already TARGET')
    args = parser.parse_args()
    ensure_dir_link(args.link, args.target, replace=args.replace)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
