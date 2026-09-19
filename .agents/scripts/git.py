#!/usr/bin/env python3
"""Memar-constrained git helpers.

Host tools already speak git. This script exists only for the constraints
Memar sessions keep violating when they improvise:

  rename   Move/rename a *tracked* path with `git mv`, never plain mv.
           Commit that rename by itself before editing content — a mixed
           rename+edit commit defeats rename detection and orphans history.

  remove   Stop tracking a path without `git rm`. `git rm` deletes in a way
           that is hard to recover from. This command sends the working-tree
           path to the OS Recycle Bin / Trash via fs.py trash, then stages
           the disappearance with `git add -u` so the index matches.

  ensure   Make `git` usable in this process. If it is missing from PATH,
           try to install it with the environment's package manager
           (winget/choco/scoop, brew, apt/dnf/pacman/apk) and refresh
           common Git install locations on PATH. Other Memar scripts that
           need git call this instead of failing immediately.

This script needs git. If git is not already present, `ensure` tries to
install it in the current environment rather than asking the caller to
stop. Usage is the interface. Do not duplicate these recipes as prose
catalogs. Do not use `git rm` in Memar sessions. Document-ID minting is
not here — use memar-doc.py hour-id.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run_git(args: list[str]) -> None:
    completed = subprocess.run(["git", *args], check=False)
    if completed.returncode != 0:
        sys.exit(completed.returncode)


def run_captured(
    args: list[str], cwd: Path | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _git_extra_dirs() -> list[Path]:
    if os.name == "nt":
        return [
            Path(r"C:\Program Files\Git\cmd"),
            Path(r"C:\Program Files (x86)\Git\cmd"),
            Path.home() / "AppData" / "Local" / "Programs" / "Git" / "cmd",
        ]
    return [
        Path("/usr/bin"),
        Path("/usr/local/bin"),
        Path("/opt/homebrew/bin"),
    ]


def augment_git_path() -> None:
    path = os.environ.get("PATH", "")
    parts = [p for p in path.split(os.pathsep) if p]
    known = set(parts)
    for extra in _git_extra_dirs():
        exe = extra / ("git.exe" if os.name == "nt" else "git")
        if extra.is_dir() and exe.is_file() and str(extra) not in known:
            parts.insert(0, str(extra))
            known.add(str(extra))
    os.environ["PATH"] = os.pathsep.join(parts)


def git_on_path() -> bool:
    augment_git_path()
    return shutil.which("git") is not None


def _install_git() -> None:
    attempts: list[list[str]] = []
    if os.name == "nt":
        if shutil.which("winget"):
            attempts.append(
                [
                    "winget",
                    "install",
                    "--id",
                    "Git.Git",
                    "-e",
                    "--accept-package-agreements",
                    "--accept-source-agreements",
                ]
            )
        if shutil.which("choco"):
            attempts.append(["choco", "install", "git", "-y"])
        if shutil.which("scoop"):
            attempts.append(["scoop", "install", "git"])
    elif sys.platform == "darwin":
        if shutil.which("brew"):
            attempts.append(["brew", "install", "git"])
    else:
        if shutil.which("apt-get"):
            attempts.append(["apt-get", "install", "-y", "git"])
            attempts.append(["sudo", "apt-get", "install", "-y", "git"])
        if shutil.which("dnf"):
            attempts.append(["dnf", "install", "-y", "git"])
        if shutil.which("pacman"):
            attempts.append(["pacman", "-S", "--noconfirm", "git"])
        if shutil.which("apk"):
            attempts.append(["apk", "add", "git"])
    if not attempts:
        print(
            "error: no package manager found to install git",
            file=sys.stderr,
        )
        return
    for cmd in attempts:
        print(f"trying: {' '.join(cmd)}", file=sys.stderr)
        completed = subprocess.run(cmd, check=False)
        if completed.returncode == 0:
            return


def ensure_git() -> None:
    if git_on_path():
        return
    print("git is not on PATH; trying to install it", file=sys.stderr)
    _install_git()
    if git_on_path():
        return
    sys.exit(
        "error: `git` is not on PATH and could not be installed in this "
        "environment. Install Git, then re-run."
    )


def cmd_ensure() -> None:
    ensure_git()
    print(shutil.which("git"))


def cmd_rename(source: Path, destination: Path) -> None:
    if not source.exists():
        sys.exit(f"error: source does not exist: {source}")
    run_git(["mv", str(source), str(destination)])
    print(
        f"renamed (index): {source} -> {destination}\n"
        "Commit this rename by itself before editing content.",
        file=sys.stderr,
    )


def cmd_remove(paths: list[Path]) -> None:
    fs_py = Path(__file__).resolve().parent / "fs.py"
    for path in paths:
        if not path.exists() and not _tracked(path):
            sys.exit(f"error: path does not exist and is not tracked: {path}")
        if path.exists():
            completed = subprocess.run(
                [sys.executable, str(fs_py), "trash", str(path)],
                check=False,
            )
            if completed.returncode != 0:
                sys.exit(completed.returncode)
        # Stage the working-tree deletion without git rm.
        run_git(["add", "-u", "--", str(path)])
        print(
            f"removed (trashed + staged): {path}\n"
            "Do not use git rm — recovery from it is hard.",
            file=sys.stderr,
        )


def _tracked(path: Path) -> bool:
    return run_captured(["ls-files", "--error-unmatch", str(path)]).returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_rename = sub.add_parser(
        "rename",
        help="git mv for a tracked path; commit the rename alone afterwards",
    )
    p_rename.add_argument("source", type=Path)
    p_rename.add_argument("destination", type=Path)

    p_remove = sub.add_parser(
        "remove",
        help="trash working-tree path then git add -u (never git rm)",
    )
    p_remove.add_argument("paths", nargs="+", type=Path)

    sub.add_parser(
        "ensure",
        help="install git if it is missing, then print the git executable",
    )

    args = parser.parse_args()
    if args.command == "rename":
        cmd_rename(args.source, args.destination)
    elif args.command == "remove":
        cmd_remove(args.paths)
    elif args.command == "ensure":
        cmd_ensure()


if __name__ == "__main__":
    main()
