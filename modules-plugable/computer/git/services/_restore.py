#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_restore.py — `restore`: discard uncommitted changes to named paths, and only with an explicit token.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from host.git_run import in_repo, repository_flag, repository_root, run_git


DISCARD_CONFIRM = "DISCARD-UNCOMMITTED"


def cmd_restore(repository: Path, paths: list[Path], confirm: str | None) -> None:
    """Discard working-tree changes only with an explicit irreversible token."""
    if confirm != DISCARD_CONFIRM:
        sys.exit(
            "error: refusing to discard uncommitted work.\n"
            "To tidy status without losing WIP: commit, or run "
            "`git.py stash --repository PATH`.\n"
            "gitignore does not hide tracked modifications.\n"
            f"Irreversible discard requires --confirm {DISCARD_CONFIRM} "
            "(do not pass that casually)."
        )
    if not paths:
        sys.exit("error: restore requires one or more paths")
    root = repository_root(repository)
    named = [in_repo(p, root) for p in paths]
    # Match host `git restore --worktree --source=HEAD` for the named paths only.
    run_git(["restore", "--source=HEAD", "--worktree", "--"] + named, root)
    print(
        "discarded working-tree changes for the named paths "
        f"(confirmed {DISCARD_CONFIRM}).",
        file=sys.stderr,
    )


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_restore = sub.add_parser(
        "restore",
        help="refuse discard by default; needs --confirm DISCARD-UNCOMMITTED",
        description=(
            "Discard uncommitted changes to each PATH, and refuse unless --confirm is\n"
            "given: \"tidy the status\" is how uncommitted work is most often lost. If\n"
            "you want the work set aside, `stash` is the command for that."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repository_flag(p_restore)
    p_restore.add_argument("paths", nargs="+", type=Path, help="paths to discard changes of, relative to the repository or absolute")
    p_restore.add_argument(
        "--confirm",
        default=None,
        help=f"must be exactly {DISCARD_CONFIRM} to discard",
    )
    p_restore.set_defaults(run=lambda a: cmd_restore(a.repository, a.paths, a.confirm))
