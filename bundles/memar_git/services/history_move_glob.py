#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path, PurePath
from ..errors.errors import MoveFailed, NoMatch, NotAFolder, PatternMalformed
from ._edge import guarded

def history_move_glob(pattern: str, destination: Path, apply: bool=False) -> str:
    if not pattern or PurePath(pattern).is_absolute() or Path(pattern).drive:
        raise PatternMalformed(f'the pattern must be a non-empty glob relative to the current folder: {pattern!r}')
    destination = Path(destination).resolve()
    if apply and (not destination.is_dir()):
        raise NotAFolder(f'destination is not a folder: {destination}')
    matches = [m for m in sorted(Path('.').glob(pattern)) if m.is_file()]
    if not matches:
        raise NoMatch(f'no files match pattern: {pattern}')
    lines = []
    for source in matches:
        target = destination / source.name
        lines.append(f'git mv {source} {target}')
        if apply:
            completed = subprocess.run(['git', 'mv', str(source), str(target)], check=False, capture_output=True, text=True)
            if completed.returncode != 0:
                raise MoveFailed(f'git mv {source} {target} exited {completed.returncode}: {completed.stderr.strip()}')
    if not apply:
        lines = [f'dry-run: {line}' for line in lines]
        print('dry-run only. Re-run with --apply to execute, then commit the renames by themselves before editing content.', file=sys.stderr)
    return '\n'.join(lines)

def describe(verbs):
    parser = verbs.add_parser('history-move-glob', help='git mv every file matching a glob, keeping history; lists only unless applied', description='Move every file matching PATTERN into DESTINATION through `git mv`. Default is dry-run;\npass --apply to execute, then commit renames by themselves afterwards.', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('pattern', help='glob relative to cwd, e.g. "*.md"')
    parser.add_argument('destination', type=Path, help='destination directory (e.g. docs)')
    parser.add_argument('--apply', action='store_true', help='execute; without this flag, print dry-run lines only')
    return guarded(lambda a: print(history_move_glob(a.pattern, a.destination, apply=a.apply)))
