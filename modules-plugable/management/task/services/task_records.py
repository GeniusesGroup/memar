#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/management/task/services/task_records.py — the tasks a content verb reads when it is asked to: their archived records and their live folders.

The source `tasks` of `CorpusSource` (`modules/knowledge/text/primitive/corpus_source.py`).
A task's records are what it wrote while it worked, and a later task meeting a question
like an earlier one must be able to find the earlier answer (owner, 2026-10-19). They are read
only when a verb is asked for them, because each is one task's claim and never a ruling, and
each is named so that a reader sees whose claim it is: the task's id and the file in it, in
the form a changelog cites them.

**Two places hold them.** A finished task's records are archived on the records branch of
the project's own repository (`modules-plugable/computer/git/services/_git_records.py`), read with git's read-only commands, so
nothing of the checkout moves: no HEAD, index or working tree. A task still in progress, or
finished and not yet swept, has a live folder: in the project's tasks folder (its preferences'
`tasks`, else `.agents/tasks/` inside it), and in Memar's own when its plan names the project
by its folder. A task that has a live folder is read from that folder alone, as
`memar git show-task-records` reads it first, since while the folder exists it is the task's latest state.

**What is read of them.** Every text file, as the archive keeps them: binary files are left
out, and so is a live folder's own temp/, which the archive never keeps. A project whose
preferences say `records: off` has no archived records; a project that is not a repository's top
folder, or whose repository has no records branch, has none either. Each of those is said in a
note the verb prints, so an empty answer is not read as an absence of the subject.

A hit names its file so: `<branch>:.agents/tasks/<id>/<file>` for an archived one, and the
live folder's path, from the project when it lies inside it, for a live one.
"""
from __future__ import annotations
from importlib import import_module
from machine.plugable_import import load as plugable_load
_m_git_records = plugable_load('computer.git.services._git_records')
git_records = _m_git_records
_m_fs_memar = plugable_load('computer.memory.filesystem.services.fs_memar')
RECORDS_BRANCH = _m_fs_memar.RECORDS_BRANCH
TEMP_DIRNAME = _m_fs_memar.TEMP_DIRNAME
TASKS_DIRNAME = _m_fs_memar.TASKS_DIRNAME
tasks_root = _m_fs_memar.tasks_root
from pathlib import Path
from typing import NamedTuple
PLAN_FILE = 'plan.md'
CLAIM_FILE = 'claim'

class Record(NamedTuple):
    """One file of one task: the path a hit names, the task's id, its suffix, and where its bytes are: a live FILE or an archived BLOB."""
    path: str
    task: str
    suffix: str
    file: Path | None
    blob: str | None

def text_of(data: bytes) -> str | None:
    """DATA as text, None when it is binary: a NUL byte in it, as git itself judges."""
    if b'\x00' in data:
        return None
    return data.decode('utf-8-sig', errors='replace')

def _same(one: Path, other: Path) -> bool:
    import os
    return os.path.normcase(str(one.resolve())) == os.path.normcase(str(other.resolve()))

def _label(file: Path, root: Path) -> str:
    try:
        return file.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return file.resolve().as_posix()

def _names_project(folder: Path, root: Path) -> bool:
    """Whether the plan in FOLDER names ROOT by its folder."""
    _m_plan_key = import_module('modules-plugable.knowledge.documentation.plan.primitive.plan_key')
    PlanKey = _m_plan_key.PlanKey
    _m_plan_file = import_module('modules-plugable.management.task.services.plan_file')
    read_plan = _m_plan_file.read_plan
    named = ((read_plan(folder / PLAN_FILE).front or {}).get(PlanKey.PROJECT.key) or '').strip()
    if not named:
        return False
    candidate = Path(named)
    return candidate.is_absolute() and candidate.is_dir() and _same(candidate, root)

def live_folders(root: Path) -> list[Path]:
    """The live task folders of the project at ROOT: each in its tasks folder, and each in Memar's own whose plan names ROOT; sorted by id."""
    from modules.process.project.services.preferences import tasks_location
    own = tasks_location(root) or root / _m_fs_memar.AGENTS_DIRNAME / TASKS_DIRNAME
    memar = tasks_root()
    found: dict[str, Path] = {}
    for location in (own, memar):
        if not location.is_dir():
            continue
        whole = _same(location, own)
        for folder in location.iterdir():
            if folder.name in found or not (folder / PLAN_FILE).is_file():
                continue
            if whole or _names_project(folder, root):
                found[folder.name] = folder
    return [found[name] for name in sorted(found)]

def _live(root: Path, folder: Path) -> list[Record]:
    from modules.knowledge.text.services.corpus import is_generated
    records = []
    for file in sorted(folder.rglob('*')):
        if not file.is_file() or file.is_symlink():
            continue
        parts = file.relative_to(folder).parts
        if parts[0] == TEMP_DIRNAME or parts == (CLAIM_FILE,) or is_generated(parts[:-1]):
            continue
        records.append(Record(_label(file, root), folder.name, file.suffix.lower(), file, None))
    return records

def archive_note(root: Path) -> str | None:
    """Why the project at ROOT has no archived records to read, or None when its records branch is there to read."""
    from modules.process.project.services.preferences import Records, preferences_path, records_preference
    said = records_preference(root)
    if said is Records.OFF:
        return f'{root} keeps no archived task records: its preferences ({preferences_path(root)}) say `records: off`'
    if said is None:
        return f'{root} has no archived task records read: `records` in {preferences_path(root)} is neither {Records.listing()}'
    if not git_records.is_top(root):
        return f'{root} has no archived task records: it is not the top folder of a git repository, so it has no branch {RECORDS_BRANCH}'
    if not git_records.exists(root):
        return f'{root} has no archived task records: its repository has no branch {RECORDS_BRANCH}'
    return None

def task_records(root: Path) -> tuple[list[Record], list[str]]:
    """Every file of every task of the project at ROOT, live folders first, and the notes that say what could not be read and why."""
    records: list[Record] = []
    live = live_folders(root)
    for folder in live:
        records.extend(_live(root, folder))
    note = archive_note(root)
    if note is not None:
        return (records, [note])
    read_live = {folder.name for folder in live}
    for task, relative, blob in git_records.every_file(root):
        if task in read_live or relative.split('/', 1)[0] == TEMP_DIRNAME:
            continue
        suffix = Path(relative).suffix.lower()
        records.append(Record(f'{git_records.reference(task)}{relative}', task, suffix, None, blob))
    return (records, [])

def read_all(root: Path, records: list[Record]) -> dict[str, str]:
    """The text of each of RECORDS that is text, by its path: live files read from disk, archived ones in one read of the branch."""
    archived = git_records.blobs(root, sorted({each.blob for each in records if each.blob}))
    found: dict[str, str] = {}
    for record in records:
        if record.file is not None:
            try:
                data = record.file.read_bytes()
            except OSError:
                continue
        else:
            data = archived.get(record.blob or '')
            if data is None:
                continue
        text = text_of(data)
        if text is not None:
            found[record.path] = text
    return found
