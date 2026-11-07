#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from bundles.memar_git.errors.errors import GitFailed, GitNotInstalled
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
RECORDS_RELATIVE = _m_memar_location.RECORDS_RELATIVE
import os
import shutil
import subprocess
from pathlib import Path
GIT_MISSING = '`git` is not on PATH; run the Memar bootstrap for this machine (install.sh / install.ps1), which installs it'

def git(project: Path, args: list[str], data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    found = shutil.which('git')
    if found is None:
        raise GitNotInstalled(f'{GIT_MISSING}')
    return subprocess.run([found, '-C', str(project), *args], input=data, capture_output=True)

def folder_on_branch(task_id: str) -> str:
    return f'{RECORDS_RELATIVE.as_posix()}/{task_id}'

def reference(task_id: str) -> str:
    return f'{RECORDS_BRANCH}:{folder_on_branch(task_id)}/'

def is_top(project: Path) -> bool:
    if not project.is_dir():
        return False
    top = git(project, ['rev-parse', '--show-toplevel'])
    if top.returncode != 0:
        return False
    told = os.path.normcase(str(Path(top.stdout.decode('utf-8', 'replace').strip()).resolve()))
    return told == os.path.normcase(str(project.resolve()))

def exists(project: Path) -> bool:
    return git(project, ['rev-parse', '--verify', '-q', f'refs/heads/{RECORDS_BRANCH}']).returncode == 0

def every_file(project: Path) -> list[tuple[str, str, str]]:
    prefix = RECORDS_RELATIVE.as_posix() + '/'
    listed = git(project, ['ls-tree', '-r', '-z', f'refs/heads/{RECORDS_BRANCH}', '--', prefix])
    if listed.returncode != 0:
        return []
    found = []
    for record in filter(None, listed.stdout.decode('utf-8', 'replace').split('\x00')):
        meta, _, path = record.partition('\t')
        kind, blob = meta.split()[1:3]
        task, _, relative = path.removeprefix(prefix).partition('/')
        if kind == 'blob' and relative:
            found.append((task, relative, blob))
    return found

def blobs(project: Path, ids: list[str]) -> dict[str, bytes]:
    if not ids:
        return {}
    asked = ''.join((f'{each}\n' for each in ids)).encode('ascii')
    done = git(project, ['cat-file', '--batch'], asked)
    if done.returncode != 0:
        raise GitFailed(f"git cat-file failed: {done.stderr.decode('utf-8', 'replace').strip()}")
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
