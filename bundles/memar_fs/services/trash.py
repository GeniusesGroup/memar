#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import os
from importlib import import_module
from pathlib import Path
from ..errors.errors import PathAbsent, TrashFailed
from ._edge import guarded
_m_fs_trash = import_module('bundles.memar_fs.services.fs_trash')

def trash(paths) -> None:
    for path in paths:
        named = Path(os.path.abspath(str(path)))
        if not os.path.lexists(named):
            raise PathAbsent(f'path does not exist: {named}')
        try:
            _m_fs_trash.soft_delete(named)
        except SystemExit as stopped:
            raise TrashFailed(str(stopped.code)) from None

def describe(verbs):
    parser = verbs.add_parser('trash', help='move paths to the recycle bin, never delete them', description='Move each PATH to the OS recycle bin / Trash instead of deleting it permanently.')
    parser.add_argument('paths', nargs='+', type=Path)
    return guarded(lambda a: trash(a.paths))
