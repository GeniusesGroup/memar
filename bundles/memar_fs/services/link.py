#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import os
import subprocess
import sys
from importlib import import_module
from pathlib import Path
from ..errors.errors import LinkExists, LinkFailed, NotAFolder, TrashFailed
from ._edge import guarded
_m_fs_trash = import_module('bundles.memar_fs.services.fs_trash')

def link(place: Path, target: Path, replace: bool=False) -> None:
    target = Path(target).resolve()
    if not target.is_dir():
        raise NotAFolder(f'link target is not a folder: {target}')
    place = Path(place)
    if place.exists() or place.is_symlink():
        try:
            if place.resolve() == target:
                return
        except OSError:
            pass
        if not replace:
            raise LinkExists(f'{place} already exists')
        try:
            _m_fs_trash.soft_delete(place)
        except SystemExit as stopped:
            raise TrashFailed(str(stopped.code)) from None
    place.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(str(target), str(place), target_is_directory=True)
    except OSError:
        if os.name != 'nt':
            raise
        completed = subprocess.run(['cmd', '/c', 'mklink', '/J', str(place), str(target)], check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout or '').strip()
            raise LinkFailed(f'could not link {place} -> {target}: {detail}') from None
    print(f'linked {place} -> {target}', file=sys.stderr)

def describe(verbs):
    parser = verbs.add_parser('link', help='make a directory link from a place to a target folder', description='Make a directory symlink from LINK to TARGET. With --replace, trash LINK first if it already exists and does not resolve to TARGET.')
    parser.add_argument('link', type=Path)
    parser.add_argument('target', type=Path)
    parser.add_argument('--replace', action='store_true', help='trash LINK first when it exists and is not already TARGET')
    return guarded(lambda a: link(a.link, a.target, replace=a.replace))
