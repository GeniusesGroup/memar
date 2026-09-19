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

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path


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


def _trash_windows(path: Path) -> None:
    # SHFileOperationW with FOF_ALLOWUNDO sends to Recycle Bin.
    import ctypes
    from ctypes import wintypes

    FO_DELETE = 3
    FOF_ALLOWUNDO = 0x40
    FOF_NOCONFIRMATION = 0x10
    FOF_NOERRORUI = 0x400
    FOF_SILENT = 0x04

    class SHFILEOPSTRUCTW(ctypes.Structure):
        _fields_ = [
            ("hwnd", wintypes.HWND),
            ("wFunc", ctypes.c_uint),
            ("pFrom", wintypes.LPCWSTR),
            ("pTo", wintypes.LPCWSTR),
            ("fFlags", ctypes.c_ushort),
            ("fAnyOperationsAborted", wintypes.BOOL),
            ("hNameMappings", wintypes.LPVOID),
            ("lpszProgressTitle", wintypes.LPCWSTR),
        ]

    # Double-null-terminated path list required by SHFileOperation.
    from_path = str(path.resolve()) + "\0\0"
    op = SHFILEOPSTRUCTW()
    op.hwnd = None
    op.wFunc = FO_DELETE
    op.pFrom = from_path
    op.pTo = None
    op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_NOERRORUI | FOF_SILENT
    op.fAnyOperationsAborted = False
    op.hNameMappings = None
    op.lpszProgressTitle = None
    result = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(op))
    if result != 0 or op.fAnyOperationsAborted:
        sys.exit(f"error: Recycle Bin move failed (code {result}): {path}")


def _trash_darwin(path: Path) -> None:
    posix = str(path.resolve())
    script = f'tell application "Finder" to delete POSIX file "{posix}"'
    completed = subprocess.run(
        ["osascript", "-e", script],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        sys.exit(
            f"error: Trash move failed: {path}\n{completed.stderr.strip()}"
        )


def _trash_xdg(path: Path) -> None:
    # Prefer desktop tools that register in Trash correctly.
    for cmd in (
        ["gio", "trash", str(path)],
        ["trash-put", str(path)],
    ):
        if shutil.which(cmd[0]):
            completed = subprocess.run(cmd, check=False)
            if completed.returncode == 0:
                return
            sys.exit(f"error: {' '.join(cmd)} failed for {path}")

    # Minimal FreeDesktop Trash fallback.
    home = Path.home()
    trash = home / ".local" / "share" / "Trash"
    files_dir = trash / "files"
    info_dir = trash / "info"
    files_dir.mkdir(parents=True, exist_ok=True)
    info_dir.mkdir(parents=True, exist_ok=True)
    resolved = path.resolve()
    dest_name = resolved.name
    dest = files_dir / dest_name
    if dest.exists():
        dest = files_dir / f"{resolved.stem}-{int(time.time())}{resolved.suffix}"
    shutil.move(str(resolved), str(dest))
    info = info_dir / (dest.name + ".trashinfo")
    deletion_date = time.strftime("%Y-%m-%dT%H:%M:%S")
    info.write_text(
        "[Trash Info]\n"
        f"Path={resolved}\n"
        f"DeletionDate={deletion_date}\n",
        encoding="utf-8",
    )


def soft_delete(path: Path) -> None:
    path = path.resolve()
    if not path.exists():
        sys.exit(f"error: path does not exist: {path}")
    if os.name == "nt":
        _trash_windows(path)
    elif sys.platform == "darwin":
        _trash_darwin(path)
    else:
        _trash_xdg(path)
    print(f"trashed (recoverable): {path}", file=sys.stderr)


def cmd_trash(paths: list[Path]) -> None:
    for path in paths:
        soft_delete(path)


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

    args = parser.parse_args()
    if args.command == "tree":
        cmd_tree(args.root, files=not args.dirs_only)
    elif args.command == "git-mv-glob":
        cmd_git_mv_glob(args.pattern, args.destination, apply=args.apply)
    elif args.command == "trash":
        cmd_trash(args.paths)


if __name__ == "__main__":
    main()
