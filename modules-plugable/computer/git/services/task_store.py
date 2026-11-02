#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/services/task_store.py — tasks live on RECORDS_BRANCH only.

Durable trees are on `RECORDS_BRANCH` at `.agents/tasks/<id>/`. Services read and
write bytes through git plumbing (`held` / `read` / `record`); there is no
task materialization folder. Claim locks alone use `temp/claims/<id>/`.
Agents never see a filesystem path for a task.
"""
from __future__ import annotations
from importlib import import_module
_m_fs_memar = import_module('modules-plugable.computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
RECORDS_RELATIVE = _m_fs_memar.RECORDS_RELATIVE
memar_root = _m_fs_memar.memar_root
scratch_root = _m_fs_memar.scratch_root
import shutil
import tempfile
from pathlib import Path
from . import branch as task_branch
from .branch import RecordRefused, folder_on_branch
CLAIMS_DIRNAME = 'claims'

def records_project() -> Path:
    """The repository whose records branch holds Memar's own tasks."""
    return memar_root()

def claims_root() -> Path:
    """Exclusive claim locks; local scratch, never recorded on the branch."""
    root = scratch_root() / CLAIMS_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root

def claim_dir(task_id: str) -> Path:
    path = claims_root() / task_id
    path.mkdir(parents=True, exist_ok=True)
    return path

def list_task_ids(project: Path | None=None) -> list[str]:
    """Task ids the records branch holds, newest-looking id first."""
    project = project or records_project()
    if not task_branch.exists(project):
        return []
    tree_ref = f'refs/heads/{RECORDS_BRANCH}:{RECORDS_RELATIVE.as_posix()}'
    listed = task_branch._git(project, ['ls-tree', '--name-only', tree_ref])
    if listed.returncode != 0:
        return []
    ids = [line.strip() for line in listed.stdout.decode('utf-8', 'replace').splitlines() if line.strip() and '/' not in line.strip()]
    ids.sort(reverse=True)
    return ids

def on_branch(task_id: str, project: Path | None=None) -> bool:
    project = project or records_project()
    return bool(task_branch.held(project, task_id))

def tree(task_id: str, project: Path | None=None) -> dict[str, bytes]:
    """Every file of TASK_ID on the branch as relative path → bytes; empty when none."""
    project = project or records_project()
    held = task_branch.held(project, task_id)
    if not held:
        return {}
    return task_branch.read_many(project, task_id, list(held))

def resolve_project_name(named: str, project: Path | None=None) -> Path:
    if project is not None and Path(project).is_dir():
        return Path(project)
    if not named:
        return records_project()
    path = Path(named)
    if path.is_dir():
        return path
    try:
        from modules.computer.software.services.project_find import project_by_name
        return Path(project_by_name(named))
    except SystemExit:
        return records_project()

def project_of_task(task_id: str, project: Path | None=None) -> Path:
    """The git repository that should hold TASK_ID's records."""
    if project is not None and Path(project).is_dir():
        return Path(project)
    files = tree(task_id)
    named = ''
    if 'task.yaml' in files:
        from modules.knowledge.text.services.header_text import parse
        named = (parse(files['task.yaml'].decode('utf-8-sig').splitlines()) or {}).get('project', '').strip()
    elif 'plan.md' in files:
        for line in files['plan.md'].decode('utf-8-sig').splitlines():
            if line.startswith('Project:'):
                named = line.split(':', 1)[1].strip()
                break
    return resolve_project_name(named)

def put_files(task_id: str, updates: dict[str, bytes], project: Path | None=None, *, message: str | None=None, replace_all: bool=False) -> str:
    """Commit UPDATES onto TASK_ID's tree on the records branch.

    Unless REPLACE_ALL, existing files are kept and UPDATES overwrite by path.
    """
    project = project_of_task(task_id, project)
    if not task_branch.is_repository(project):
        raise RecordRefused(f'{project} is not the top of a git repository')
    if task_branch.is_checked_out(project):
        raise RecordRefused(f'the branch {RECORDS_BRANCH} is checked out in {project}')
    files = {} if replace_all else tree(task_id, project)
    files.update(updates)
    return flush_bytes(task_id, files, project=project, message=message)

def flush_bytes(task_id: str, files: dict[str, bytes], project: Path | None=None, *, message: str | None=None) -> str:
    """Replace TASK_ID's tree on the branch with FILES in one commit."""
    project = project or records_project()
    with tempfile.TemporaryDirectory(dir=scratch_root(), prefix='record-') as workdir:
        scratch = Path(workdir)
        folder = scratch / 'tree'
        folder.mkdir()
        entries: dict[str, Path] = {}
        for relative, data in files.items():
            path = folder / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
            entries[f'{folder_on_branch(task_id)}/{relative}'] = path
        return task_branch.record(project, entries, [folder_on_branch(task_id)], message or f'Record task {task_id}\n', scratch)

def verify_tip(project: Path | None=None) -> str:
    """The records branch tip, or raise RecordRefused when the branch is missing."""
    project = project or records_project()
    if not task_branch.exists(project):
        raise RecordRefused(f'no branch {RECORDS_BRANCH} in {project}')
    done = task_branch._git(project, ['rev-parse', f'refs/heads/{RECORDS_BRANCH}'])
    if done.returncode != 0:
        raise RecordRefused(f'cannot read tip of {RECORDS_BRANCH} in {project}')
    return done.stdout.decode('utf-8').strip()

def drop_legacy_task_store() -> None:
    """Remove leftover temp/task-store if a prior cutover left one; never recreated."""
    root = scratch_root() / 'task-store'
    if root.is_dir():
        shutil.rmtree(root, ignore_errors=True)
