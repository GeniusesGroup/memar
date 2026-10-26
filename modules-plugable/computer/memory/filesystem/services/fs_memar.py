#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/memory/filesystem/services/fs_memar.py — where Memar lives on disk: the one home for location answers.

Every script that needs a Memar path — the checkout, the recorded root, the
scratch root, a task folder — asks here instead of recomputing it. One need,
one method: a second copy of any of these answers is a second truth about where
things are, and the two drift.

It also owns the names of the folders Memar keeps inside a checkout. Those were
spelled out in three files that each had a copy — the shelf the `memar` router
lives on (which install puts on PATH), the bootstrap folder under `.agents/scripts`,
the skill folder the app layer copies, the extensions folder the editor layer
writes — and a rename in one would have left the others pointing at a folder
that no longer exists.
"""
from __future__ import annotations

from importlib import import_module
from pathlib import Path
from machine.console import fail
from machine.env_location import recorded_root

_m_fs_memar_repository = import_module("modules-plugable.computer.memory.filesystem.services.fs_memar_repository")
is_memar_repository = _m_fs_memar_repository.is_memar_repository

# The folder Memar's own configuration lives in, relative to a checkout root.
AGENTS_DIRNAME = ".agents"
# TEMP_FOLDER: spelled once here. Module and lock scratch; never part of a record;
# install gitignores a folder of this name at any depth; a task folder's own temp/ is never archived.
TEMP_FOLDER = 'temp'
TEMP_DIRNAME = TEMP_FOLDER
# Live and archived task folders share this name under `.agents/` (owner, 2026-10-20):
# not under temp/, so a branch switch or clean cannot drop the work without git noticing.
TASKS_DIRNAME = 'tasks'
TASKS_DIRNAME = TASKS_DIRNAME  # older import name; same folder
PROJECT_TASKS_NAME = 'tasks.projects'
PROJECTS_LOG_NAME = 'projects.log'
SCRIPTS_RELATIVE = Path(AGENTS_DIRNAME) / 'scripts'
LAUNCHER_RELATIVE = Path('bundles') / 'memar'
SKILL_RELATIVE = Path(AGENTS_DIRNAME) / 'skills' / 'memar'
EXTENSIONS_RELATIVE = Path(AGENTS_DIRNAME) / 'vscode' / 'extensions'
CONSUMER_README_RELATIVE = Path(AGENTS_DIRNAME) / 'memar' / 'README.md'
AGENTS_INDEX_RELATIVE = Path(AGENTS_DIRNAME) / 'README.md'
RECORDS_RELATIVE = Path(AGENTS_DIRNAME) / TASKS_DIRNAME
RECORDS_BRANCH = 'dev-knowledge'
PUBLISHED_REPOSITORY = 'GeniusesGroup/memar'
PUBLISH_BRANCH = 'main'
PUBLISHED_PAGES = f'https://github.com/{PUBLISHED_REPOSITORY}/blob/{PUBLISH_BRANCH}/'
MODULE_SKELETON = 'modules-plugable.knowledge.module-skeleton.services.module_ensure_folders'

def role_folders() -> tuple[str, ...]:
    """The role folders' names the module-skeleton profile declares; none when that pluggable module is absent.

    For the tools that walk a checkout and must not take a module's role folder
    for a module of its own (the router, the module-graph test). Imported only
    when asked, and the checkout's top must be on the search path.
    """
    import importlib
    try:
        return tuple(importlib.import_module(MODULE_SKELETON).ROLE_FOLDERS)
    except ModuleNotFoundError:
        return ()

PLUGABLE_ROOT = 'modules-plugable'

def checkout_root(start: Path | None=None) -> Path:
    """The checkout a file is in: the parent of the nearest `modules-plugable` folder above it.

    Found by that marker and not counted in levels, so a move of the file, to a
    deeper folder or a mirrored one, leaves the answer right; `start` defaults to
    this file, which stands in that folder. The nearest is taken because a pluggable
    module stands under it once, whatever its depth. Code that cannot yet import this
    file (a test that must find the root to put it on the search path) repeats the
    marker search in one line.
    """
    here = Path(start if start is not None else __file__).resolve()
    for folder in here.parents:
        if folder.name == PLUGABLE_ROOT:
            return folder.parent
    fail(f'{here} stands under no {PLUGABLE_ROOT} folder, so no checkout is found from it.')
def memar_root() -> Path:
    """The Memar root scratch lives under: recorded MEMAR_ROOT else this checkout.

    Fail-closed: when the recorded value names no repository and the checkout
    this file runs inside is no Memar repository either, there is no root to
    put scratch under, so this errors rather than guessing another folder.
    """
    recorded = recorded_root()
    if recorded is not None:
        return recorded
    checkout = checkout_root()
    if is_memar_repository(checkout):
        return checkout
    fail('cannot resolve a Memar root for scratch: MEMAR_ROOT names no Memar repository and this file runs inside no checkout either. Record one (memar install) or run from inside a checkout; nothing was guessed.')

def scratch_root() -> Path:
    """The ONE scratch root for locks and short-lived work: <root>/temp/."""
    root = memar_root() / TEMP_DIRNAME
    root.mkdir(parents=True, exist_ok=True)
    return root

def tasks_root() -> Path:
    """The folder every live task folder lives in: <root>/.agents/tasks/.

    Same relative path as archived records on `RECORDS_BRANCH` (`RECORDS_RELATIVE`).
    Not under temp/: the folder is visible to git so a mistaken clean or branch
    switch cannot drop the work without a chance to stage or recover it.
    """
    root = memar_root() / RECORDS_RELATIVE
    root.mkdir(parents=True, exist_ok=True)
    return root

tasks_root = tasks_root

def project_tasks_registry() -> Path:
    """The earlier file listing the project folders task folders were made in: <root>/.agents/tasks/tasks.projects.

    The core only notices it (`task_location`) and never reads it: a
    location it lists is recorded on its project's entry in `projects_log()`
    again when a task is next made or continued there.
    """
    return tasks_root() / PROJECT_TASKS_NAME

def projects_log() -> Path:
    """The registry of projects and their names: <root>/temp/projects.log.

    The one place a project's short name is turned into its folder, so no
    script keeps a default project or reads the calling folder. Asking for the
    path makes the missing temp folder and nothing else.
    """
    return scratch_root() / PROJECTS_LOG_NAME

def task_dir(task_id: str, *, create: bool=False) -> Path:
    """The folder of one task, under the tasks root. No guessing, no creation.

    The id names one folder segment, never a path: anything else is refused
    rather than resolved. Pass create=True only where the caller owns the
    task lifecycle; readers of another task's folder never create.
    """
    if not task_id or task_id in ('.', '..') or '/' in task_id or ('\\' in task_id):
        fail(f'refusing task id {task_id!r}: name one folder segment, not a path.')
    path = tasks_root() / task_id
    if create:
        path.mkdir(parents=True, exist_ok=True)
    return path
