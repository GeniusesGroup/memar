#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_reindex.py — `reindex`: finish, or undo, a commit or uncommit that moved HEAD but could not write the shared index.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from host.git_index import index_entries, index_from, tree_entries
from host.git_lock import lock_deadline, once, patiently, stopped
from host.git_run import in_repo, plumb, repository_flag, repository_root
from host.git_staged import staged_moves


def cmd_reindex(repository: Path, paths: list[Path], source: str, was: str, undo: bool) -> None:
    """Finish a commit or uncommit that moved HEAD but stopped before the shared index, or with UNDO take its move back.

    Finishing gives PATHS SOURCE's entries, and only while HEAD holds them as
    SOURCE does; undoing moves HEAD from SOURCE back to WAS, and only while HEAD
    is SOURCE and the shared index still holds them as before the command. That
    is WAS's entries, except where a commit took a move or removal staged
    against WAS, which the index still holds as staged. Either way a path
    staged otherwise is refused, so nothing someone staged since is overwritten
    or left against the wrong HEAD.
    """
    root = repository_root(repository)
    deadline = lock_deadline()
    rev = plumb(["rev-parse", "--verify", f"{source}^{{commit}}"], root)
    old = plumb(["rev-parse", "--verify", f"{was}^{{commit}}"], root)
    named = [in_repo(path, root) for path in paths]
    have, want, then = index_entries(named, root), tree_entries(rev, named, root), tree_entries(old, named, root)
    uncommitted = rev in plumb(["rev-list", "--parents", "-n", "1", old], root).split()[1:]
    staged = set() if uncommitted else staged_moves(named, root, old)
    for path in sorted({*have, *want, *then} - staged):
        if have.get(path) not in (want.get(path), then.get(path)):
            sys.exit(
                f"error: {path} is staged as neither {rev[:12]} nor {old[:12]} has it — "
                "another session's, or yours from host git. Nothing was changed. Commit "
                "or unstage it first; this verb will not decide whose it is."
            )
    head = plumb(["rev-parse", "HEAD"], root)
    if undo:
        if head != rev:
            sys.exit(
                f"error: HEAD is {head[:12]}, not {rev[:12]}: it has moved since, so it is "
                f"not moved back to {old[:12]}. Nothing was changed."
            )
        if any(have.get(path) != then.get(path) for path in named if path not in staged):
            sys.exit(
                f"error: the shared index no longer holds these paths as {old[:12]} has "
                f"them — it was finished, or they were staged since — so HEAD is not moved "
                f"back to {old[:12]}. Nothing was changed."
            )
        moved, lock = patiently(["update-ref", "-m", "host/git.py reindex --undo", "HEAD", old, rev], root, deadline)
        if moved.returncode != 0:
            stopped(
                f"nothing was changed: HEAD is still {rev}.",
                f"{once(lock).capitalize()}, rerun the same command.",
                moved,
                lock,
            )
        print(
            f"moved HEAD from {rev[:12]} back to {old[:12]}; the shared index was not touched, "
            f"and holds the {len(named)} named path(s) as it did before {rev[:12]} was made "
            f"HEAD. {rev[:12]} stays in git reflog.",
            file=sys.stderr,
        )
        return
    if tree_entries("HEAD", named, root) != want:
        sys.exit(
            f"error: HEAD is {head[:12]}, which does not hold these paths as {rev[:12]} "
            "does: it has moved since, so the shared index is not given them. Nothing "
            "was changed."
        )
    index_from(rev, old, named, root, f"HEAD is {head}", deadline)
    print(
        f"the shared index holds the {len(named)} named path(s) as {rev[:12]} has them; "
        "nothing else in it was touched.",
        file=sys.stderr,
    )


def add_parser(sub: argparse._SubParsersAction) -> None:
    """Declare this verb on the command's subparsers."""
    p_reindex = sub.add_parser(
        "reindex",
        help="finish, or undo, a commit or uncommit that moved HEAD but could not update the shared index",
        description=(
            "Give the named paths, in the shared index, the entries the commit --from has,\n"
            "in one write, and touch nothing else in it. This is the last step of `commit`\n"
            "and `uncommit`; when another git process holds the index lock past the wait,\n"
            "they stop after moving HEAD and print this command, and its --undo, with their\n"
            "arguments filled in. Finishing is refused once HEAD no longer holds the paths\n"
            "as --from does; --undo moves HEAD from --from back to --was instead, and is\n"
            "refused once HEAD is not --from or the index no longer holds the paths as it\n"
            "did before the command. A path staged as neither --from nor --was has it, and\n"
            "not as a move or removal the commit took, is refused either way: someone\n"
            "staged it since."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repository_flag(p_reindex)
    p_reindex.add_argument("paths", nargs="+", type=Path, help="the commit's paths, as the stopped command printed them")
    p_reindex.add_argument(
        "--from",
        dest="source",
        required=True,
        metavar="REV",
        help="the commit HEAD was moved to",
    )
    p_reindex.add_argument(
        "--was",
        required=True,
        metavar="REV",
        help="the commit HEAD was moved from",
    )
    p_reindex.add_argument(
        "--undo",
        action="store_true",
        help="move HEAD from --from back to --was, leaving the shared index as it is",
    )
    p_reindex.set_defaults(run=lambda a: cmd_reindex(a.repository, a.paths, a.source, a.was, a.undo))
