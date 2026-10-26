#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/branch.py — a project's records branch: what it holds, and the one way a commit is added to it.

A project's tasks' records are kept on a branch of the project's own
repository (`fs_memar.RECORDS_BRANCH`), each task
at `.agents/tasks/<id>/` in the branch's tree, so the history of the work
does not grow with them and nothing of the checkout moves when one is kept. This
file is the whole of what the other task services know about git:

  reading   whether a folder is a repository, what the branch holds for a
            task (each file's blob id), the bytes of one file, and the blob
            id a file would have, all read-only and all told the repository,
            never the folder the process runs in;
  writing   one commit through `_host_git_cli.py record`, run by its path, which
            builds it without touching HEAD, the shared index or the working
            tree and never pushes. Nothing here runs a git command that writes.

The blob id of a file is `git hash-object --no-filters`, the bytes as they are,
which is also how `record` stores them, so "the branch holds what keeping would
write" is a comparison of ids and not of text.
"""
from __future__ import annotations
from importlib import import_module
_m_git_records = import_module('modules-plugable.computer.git.services._git_records')
git_records = _m_git_records
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
import shutil
import subprocess
import sys
from pathlib import Path
from modules.process.project.services.task_location import same_path
GIT_MISSING = '`git` is not on PATH; run the Memar bootstrap for this machine (install.sh / install.ps1), which installs it'
RECORD_VERB = 'record'

class RecordRefused(Exception):
    """`_host_git_cli.py record` could not make the commit; the message is what it said, and the branch is as it was."""

def _git(project: Path, args: list[str], data: bytes | None=None) -> subprocess.CompletedProcess[bytes]:
    found = shutil.which('git')
    if found is None:
        sys.exit(f'error: {GIT_MISSING}')
    return subprocess.run([found, '-C', str(project), *args], input=data, capture_output=True)

def reference(task_id: str) -> str:
    """How a task's records are named wherever they are cited: the branch, a colon, the task's folder on it; `modules-plugable/computer/git/services/_git_records.py` holds the form, which the content module reads too."""
    return git_records.reference(task_id)

def folder_on_branch(task_id: str) -> str:
    """The path of a task's folder in the branch's tree, without a trailing slash."""
    return git_records.folder_on_branch(task_id)

def is_repository(project: Path) -> bool:
    """Whether PROJECT is the top folder of a git repository: a project folder inside another project's repository is not one."""
    if not project.is_dir():
        return False
    top = _git(project, ['rev-parse', '--show-toplevel'])
    if top.returncode != 0:
        return False
    return same_path(Path(top.stdout.decode('utf-8', 'replace').strip()), project)

def is_checked_out(project: Path) -> bool:
    """Whether the records branch is the branch PROJECT's repository has checked out: a branch `record` will not move."""
    head = _git(project, ['symbolic-ref', '-q', 'HEAD']).stdout.decode('utf-8', 'replace').strip()
    return head == f'refs/heads/{RECORDS_BRANCH}'

def exists(project: Path) -> bool:
    """Whether PROJECT's repository has the records branch."""
    return _git(project, ['rev-parse', '--verify', '-q', f'refs/heads/{RECORDS_BRANCH}']).returncode == 0

def held(project: Path, task_id: str) -> dict[str, str]:
    """The files the branch holds for TASK_ID, by path from the task's folder, each with its blob id; none when it holds none."""
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
    """The bytes of RELATIVE in TASK_ID's folder on the branch, or None when the branch does not hold it."""
    if not exists(project):
        return None
    done = _git(project, ['cat-file', 'blob', f'refs/heads/{RECORDS_BRANCH}:{folder_on_branch(task_id)}/{relative}'])
    return done.stdout if done.returncode == 0 else None

def read_many(project: Path, task_id: str, relatives: list[str]) -> dict[str, bytes]:
    """The bytes of each of RELATIVES in TASK_ID's folder on the branch, in one `git cat-file --batch`; one the branch does not hold, or no branch, is left out.

    One process start for all of them, where `read` starts two for each: on a machine
    that scans every executable start, the starts are the cost.
    """
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

def blob_ids(project: Path, files: list[Path]) -> list[str]:
    """The blob id each of FILES would have in PROJECT's repository, the bytes as they are, in order."""
    if not files:
        return []
    listed = ''.join((f'{path}\n' for path in files)).encode('utf-8')
    done = _git(project, ['hash-object', '--no-filters', '--stdin-paths'], listed)
    if done.returncode != 0:
        sys.exit(f"error: git hash-object failed: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout.decode('utf-8').split()

def record_script() -> Path:
    """Path-invoked git CLI entry beside this file in the same services folder."""
    return Path(__file__).resolve().parent / '_host_git_cli.py'

def record(project: Path, entries: dict[str, Path], replace: list[str], message: str, scratch: Path) -> str:
    """Commit ENTRIES (a path in the branch's tree, the file giving its bytes) onto the branch, first emptying the REPLACE folders; the branch's tip.

    The manifest and the message go in files in SCRATCH, a folder that is the
    caller's to clear. A run that cannot commit raises RecordRefused with what
    `_host_git_cli.py` said, and the branch is as it was.
    """
    manifest, message_file = (scratch / 'manifest.txt', scratch / 'message.txt')
    manifest.write_bytes(''.join((f'{target}\t{source}\n' for target, source in entries.items())).encode('utf-8'))
    message_file.write_bytes(message.encode('utf-8'))
    command = [sys.executable, str(record_script()), RECORD_VERB, '--repository', str(project), '--branch', RECORDS_BRANCH, '--manifest', str(manifest), '-F', str(message_file)]
    for folder in replace:
        command += ['--replace', folder]
    done = subprocess.run(command, capture_output=True)
    if done.returncode != 0:
        said = (done.stderr or done.stdout).decode('utf-8', 'replace').strip()
        raise RecordRefused(said.removeprefix('error: ') if said else f'git.py {RECORD_VERB} failed with status {done.returncode}')
    return done.stdout.decode('utf-8').strip().splitlines()[-1]
