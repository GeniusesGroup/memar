#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import shutil
import subprocess
from pathlib import Path
from ..errors.errors import GitFailed, GitNotInstalled, NotARepository, NotNamed
GIT_MISSING = '`git` is not on PATH. Run the Memar bootstrap for this machine (install.sh on POSIX, install.ps1 on Windows), which installs git, then run this again.'

def _git() -> str:
    found = shutil.which('git')
    if found is None:
        raise GitNotInstalled(GIT_MISSING)
    return found

def run_git(args: list[str], root: Path) -> None:
    completed = subprocess.run([_git(), '-C', str(root), *args], check=False)
    if completed.returncode != 0:
        raise GitFailed(f"git {' '.join(args)} exited {completed.returncode}")

def run_captured(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([_git(), *args], cwd=str(cwd), capture_output=True, text=True, encoding='utf-8', errors='replace')

def attempt(args: list[str], root: Path, env: dict | None=None, data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run([_git(), '-C', str(root), *args], input=data, capture_output=True, env=env)

def stderr_of(completed: subprocess.CompletedProcess[bytes]) -> str:
    return completed.stderr.decode('utf-8', 'replace').strip()

def plumb(args: list[str], root: Path, env: dict | None=None, data: bytes | None=None) -> str:
    completed = attempt(args, root, env, data)
    if completed.returncode != 0:
        raise GitFailed(f"git {' '.join(args)} failed: {stderr_of(completed)}")
    return completed.stdout.decode('utf-8').strip()

def in_repo(path: Path, root: Path) -> str:
    try:
        return (path if path.is_absolute() else root / path).resolve().relative_to(root).as_posix()
    except ValueError:
        raise NotNamed(f'{path} is not inside the repository at {root}') from None

def repository_root(repository: Path) -> Path:
    if not repository.is_dir():
        raise NotARepository(f'{repository} is not inside a git repository: it is not a folder')
    toplevel = run_captured(['rev-parse', '--show-toplevel'], cwd=repository)
    if toplevel.returncode != 0:
        raise NotARepository(f'{repository} is not inside a git repository')
    return Path(toplevel.stdout.strip()).resolve()

def repository_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument('--repository', required=True, type=Path, metavar='PATH', help='the repository to act on, by a folder in it; the folder this runs from is never read')
