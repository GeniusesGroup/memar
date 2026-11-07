#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from bundles.memar_git.errors.errors import GitFailed, GitNotInstalled
from importlib import import_module
_m_git_records = import_module('bundles.memar_git.services._git_records')
git_records = _m_git_records
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
RECORDS_RELATIVE = _m_memar_location.RECORDS_RELATIVE
import shutil
import subprocess
import sys
from pathlib import Path
_m_task_location = import_module('modules-plugable.management.task.services.task_location')
same_path = _m_task_location.same_path
GIT_MISSING = '`git` is not on PATH; run the Memar bootstrap for this machine (install.sh / install.ps1), which installs it'
RECORD_VERB = 'record'

class RecordRefused(Exception):
    pass

def _git(project: Path, args: list[str], data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    found = shutil.which('git')
    if found is None:
        raise GitNotInstalled(f'{GIT_MISSING}')
    return subprocess.run([found, '-C', str(project), *args], input=data, capture_output=True)

def reference(task_id: str) -> str:
    return git_records.reference(task_id)

def folder_on_branch(task_id: str) -> str:
    return git_records.folder_on_branch(task_id)

def is_repository(project: Path) -> bool:
    if not project.is_dir():
        return False
    top = _git(project, ['rev-parse', '--show-toplevel'])
    if top.returncode != 0:
        return False
    return same_path(Path(top.stdout.decode('utf-8', 'replace').strip()), project)

def is_checked_out(project: Path) -> bool:
    head = _git(project, ['symbolic-ref', '-q', 'HEAD']).stdout.decode('utf-8', 'replace').strip()
    return head == f'refs/heads/{RECORDS_BRANCH}'

def exists(project: Path) -> bool:
    return _git(project, ['rev-parse', '--verify', '-q', f'refs/heads/{RECORDS_BRANCH}']).returncode == 0

def held(project: Path, task_id: str) -> dict[str, str]:
    prefix = folder_on_branch(task_id) + '/'
    if not exists(project):
        return {}
    listed = _git(project, ['ls-tree', '-r', '-z', f'refs/heads/{RECORDS_BRANCH}', '--', prefix])
    if listed.returncode != 0:
        return {}
    found: dict[str, str] = {}
    for record in filter(None, listed.stdout.decode('utf-8', 'replace').split('\x00')):
        meta, _, path = record.partition('\t')
        found[path.removeprefix(prefix)] = meta.split()[2]
    return found

def read(project: Path, task_id: str, relative: str) -> bytes | None:
    if not exists(project):
        return None
    done = _git(project, ['cat-file', 'blob', f'refs/heads/{RECORDS_BRANCH}:{folder_on_branch(task_id)}/{relative}'])
    return done.stdout if done.returncode == 0 else None

def read_many(project: Path, task_id: str, relatives: list[str]) -> dict[str, bytes]:
    asked = ''.join((f'refs/heads/{RECORDS_BRANCH}:{folder_on_branch(task_id)}/{each}\n' for each in relatives)).encode('utf-8')
    done = _git(project, ['cat-file', '--batch'], asked)
    out, at, found = (done.stdout, 0, {})
    for each in relatives:
        end = out.find(b'\n', at)
        if end < 0:
            break
        header = out[at:end].decode('utf-8', 'replace').split()
        at = end + 1
        if len(header) == 3 and header[1] == 'blob':
            size = int(header[2])
            found[each] = out[at:at + size]
            at += size + 1
    return found

def read_named_of_all(project: Path, names: tuple[str, ...]) -> dict[str, dict[str, bytes]]:
    if not exists(project):
        return {}
    prefix = RECORDS_RELATIVE.as_posix() + '/'
    listed = _git(project, ['ls-tree', '-r', '-z', f'refs/heads/{RECORDS_BRANCH}', '--', prefix])
    if listed.returncode != 0:
        return {}
    tasks: dict[str, dict[str, str]] = {}
    for record in filter(None, listed.stdout.decode('utf-8', 'replace').split('\x00')):
        meta, _, path = record.partition('\t')
        task_id, _, relative = path.removeprefix(prefix).partition('/')
        wanted = tasks.setdefault(task_id, {})
        if relative in names:
            wanted[relative] = meta.split()[2]
    blobs = sorted({blob for wanted in tasks.values() for blob in wanted.values()})
    done = _git(project, ['cat-file', '--batch'], ''.join((f'{blob}\n' for blob in blobs)).encode('utf-8'))
    out, at, content = (done.stdout, 0, {})
    for blob in blobs:
        end = out.find(b'\n', at)
        if end < 0:
            break
        header = out[at:end].decode('utf-8', 'replace').split()
        at = end + 1
        if len(header) == 3 and header[1] == 'blob':
            size = int(header[2])
            content[blob] = out[at:at + size]
            at += size + 1
    return {task_id: {name: content[blob] for name, blob in wanted.items() if blob in content} for task_id, wanted in tasks.items()}

def blob_ids(project: Path, files: list[Path]) -> list[str]:
    if not files:
        return []
    listed = ''.join((f'{path}\n' for path in files)).encode('utf-8')
    done = _git(project, ['hash-object', '--no-filters', '--stdin-paths'], listed)
    if done.returncode != 0:
        raise GitFailed(f"git hash-object failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout.decode('utf-8').split()

def record_script() -> Path:
    return Path(__file__).resolve().parent / '_host_git_cli.py'

def record(project: Path, entries: dict[str, Path], replace: list[str], message: str, scratch: Path) -> str:
    manifest, message_file = (scratch / 'manifest.txt', scratch / 'message.txt')
    manifest.write_bytes(''.join((f'{target}\t{source}\n' for target, source in entries.items())).encode('utf-8'))
    message_file.write_bytes(message.encode('utf-8'))
    command = [sys.executable, str(record_script()), RECORD_VERB, '--repository', str(project), '--branch', RECORDS_BRANCH, '--manifest', str(manifest), '-F', str(message_file)]
    replace_file = scratch / 'replace.txt'
    replace_file.write_bytes(''.join((f'{folder}' + chr(10) for folder in replace)).encode('utf-8'))
    command += ['--replace-file', str(replace_file)]
    done = subprocess.run(command, capture_output=True)
    if done.returncode != 0:
        said = (done.stderr or done.stdout).decode('utf-8', 'replace').strip()
        raise RecordRefused(said.removeprefix('error: ') if said else f'git.py {RECORD_VERB} failed with status {done.returncode}')
    return done.stdout.decode('utf-8').strip().splitlines()[-1]
