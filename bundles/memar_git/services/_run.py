#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""computer/git/services/_run.py — running git in a repository the caller named, and naming that repository.

The floor every path-invoked git verb stands on: the git executable, one run that stops the verb
on failure, one that captures, one that keeps git's answer for the caller to judge, the
repository's top folder from a folder in it, a path as git names it from there, and the
`--repository` flag every verb takes. None reads the folder it runs from.
"""
from __future__ import annotations
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
GIT_MISSING = 'error: `git` is not on PATH. Run the Memar bootstrap for this machine (install.sh on POSIX, install.ps1 on Windows) — it installs git — then run this again.'

def _git() -> str:
    """The git executable, or the one command that provides it."""
    found = shutil.which('git')
    if found is None:
        sys.exit(GIT_MISSING)
    return found

def run_git(args: list[str], root: Path) -> None:
    """Run git in the repository at ROOT, never in the folder this runs from."""
    completed = subprocess.run([_git(), '-C', str(root), *args], check=False)
    if completed.returncode != 0:
        sys.exit(completed.returncode)

def run_captured(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([_git(), *args], cwd=str(cwd), capture_output=True, text=True, encoding='utf-8', errors='replace')

def attempt(args: list[str], root: Path, env: dict | None=None, data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([_git(), '-C', str(root), *args], input=data, capture_output=True, env=env)

def stderr_of(completed: subprocess.CompletedProcess[bytes]) -> str:
    return completed.stderr.decode('utf-8', 'replace').strip()

def plumb(args: list[str], root: Path, env: dict | None=None, data: bytes | None=None) -> str:
    completed = attempt(args, root, env, data)
    if completed.returncode != 0:
        sys.exit(f"error: git {' '.join(args)} failed: {stderr_of(completed)}")
    return completed.stdout.decode('utf-8').strip()

def in_repo(path: Path, root: Path) -> str:
    """PATH as git names it, from the top of the repository at ROOT: a relative PATH is relative to the repository, never to the folder this runs from."""
    try:
        return (path if path.is_absolute() else root / path).resolve().relative_to(root).as_posix()
    except ValueError:
        sys.exit(f'error: {path} is not inside the repository at {root}')

def repository_root(repository: Path) -> Path:
    """The top folder of the repository REPOSITORY is in: the folder the caller named, never the one the command runs from."""
    if not repository.is_dir():
        sys.exit(f'error: {repository} is not inside a git repository: it is not a folder')
    toplevel = run_captured(['rev-parse', '--show-toplevel'], cwd=repository)
    if toplevel.returncode != 0:
        sys.exit(f'error: {repository} is not inside a git repository')
    return Path(toplevel.stdout.strip()).resolve()

def repository_flag(parser: argparse.ArgumentParser) -> None:
    """Give PARSER the one flag that says which repository a verb acts on: always given, never read from the folder it runs in."""
    parser.add_argument('--repository', required=True, type=Path, metavar='PATH', help='the repository to act on, by a folder in it; the folder this runs from is never read')
