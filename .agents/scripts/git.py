#!/usr/bin/env python3
"""Memar-constrained git helpers.

Host tools already speak git. This script exists only for the constraints
Memar sessions keep violating when they improvise:

  rename   Move/rename a *tracked* path with `git mv`, never plain mv.
           Commit that rename by itself before editing content — a mixed
           rename+edit commit defeats rename detection and orphans history.

  remove   Stop tracking a path without `git rm`. `git rm` deletes in a way
           that is hard to recover from. This command sends the working-tree
           path to the OS Recycle Bin / Trash via fs.py trash, then stages
           the disappearance with `git add -u` so the index matches.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
Do not use `git rm` in Memar sessions. Document-ID minting is not here —
use memar-doc.py hour-id.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str]) -> None:
    completed = subprocess.run(["git", *args], check=False)
    if completed.returncode != 0:
        sys.exit(completed.returncode)


def cmd_rename(source: Path, destination: Path) -> None:
    if not source.exists():
        sys.exit(f"error: source does not exist: {source}")
    run_git(["mv", str(source), str(destination)])
    print(
        f"renamed (index): {source} -> {destination}\n"
        "Commit this rename by itself before editing content.",
        file=sys.stderr,
    )


def cmd_remove(paths: list[Path]) -> None:
    fs_py = Path(__file__).resolve().parent / "fs.py"
    for path in paths:
        if not path.exists() and not _tracked(path):
            sys.exit(f"error: path does not exist and is not tracked: {path}")
        if path.exists():
            completed = subprocess.run(
                [sys.executable, str(fs_py), "trash", str(path)],
                check=False,
            )
            if completed.returncode != 0:
                sys.exit(completed.returncode)
        # Stage the working-tree deletion without git rm.
        run_git(["add", "-u", "--", str(path)])
        print(
            f"removed (trashed + staged): {path}\n"
            "Do not use git rm — recovery from it is hard.",
            file=sys.stderr,
        )


def _tracked(path: Path) -> bool:
    completed = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)],
        check=False,
        capture_output=True,
    )
    return completed.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_rename = sub.add_parser(
        "rename",
        help="git mv for a tracked path; commit the rename alone afterwards",
    )
    p_rename.add_argument("source", type=Path)
    p_rename.add_argument("destination", type=Path)

    p_remove = sub.add_parser(
        "remove",
        help="trash working-tree path then git add -u (never git rm)",
    )
    p_remove.add_argument("paths", nargs="+", type=Path)

    args = parser.parse_args()
    if args.command == "rename":
        cmd_rename(args.source, args.destination)
    elif args.command == "remove":
        cmd_remove(args.paths)


if __name__ == "__main__":
    main()
