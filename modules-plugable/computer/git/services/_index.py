#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""host/git_index.py — a private index to build a tree in, reading entries of a tree or an index, and the one write that gives the shared index a commit's entries.

Shared by `commit`, `reindex` and `record`. The private index is a file of its own in a folder of
its own under the repository's git folder, gone when the command ends, so two commands at once
never read or write one file.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

from host.git_lock import once, patiently, stopped, this_command
from host.git_run import plumb


def tree_entry(rev: str, path: str, root: Path) -> str:
    """`mode sha` of path in rev, or empty when rev does not hold it."""
    listed = plumb(["ls-tree", rev, "--", path], root)
    return listed.split("\t")[0].replace(" blob ", " ") if listed else ""


class PrivateIndex:
    """A throwaway index file of its own, made inside the repository's git folder and gone when the command ends.

    Two commands at once each get their own, so neither reads or writes the
    other's. The folder is removed by `tempfile`, not by this file.
    """

    def __init__(self, root: Path) -> None:
        git_dir = Path(plumb(["rev-parse", "--absolute-git-dir"], root))
        self._folder = tempfile.TemporaryDirectory(dir=git_dir, prefix="memar-host-index-", ignore_cleanup_errors=True)

    def __enter__(self) -> dict[str, str]:
        return dict(os.environ, GIT_INDEX_FILE=str(Path(self._folder.name) / "index"))

    def __exit__(self, *_: object) -> None:
        self._folder.cleanup()


def tree_entries(rev: str, paths: list[str], root: Path) -> dict[str, str]:
    """`mode sha` of each file under PATHS in REV, by path."""
    if not paths:
        return {}
    listed = plumb(["--literal-pathspecs", "ls-tree", "-r", "-z", rev, "--", *paths], root)
    entries = {}
    for record in filter(None, listed.split("\0")):
        meta, _, path = record.partition("\t")
        mode, _, sha = meta.split(" ")
        entries[path] = f"{mode} {sha}"
    return entries


def index_entries(paths: list[str], root: Path, env: dict | None = None) -> dict[str, str]:
    """`mode sha` of each entry under PATHS in the index ENV names, the shared one by default, by path."""
    if not paths:
        return {}
    listed = plumb(["--literal-pathspecs", "ls-files", "-s", "-z", "--", *paths], root, env=env)
    entries = {}
    for record in filter(None, listed.split("\0")):
        meta, _, path = record.partition("\t")
        mode, sha, _ = meta.split(" ")
        entries[path] = f"{mode} {sha}"
    return entries


def index_input(rev: str, paths: list[str], root: Path, env: dict | None = None) -> bytes:
    """`update-index -z --index-info` input giving PATHS REV's entries, and taking out each entry REV lacks."""
    want = tree_entries(rev, paths, root)
    zero = "0" * len(plumb(["rev-parse", rev], root))
    records = [f"{entry}\t{path}" for path, entry in want.items()]
    records += [f"0 {zero}\t{path}" for path in index_entries(paths, root, env) if path not in want]
    return "".join(f"{record}\0" for record in records).encode("utf-8")


def index_from(rev: str, was: str, paths: list[str], root: Path, reached: str, deadline: float) -> None:
    """Give PATHS in the shared index REV's entries, in one write; stop saying how to finish or undo when it cannot.

    One write, so the shared index holds either every path as it did before or
    every path as REV has them, never a mix. REACHED says where HEAD stands,
    for the message that stops; WAS is the commit HEAD was moved from.
    """
    if not paths:
        return
    done, lock = patiently(["update-index", "-z", "--index-info"], root, deadline, index_input(rev, paths, root))
    if done.returncode == 0:
        return
    named = ["--from", rev, "--was", was, "--", *paths]
    stopped(
        f"{reached}, but the shared index was not updated for the commit's {len(paths)} "
        f"path(s): {', '.join(paths)}. It holds them as it held them before this command, "
        "and the working tree is as it should be; until this is finished `git status` "
        "shows a staged difference for them.",
        f"To finish, {once(lock)}, run:\n    {this_command('reindex', '--repository', str(root), *named)}\n"
        f"To undo instead, moving HEAD back to {was[:12]} so it matches the shared index again:\n"
        f"    {this_command('reindex', '--repository', str(root), '--undo', *named)}",
        done,
        lock,
    )
