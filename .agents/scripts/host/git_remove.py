#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_remove.py — `remove`: trash a working-tree path and stage its disappearance, never `git rm`.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from host.git_run import in_repo, repository_flag, repository_root, run_captured, run_git


def cmd_remove(repository: Path, paths: list[Path]) -> None:
    root = repository_root(repository)
    fs_py = Path(__file__).resolve().parent / "fs.py"
    for path in paths:
        named = in_repo(path, root)
        if not (root / named).exists() and not _tracked(named, root):
            sys.exit(f"error: path does not exist and is not tracked: {path}")
        if (root / named).exists():
            completed = subprocess.run(
                [sys.executable, str(fs_py), "trash", str(root / named)],
                check=False,
            )
            if completed.returncode != 0:
                sys.exit(completed.returncode)
        # Stage the working-tree deletion without git rm.
        run_git(["add", "-u", "--", named], root)
        print(
            f"removed (trashed + staged): {named}\n"
            "Do not use git rm — recovery from it is hard.",
            file=sys.stderr,
        )


def _tracked(path: str, root: Path) -> bool:
    return run_captured(["ls-files", "--error-unmatch", path], cwd=root).returncode == 0


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_remove = sub.add_parser(
        "remove",
        help="trash working-tree path then git add -u (never git rm)",
        description=(
            "Stop tracking each PATH without deleting it: the file goes to the recycle\n"
            "bin, so it is still there if it turns out to be needed, and its\n"
            "disappearance is staged."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repository_flag(p_remove)
    p_remove.add_argument("paths", nargs="+", type=Path, help="paths to remove, relative to the repository or absolute")
    p_remove.set_defaults(run=lambda a: cmd_remove(a.repository, a.paths))
