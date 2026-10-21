#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_uncommit.py — `uncommit`: take back the last unpushed commit, keeping its work in the tree.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from host.git_index import index_from
from host.git_lock import LOCK_NOTE, lock_deadline, locks_free, once, patiently, shared_locks, stopped
from host.git_run import plumb, repository_flag, repository_root
from host.git_staged import refuse_staged, upstream_holding


# A commit id as `git log` prints it, whole or abbreviated: `--expect` is the
# caller saying which commit it means, and a name like HEAD would say nothing.
COMMIT_ID = re.compile(r"[0-9a-f]{7,40}")


def cmd_uncommit(repository: Path, expect: str) -> None:
    """Move HEAD back to its parent, the commit's work kept in the tree and others' staging in the index."""
    root = repository_root(repository)
    expected = expect.lower()
    if not COMMIT_ID.fullmatch(expected):
        sys.exit(f"error: --expect takes the commit's id as `git log` prints it, not {expect!r}")
    head = plumb(["rev-parse", "HEAD"], root)
    if not head.startswith(expected):
        sys.exit(f"error: HEAD is {head[:12]}, not {expect}; nothing was changed")
    parents = plumb(["rev-list", "--parents", "-n", "1", head], root).split()[1:]
    if len(parents) != 1:
        sys.exit(
            f"error: {head[:12]} has {len(parents)} parents; this takes back only a commit "
            "with exactly one"
        )
    parent = parents[0]
    upstream = upstream_holding(head, root)
    if upstream:
        sys.exit(
            f"error: {head[:12]} is already on {upstream[:12]} upstream; "
            "taking it back would rewrite published history"
        )
    listed = plumb(["diff-tree", "-r", "--no-renames", "--name-only", "-z", parent, head], root)
    changed = [path for path in listed.split("\0") if path]
    refuse_staged(changed, root, "Nothing was changed.")

    unchanged = f"nothing was changed: HEAD is still {head}, and the shared index and the working tree are as they were."
    deadline = lock_deadline()
    lock = locks_free(shared_locks(root), "moving HEAD", deadline)
    if lock is not None:
        stopped(unchanged, f"{once(lock).capitalize()}, rerun the same command.", lock=lock)
    moved, lock = patiently(["update-ref", "-m", "host/git.py uncommit", "HEAD", parent, head], root, deadline)
    if moved.returncode != 0:
        stopped(unchanged, f"{once(lock).capitalize()}, rerun the same command.", moved, lock)
    index_from(parent, head, changed, root, f"HEAD moved from {head} back to its parent {parent}", deadline)

    print(parent)
    print(plumb(["diff", "--stat", parent, head], root), file=sys.stderr)
    print(
        f"took back {head[:12]}; HEAD is {parent[:12]}. Its changes are in the working "
        f"tree, unstaged; the shared index was reset for its {len(changed)} path(s) "
        "only, and whatever else was staged is still staged.\n"
        f"It is recoverable from git reflog as {head}: `git update-ref HEAD {head} "
        f"{parent}` puts it back, and `git reset -q {head} -- PATH...` its paths' index entries.",
        file=sys.stderr,
    )


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_uncommit = sub.add_parser(
        "uncommit",
        help="take back the last unpushed commit; its changes stay in the tree, others' staging stays staged",
        description=(
            "Move HEAD back to the parent of the commit you name, which must be HEAD,\n"
            "have one parent, and not be upstream yet. The working tree is left as it\n"
            "is, so the commit's changes show as unstaged edits; in the shared index\n"
            "only that commit's paths go back to the parent, and anything else staged\n"
            "stays staged. A path of the commit holding a staged change of its own is\n"
            "refused. The commit stays recoverable from git reflog, and the command\n"
            "prints how to put it back. It asks for the commit's id, so it never takes\n"
            "back one you did not mean.\n\n"
            f"{LOCK_NOTE}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repository_flag(p_uncommit)
    p_uncommit.add_argument(
        "--expect",
        required=True,
        metavar="SHA",
        help="the id of the commit to take back, as git log prints it; refused unless it is HEAD",
    )
    p_uncommit.set_defaults(run=lambda a: cmd_uncommit(a.repository, a.expect))
