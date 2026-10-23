#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""computer/git/services/_staged.py — judging what is staged in the shared index and what is already published, before a verb moves HEAD.

Shared by `commit`, `uncommit` and `reindex`: the moves and removals `rename` and `remove` stage,
whether a rename still shows as one in the tree a commit writes, a staged change that is not the
verb's, and a commit already on the upstream.
"""
from __future__ import annotations
import sys
from pathlib import Path
from ._index import index_entries
from ._run import plumb, run_captured

def upstream_holding(commit: str, root: Path) -> str:
    """The upstream's commit when COMMIT is already on it, else empty: the published-history check."""
    upstream = run_captured(['rev-parse', '--verify', '--quiet', '@{upstream}'], cwd=root)
    if upstream.returncode != 0:
        return ''
    held = run_captured(['merge-base', '--is-ancestor', commit, upstream.stdout.strip()], cwd=root).returncode == 0
    return upstream.stdout.strip() if held else ''

def staged_moves(paths: list[str], root: Path, against: str='HEAD', prepared: dict[str, Path] | None=None) -> set[str]:
    """Both ends of each move, and each removal, staged for PATHS against AGAINST as `rename` and `remove` stage them.

    `rename` stages a `git mv` and asks for it to be committed. A staged move
    whose source and destination the caller both names is claimed by that
    naming, and so is an edit staged into its destination — any edit that
    keeps the file above git's rename threshold, which folds into the task's
    commit with the move even when another task staged it — so it is not the someone-else's staging
    `refuse_staged` guards against. What still makes it a move is git's own
    rename detection at its default threshold, here and, through
    `renames_lost`, in the tree the commit writes. Nor is a staged removal of
    a named path the working tree no longer has, which is what `remove`
    leaves: the commit records the absence either way.

    A destination PREPARED gives a file for counts only when that file is the
    very blob the move staged: it is how the move is committed alone once the
    destination has been edited in the working tree. A source or a removal
    given a file is never a move.
    """
    if not paths:
        return set()
    prepared = prepared or {}
    listed = run_captured(['diff', '--cached', '-M', '--name-status', '-z', against, '--', *paths], cwd=root).stdout.split('\x00')
    wanted, moved, at = (set(paths), set(), 0)
    while at < len(listed) and listed[at]:
        status = listed[at]
        if status.startswith(('R', 'C')):
            source, destination = (listed[at + 1], listed[at + 2])
            if status.startswith('R') and source in wanted and (source not in prepared) and (destination in wanted) and (destination not in prepared or _is_staged_blob(prepared[destination], destination, root)):
                moved.update((source, destination))
            at += 3
        else:
            path = listed[at + 1]
            if status == 'D' and path in wanted and (path not in prepared) and (not (root / path).exists()):
                moved.add(path)
            at += 2
    return moved

def _renames(args: list[str], root: Path) -> set[tuple[str, str]]:
    """The (source, destination) pairs a `--name-status -z` listing from git ARGS reports as renamed."""
    listed = run_captured([*args[:1], '--name-status', '-z', *args[1:]], cwd=root).stdout.split('\x00')
    pairs, at = (set(), 0)
    while at < len(listed) and listed[at]:
        if listed[at].startswith(('R', 'C')):
            if listed[at].startswith('R'):
                pairs.add((listed[at + 1], listed[at + 2]))
            at += 3
        else:
            at += 2
    return pairs

def renames_lost(moved: set[str], parent: str, tree: str, root: Path) -> list[str]:
    """Each staged move among MOVED that TREE, against PARENT, no longer shows as a rename.

    The commit takes a named file as the working tree has it, so an edit made
    after the move was staged rides with it too; the move survives only if git
    still pairs the two ends once that edit is in.
    """
    if not moved:
        return []
    staged = _renames(['diff', '--cached', '-M', 'HEAD', '--', *sorted(moved)], root)
    written = _renames(['diff-tree', '-r', '-M', parent, tree, '--', *sorted(moved)], root)
    return [f'{source} -> {destination}' for source, destination in sorted(staged - written)]

def _is_staged_blob(file: Path, path: str, root: Path) -> bool:
    """Whether FILE, cleaned as PATH would be, is the blob the shared index holds for PATH."""
    staged = index_entries([path], root).get(path, '')
    return plumb(['hash-object', '--path', path, str(file)], root) == staged.partition(' ')[2]

def refuse_staged(paths: list[str], root: Path, outcome: str) -> None:
    """Stop when any of PATHS holds a staged change HEAD does not: it is someone's, not this verb's."""
    for path in paths:
        if run_captured(['diff', '--cached', '--quiet', 'HEAD', '--', path], cwd=root).returncode:
            sys.exit(f"error: {path} has a staged change that HEAD does not hold — another task's, or yours from host git. {outcome} Commit or unstage it first; this verb will not decide whose it is.")
