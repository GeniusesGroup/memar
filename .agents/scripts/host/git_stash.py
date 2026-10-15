#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_stash.py — `stash`: park uncommitted work, tracked and untracked, so a later session can get it back.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from host.git_run import repository_flag, repository_root, run_captured, run_git


def _working_tree_dirty(root: Path) -> bool:
    """True when tracked or untracked-non-ignored paths differ from HEAD/index."""
    porcelain = run_captured(["status", "--porcelain", "--untracked-files=normal"], cwd=root)
    return bool(porcelain.stdout.strip())


def cmd_stash(repository: Path, message: str | None) -> None:
    """Park WIP recoverably. Does not include ignored files (use commit for those)."""
    root = repository_root(repository)
    if not _working_tree_dirty(root):
        print("nothing to stash", file=sys.stderr)
        return
    args = ["stash", "push", "--include-untracked"]
    if message:
        args.extend(["-m", message])
    run_git(args, root)
    print(
        "stashed tracked + untracked (not ignored).\n"
        "Recover with `git stash pop` / `git stash apply` when ready.\n"
        "Ignored paths were not included — commit those if they must survive.",
        file=sys.stderr,
    )


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_stash = sub.add_parser(
        "stash",
        help="stash tracked+untracked WIP (not ignored); prefer over discard",
        description="Set uncommitted work aside where a later session can get it back.",
    )
    repository_flag(p_stash)
    p_stash.add_argument(
        "-m",
        "--message",
        default=None,
        help="optional stash message",
    )
    p_stash.set_defaults(run=lambda a: cmd_stash(a.repository, a.message))
