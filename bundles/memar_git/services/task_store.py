#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
_m_memar_location = import_module('bundles.memar.services.location.memar_location')
RECORDS_BRANCH = _m_memar_location.RECORDS_BRANCH
RECORDS_RELATIVE = _m_memar_location.RECORDS_RELATIVE
import shutil
import tempfile
from pathlib import Path
from . import branch as task_branch
from .branch import RecordRefused, folder_on_branch
CLAIMS_DIRNAME = 'claims'

def memar_root() -> Path:
    return _m_memar_location.memar_root()

def scratch_root() -> Path:
    return _m_memar_location.scratch_root()

def records_project() -> Path:
    return memar_root()

def claims_root() -> Path:
    root = scratch_root() / CLAIMS_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root

def claim_dir(task_id: str) -> Path:
    path = claims_root() / task_id
    path.mkdir(parents=True, exist_ok=True)
    return path

def list_task_ids(project: Path | None=None) -> list[str]:
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
    project = project or records_project()
    held = task_branch.held(project, task_id)
    if not held:
        return {}
    return task_branch.read_many(project, task_id, list(held))
_scanned: dict[str, dict[str, bytes]] | None = None

def scan(names: tuple[str, ...]) -> None:
    global _scanned
    _scanned = task_branch.read_named_of_all(records_project(), names)

def light(task_id: str, names: tuple[str, ...]) -> dict[str, bytes]:
    if _scanned is not None and task_id in _scanned:
        return {name: data for name, data in _scanned[task_id].items() if name in names}
    project = records_project()
    held = task_branch.held(project, task_id)
    return task_branch.read_many(project, task_id, [name for name in names if name in held])

def forget_scan() -> None:
    global _scanned
    _scanned = None

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
    if project is not None and Path(project).is_dir():
        return Path(project)
    files = tree(task_id)
    named = ''
    if 'task.yaml' in files:
        from modules.knowledge.text.services.header_text import parse
        named = (parse(files['task.yaml'].decode('utf-8-sig').splitlines()) or {}).get('project', '').strip()
    return resolve_project_name(named)

def put_files(task_id: str, updates: dict[str, bytes], project: Path | None=None, *, message: str | None=None, replace_all: bool=False) -> str:
    project = project_of_task(task_id, project)
    if not task_branch.is_repository(project):
        raise RecordRefused(f'{project} is not the top of a git repository')
    if task_branch.is_checked_out(project):
        raise RecordRefused(f'the branch {RECORDS_BRANCH} is checked out in {project}')
    files = {} if replace_all else tree(task_id, project)
    files.update(updates)
    return flush_bytes(task_id, files, project=project, message=message)

def flush_bytes(task_id: str, files: dict[str, bytes], project: Path | None=None, *, message: str | None=None) -> str:
    project = project or records_project()
    forget_scan()
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
    project = project or records_project()
    if not task_branch.exists(project):
        raise RecordRefused(f'no branch {RECORDS_BRANCH} in {project}')
    done = task_branch._git(project, ['rev-parse', f'refs/heads/{RECORDS_BRANCH}'])
    if done.returncode != 0:
        raise RecordRefused(f'cannot read tip of {RECORDS_BRANCH} in {project}')
    return done.stdout.decode('utf-8').strip()

def drop_legacy_task_store() -> None:
    root = scratch_root() / 'task-store'
    if root.is_dir():
        shutil.rmtree(root, ignore_errors=True)
