#!/usr/bin/env python3
"""Memar-constrained filesystem helpers.

Host tools already list and delete files. This script exists for the
constraints Memar sessions keep violating when they improvise:

  tree        List a directory tree with ASCII box characters (agent-log
              friendly), similar intent to Windows `tree /F /A`.

  git-mv-glob Move every path matching a glob into a destination directory
              via `git mv` (history-preserving). Default is dry-run; pass
              --apply to execute. Commit renames by themselves afterwards.

  trash       Move a path to the OS recycle bin / Trash — never permanent
              delete. Agents that "deep delete" then need the file again burn
              tokens reconstructing it; trash keeps recovery cheap.

  temp        Print the process temp directory, optionally joined with
              extra path parts. Scratch space only: Memar itself lives at its
              permanent install location, never under temp.

  link        Make a directory symlink (a junction on Windows) from LINK
              to TARGET. With --replace, trash LINK first if it already
              exists and does not already resolve to TARGET.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import sys_fs_trash


def canonical_temp(*parts: str) -> Path:
    return Path(tempfile.gettempdir()).joinpath(*parts)


def cmd_tree(root: Path, *, files: bool = True) -> None:
    root = root.resolve()
    if not root.is_dir():
        sys.exit(f"error: not a directory: {root}")
    print(root.name)

    def walk(directory: Path, prefix: str) -> None:
        try:
            entries = sorted(
                directory.iterdir(),
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except OSError as exc:
            print(f"{prefix}[error: {exc}]", file=sys.stderr)
            return
        # Skip noise that agents rarely want in a structural listing.
        entries = [
            e
            for e in entries
            if e.name not in {".git", "__pycache__", ".venv", "node_modules"}
        ]
        for index, entry in enumerate(entries):
            last = index == len(entries) - 1
            branch = "`-- " if last else "|-- "
            next_prefix = prefix + ("    " if last else "|   ")
            if entry.is_dir():
                print(f"{prefix}{branch}{entry.name}/")
                walk(entry, next_prefix)
            elif files:
                print(f"{prefix}{branch}{entry.name}")

    walk(root, "")


def cmd_git_mv_glob(pattern: str, destination: Path, *, apply: bool) -> None:
    destination = destination.resolve()
    if apply and not destination.is_dir():
        sys.exit(f"error: destination is not a directory: {destination}")
    matches = sorted(Path(".").glob(pattern))
    matches = [m for m in matches if m.is_file()]
    if not matches:
        sys.exit(f"error: no files match pattern: {pattern}")
    git_py = Path(__file__).resolve().parent / "git.py"
    for source in matches:
        dest = destination / source.name
        line = f"git mv {source} {dest}"
        if not apply:
            print(f"dry-run: {line}")
            continue
        completed = subprocess.run(
            [sys.executable, str(git_py), "rename", str(source), str(dest)],
            check=False,
        )
        if completed.returncode != 0:
            sys.exit(completed.returncode)
    if not apply:
        print(
            "dry-run only. Re-run with --apply to execute, then commit the "
            "renames by themselves before editing content.",
            file=sys.stderr,
        )


def cmd_trash(paths: list[Path]) -> None:
    for path in paths:
        sys_fs_trash.soft_delete(path)


def ensure_dir_link(link: Path, target: Path, *, replace: bool = False) -> None:
    target = target.resolve()
    if not target.is_dir():
        sys.exit(f"error: link target is not a directory: {target}")
    link = Path(link)
    if link.exists() or link.is_symlink():
        try:
            if link.resolve() == target:
                return
        except OSError:
            pass
        if not replace:
            sys.exit(f"error: {link} already exists")
        sys_fs_trash.soft_delete(link)
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(str(target), str(link), target_is_directory=True)
    except OSError:
        if os.name != "nt":
            raise
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            err = (completed.stderr or completed.stdout or "").strip()
            sys.exit(f"error: could not link {link} -> {target}\n{err}")
    print(f"linked {link} -> {target}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_tree = sub.add_parser(
        "tree",
        help="list directory tree with ASCII branches (files included by default)",
    )
    p_tree.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path("."),
        help="directory to list (default: .)",
    )
    p_tree.add_argument(
        "--dirs-only",
        action="store_true",
        help="list directories only",
    )

    p_glob = sub.add_parser(
        "git-mv-glob",
        help="git-mv every file matching a glob into a destination directory",
    )
    p_glob.add_argument(
        "pattern",
        help='glob relative to cwd, e.g. "*.md"',
    )
    p_glob.add_argument(
        "destination",
        type=Path,
        help="destination directory (e.g. docs)",
    )
    p_glob.add_argument(
        "--apply",
        action="store_true",
        help="execute; without this flag, print dry-run lines only",
    )

    p_trash = sub.add_parser(
        "trash",
        help="move path(s) to OS Recycle Bin / Trash (never permanent delete)",
    )
    p_trash.add_argument("paths", nargs="+", type=Path)

    p_temp = sub.add_parser(
        "temp",
        help="print tempfile.gettempdir(), optionally joined with names",
    )
    p_temp.add_argument(
        "parts",
        nargs="*",
        help="path parts under the temp directory (e.g. work)",
    )

    p_link = sub.add_parser(
        "link",
        help="directory symlink (junction on Windows) from LINK to TARGET",
    )
    p_link.add_argument("link", type=Path)
    p_link.add_argument("target", type=Path)
    p_link.add_argument(
        "--replace",
        action="store_true",
        help="trash LINK first when it exists and is not already TARGET",
    )

    args = parser.parse_args()
    if args.command == "tree":
        cmd_tree(args.root, files=not args.dirs_only)
    elif args.command == "git-mv-glob":
        cmd_git_mv_glob(args.pattern, args.destination, apply=args.apply)
    elif args.command == "trash":
        cmd_trash(args.paths)
    elif args.command == "temp":
        print(canonical_temp(*args.parts))
    elif args.command == "link":
        ensure_dir_link(args.link, args.target, replace=args.replace)


if __name__ == "__main__":
    main()
