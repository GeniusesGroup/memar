#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/_git_records.py — a project's records branch, read: what it holds, by whom it is cited, and the bytes of its files.

A project's sessions' records are kept on the branch `fs_memar.RECORDS_BRANCH` of
the project's own repository, each session at `RECORDS_RELATIVE/<id>/` in the branch's tree,
by `memar git archive-task-records` (`modules-plugable/computer/git/services/archive_task_records.py`). Two modules read
that branch: the session module, which prints one session by its id, and the content module,
whose `find` and `search` read every session's records when they are asked to. The content
module may not import the session module, which imports it, so what both need is here, on the
shelf below both: how a session's records are cited, and git's read-only commands on the
branch. Nothing here writes; writing is `_host_git_cli.py record`'s, through the session module.

Every function is told the repository and never reads the folder the process runs in. Each
asks git with `-C PROJECT`, so a folder inside another repository is not taken for that
repository: `is_top` says whether PROJECT is a repository's own top folder.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
import os
import shutil
import subprocess
import sys
from pathlib import Path
GIT_MISSING = '`git` is not on PATH; run the Memar bootstrap for this machine (install.sh / install.ps1), which installs it'

def git(project: Path, args: list[str], data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    """Run git's ARGS on the repository PROJECT, never on the folder the process runs in."""
    found = shutil.which('git')
    if found is None:
        sys.exit(f'error: {GIT_MISSING}')
    return subprocess.run([found, '-C', str(project), *args], input=data, capture_output=True)

def folder_on_branch(task_id: str) -> str:
    """The path of a session's folder in the branch's tree, without a trailing slash."""
    return f'{RECORDS_RELATIVE.as_posix()}/{task_id}'

def reference(task_id: str) -> str:
    """How a session's records are named wherever they are cited: the branch, a colon, the session's folder on it."""
    return f'{RECORDS_BRANCH}:{folder_on_branch(task_id)}/'

def is_top(project: Path) -> bool:
    """Whether PROJECT is the top folder of a git repository: a folder inside another project's repository is not one."""
    if not project.is_dir():
        return False
    top = git(project, ['rev-parse', '--show-toplevel'])
    if top.returncode != 0:
        return False
    told = os.path.normcase(str(Path(top.stdout.decode('utf-8', 'replace').strip()).resolve()))
    return told == os.path.normcase(str(project.resolve()))

def exists(project: Path) -> bool:
    """Whether PROJECT's repository has the records branch."""
    return git(project, ['rev-parse', '--verify', '-q', f'refs/heads/{RECORDS_BRANCH}']).returncode == 0

def every_file(project: Path) -> list[tuple[str, str, str]]:
    """Each file the branch holds under its sessions' folder, as (session id, path from the session's folder, blob id), in the branch's order; none without the branch."""
    prefix = RECORDS_RELATIVE.as_posix() + '/'
    listed = git(project, ['ls-tree', '-r', '-z', RECORDS_BRANCH, '--', prefix])
    if listed.returncode != 0:
        return []
    found = []
    for record in filter(None, listed.stdout.decode('utf-8', 'replace').split('\x00')):
        meta, _, path = record.partition('\t')
        kind, blob = meta.split()[1:3]
        session, _, relative = path.removeprefix(prefix).partition('/')
        if kind == 'blob' and relative:
            found.append((session, relative, blob))
    return found

def blobs(project: Path, ids: list[str]) -> dict[str, bytes]:
    """The bytes of each blob of IDS in PROJECT's repository, read in one `git cat-file --batch`; an id git does not hold is left out."""
    if not ids:
        return {}
    asked = ''.join((f'{each}\n' for each in ids)).encode('ascii')
    done = git(project, ['cat-file', '--batch'], asked)
    if done.returncode != 0:
        sys.exit(f"error: git cat-file failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    out, at, found = (done.stdout, 0, {})
    while at < len(out):
        end = out.index(b'\n', at)
        header = out[at:end].decode('ascii', 'replace').split()
        at = end + 1
        if len(header) < 3 or header[1] == 'missing':
            continue
        size = int(header[2])
        found[header[0]] = out[at:at + size]
        at += size + 1
    return found
