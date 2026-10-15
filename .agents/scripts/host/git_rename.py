#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_rename.py — `rename`: move a tracked path with `git mv` so history follows it.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from host.git_run import in_repo, repository_flag, repository_root, run_git


def cmd_rename(repository: Path, source: Path, destination: Path) -> None:
    root = repository_root(repository)
    named_source = in_repo(source, root)
    named_destination = in_repo(destination, root)
    if not (root / named_source).exists():
        sys.exit(f"error: source does not exist: {source}")
    run_git(["mv", named_source, named_destination], root)
    print(
        f"renamed (index): {named_source} -> {named_destination}\n"
        "The rename rides with the task's commit while git still detects it\n"
        "as a rename; an edit that breaks detection needs the rename committed first.",
        file=sys.stderr,
    )


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_rename = sub.add_parser(
        "rename",
        help="git mv for a tracked path; the rename rides with the task's commit",
        description="Move a tracked file or folder with `git mv`, so history follows it.",
    )
    repository_flag(p_rename)
    p_rename.add_argument("source", type=Path, help="the tracked path to move, relative to the repository or absolute")
    p_rename.add_argument("destination", type=Path, help="where it goes, relative to the repository or absolute")
    p_rename.set_defaults(run=lambda a: cmd_rename(a.repository, a.source, a.destination))
