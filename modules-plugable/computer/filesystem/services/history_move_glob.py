#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/filesystem/services/history_move_glob.py — git-mv every file matching a glob."""
from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path
_REPO = Path(__file__).resolve().parents[4]
if __package__ in (None, ''):
    for _folder in (_REPO, _REPO / 'bundles' / 'memar'):
        if str(_folder) not in sys.path:
            sys.path.insert(0, str(_folder))
    __package__ = 'modules-plugable.computer.filesystem.services'
from ._fs_common import host_git_cli
DESCRIPTION = 'modules-plugable/computer/filesystem/services/history_move_glob.py — history-preserving bulk move (git-mv-glob)\n\nMove every file matching PATTERN into DESTINATION through `git mv`. Default is dry-run;\npass --apply to execute, then commit renames by themselves afterwards.\n'

def cmd_git_mv_glob(pattern: str, destination: Path, *, apply: bool) -> None:
    destination = destination.resolve()
    if apply and (not destination.is_dir()):
        sys.exit(f'error: destination is not a directory: {destination}')
    matches = sorted(Path('.').glob(pattern))
    matches = [m for m in matches if m.is_file()]
    if not matches:
        sys.exit(f'error: no files match pattern: {pattern}')
    git_py = host_git_cli()
    for source in matches:
        dest = destination / source.name
        line = f'git mv {source} {dest}'
        if not apply:
            print(f'dry-run: {line}')
            continue
        completed = subprocess.run([sys.executable, str(git_py), 'rename', str(source), str(dest)], check=False)
        if completed.returncode != 0:
            sys.exit(completed.returncode)
    if not apply:
        print('dry-run only. Re-run with --apply to execute, then commit the renames by themselves before editing content.', file=sys.stderr)

def main() -> int:
    parser = argparse.ArgumentParser(description=DESCRIPTION, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('pattern', help='glob relative to cwd, e.g. "*.md"')
    parser.add_argument('destination', type=Path, help='destination directory (e.g. docs)')
    parser.add_argument('--apply', action='store_true', help='execute; without this flag, print dry-run lines only')
    args = parser.parse_args()
    cmd_git_mv_glob(args.pattern, args.destination, apply=args.apply)
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
