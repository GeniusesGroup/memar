#!/usr/bin/env python3
"""host/fs.py — a filesystem operation with the constraint a session keeps violating.

**Two audiences, two texts, and this file is where each lives.** `DESCRIPTION`
below is what `--help` prints, and the per-verb `help=` strings beside each
argument are what `fs.py <verb> --help` prints. Both are addressed to whoever is
about to run one of these — usually an agent that has just been about to do the
unconstrained thing. Everything from here down is addressed to whoever opens this
file.

The host tool already lists and deletes files; this file is the constraint, not
the capability. Three of them, each against a habit free-form shell habits form:

  tree        List a directory tree with ASCII box characters (agent-log
              friendly), similar intent to Windows `tree /F /A`.

  git-mv-glob Move every path matching a glob into a destination directory
              via `git mv` (history-preserving). Default is dry-run; pass
              --apply to execute. Commit renames by themselves afterwards.

  trash       Move a path to the OS recycle bin / Trash — never permanent
              delete. Agents that "deep delete" then need the file again burn
              tokens reconstructing it; trash keeps recovery cheap.

  link        Make a directory symlink (a junction on Windows) from LINK
              to TARGET. With --replace, trash LINK first if it already
              exists and does not already resolve to TARGET.

There is deliberately no command here that prints the operating system's
temporary directory. Session scratch has one home, `<memar-root>/temp/`, and it
is reached through the session tool; an OS temp directory is wiped by other
applications while sessions last days. A command whose output is the path the
scratch rule forbids is a command that invites the failure the rule exists to
stop, so the absence is the constraint.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from machine.fs_trash import soft_delete

DESCRIPTION = """host/fs.py — filesystem operations that are safe to undo

The operating system already lists and deletes files. These are the same
operations with the constraint a session keeps wanting to skip:

  tree          list a directory tree, as ASCII branches
  git-mv-glob   move matching paths into a folder, through git so history follows
  trash         move a path to the recycle bin instead of deleting it
  link          make a directory link

`trash` exists because a delete you cannot undo is a delete you cannot take
back: if the file turns out to be needed, the recycle bin still has it.
`git-mv-glob` prints what it would move and does nothing until you pass
`--apply`, so a mistaken glob is visible before it is real.

There is no command here that prints the OS temporary directory. Session scratch
belongs in your session folder — run `memar session new` and work there.
"""


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
        soft_delete(path)


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
        soft_delete(link)
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
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
    elif args.command == "link":
        ensure_dir_link(args.link, args.target, replace=args.replace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
