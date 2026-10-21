#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/filesystem/services/trash.py — move path(s) to OS Recycle Bin / Trash."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
_REPO = Path(__file__).resolve().parents[4]
if __package__ in (None, ''):
    for _folder in (_REPO, _REPO / 'bundles' / 'memar'):
        if str(_folder) not in sys.path:
            sys.path.insert(0, str(_folder))
    __package__ = 'modules-plugable.computer.filesystem.services'
from ._fs_common import cmd_trash
DESCRIPTION = 'modules-plugable/computer/filesystem/services/trash.py — recoverable delete\n\nMove each PATH to the OS recycle bin / Trash instead of deleting it permanently.\n'

def main() -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('paths', nargs='+', type=Path)
    args = parser.parse_args()
    cmd_trash(args.paths)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
