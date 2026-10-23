#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/services/task_location.py — where a task's folder is made: Memar's own .agents/tasks/, or the project's own task location.

A project keeps its own task folders. Unless it says otherwise with the
`tasks` key of its preferences (`project_preferences`), they are made in
`.agents/tasks/` inside the project, as Memar's are inside Memar's checkout,
so git can see them and a branch switch does not drop the work silently. The
one project that does not get that default treated as a foreign location is the
Memar checkout itself, whose folders are made under the Memar root
(`modules-plugable/computer/filesystem/services/fs_memar.py`) and swept from there once their task is done. A
project may put them elsewhere with the `tasks` key. Those folders are the
project's, not Memar's: the sweep (`sweep_idle_task_folders`) never touches them,
and keeping or deleting one is the project's business, which `ensure` says each
time it makes or continues one there and `gc` says by naming the locations it
did not sweep.

A project's location is outside every Memar root, so the other task verbs —
`list`, `close`, `new --task-id` — could not find a folder there from
another working directory without searching the disk. Memar keeps the
locations instead, on the project's own entry in temp/projects.log
(`project_registry`, the `locations` array beside its names): `ensure` adds a
location each time it makes or continues a task there and the entry does
not hold it, making the entry from the project's folder name when there is
none, and reporting, never renaming, a name another project holds. Every
other reader passes over a location that no longer exists rather than
removing it, since it may be a drive that is not mounted now. Only `gc`, which
a person runs, removes those locations (`prune_registry`) and names each one,
and a location used again is recorded again by the next `ensure` there.

The earlier record, `.agents/tasks/tasks.projects` (and before that
`.agents/tasks/tasks.projects`; one location a line, no project), is not
read here. A reader of locations that finds it says so on stderr, and that a
location it lists is recorded again the next time `ensure` makes or continues a
task there, as every location is; it names no conversion, and leaves the file
as it is.

Which project a folder is in is answered here (`project_root`), because
`ensure` records it in a plan and `list --project` compares against it, and the
two must not disagree: a folder's project is its git top-level, else the
folder itself. Which locations are a project's own is answered here too, for
`list --project`: the one its preferences set, and each one on its entry, where a
location its preferences no longer name still lies. The entry, not the
location's place on disk, says whose it is: a nested project's location is its
own, and a folder that is no project owns none. Two projects are the same when
their resolved paths are, in the case the filesystem ignores (`same_path`).
No answer here reads the folder the process runs in: a project is always given.

A location that resolves inside Memar's own scratch root is Memar's, not the
project's: folders there are already found, swept, and moved by the rules for
Memar's own, and a second set of rules for the same folder would be two
answers to whether it may go. `ensure` says so each time, since the person who
set it expects otherwise. A location that resolves to the project's top folder,
or to a drive or filesystem root, is refused: its task folders would sit
among folders that are not tasks, which only the test in `task_folder`
keeps every task verb out of.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
AGENTS_DIRNAME = _m_fs_memar.AGENTS_DIRNAME
TASKS_DIRNAME = _m_fs_memar.TASKS_DIRNAME
TASKS_DIRNAME = _m_fs_memar.TASKS_DIRNAME
TEMP_DIRNAME = _m_fs_memar.TEMP_DIRNAME
project_tasks_registry = _m_fs_memar.project_tasks_registry
scratch_root = _m_fs_memar.scratch_root
tasks_root = _m_fs_memar.tasks_root
import os
import subprocess
import sys
from pathlib import Path
from machine.console import fail
from modules.process.project.services.registry import add_location, forget_missing_locations, read_entries
from modules.process.project.services.preferences import PREFERENCES_RELATIVE, TASKS_KEY, preferences_path, tasks_location
EARLIER_RECORD_REMEDY = 'a location it lists is recorded again the next time `memar task ensure` makes or continues a task there'

def _inside(path: Path, root: Path) -> bool:
    try:
        return path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False

def _key(path: Path | str) -> str:
    return os.path.normcase(str(Path(path).resolve()))

def project_root(folder: Path) -> Path:
    """The git top-level of FOLDER, else FOLDER itself; the folder the process runs in is never read, so FOLDER is always given."""
    where = Path(folder).resolve()
    try:
        found = subprocess.run(['git', '-C', str(where), 'rev-parse', '--show-toplevel'], capture_output=True, encoding='utf-8', errors='replace')
    except OSError:
        return where
    top = found.stdout.strip()
    return Path(top).resolve() if found.returncode == 0 and top else where

def same_path(one: Path | str, other: Path | str) -> bool:
    """Whether ONE and OTHER resolve to one path, in any case where the filesystem ignores case."""
    try:
        return _key(one) == _key(other)
    except (OSError, ValueError):
        return False

def _refused(project: Path, location: Path) -> str | None:
    """What LOCATION is when it may not hold PROJECT's task folders, else None."""
    resolved = location.resolve()
    if resolved == project.resolve():
        return "the project's top folder"
    if resolved == Path(resolved.anchor):
        return 'a drive or filesystem root'
    return None

def default_location(project: Path) -> Path:
    """The folder PROJECT's task folders are made in when its preferences name none: .agents/tasks/ inside it.

    Memar is an entry like any other project: its checkout's default is the same
    rule, which is Memar's own tasks folder (`modules-plugable/computer/filesystem/services/fs_memar.py`), so
    `project_location` answers None for it as for Memar's own tasks root.
    """
    return project / AGENTS_DIRNAME / TASKS_DIRNAME

def configured_location(project: Path) -> Path:
    """The folder PROJECT's preferences name, else its default."""
    named = tasks_location(project)
    return named if named is not None else default_location(project)

def _memar_own_tasks(location: Path) -> bool:
    """Whether LOCATION is Memar's own live tasks root (or still under temp scratch from before the cutover)."""
    try:
        return same_path(location, tasks_root()) or _inside(location, tasks_root()) or _inside(location, scratch_root())
    except OSError:
        return False

def unignored_note(location: Path) -> str | None:
    """The one line `ensure` prints when LOCATION is a custom path git does not ignore and is not the intended .agents/tasks default, else None."""
    try:
        if same_path(location, location.parent / AGENTS_DIRNAME / TASKS_DIRNAME) or (
            location.name == TASKS_DIRNAME and location.parent.name == AGENTS_DIRNAME
        ):
            return None
    except OSError:
        pass
    probe = location if location.exists() else location.parent
    if not probe.exists():
        probe = probe.parent
    try:
        found = subprocess.run(['git', '-C', str(probe), 'check-ignore', '-q', '--no-index', str(location / 'x')], capture_output=True)
        inside = subprocess.run(['git', '-C', str(probe), 'rev-parse', '--is-inside-work-tree'], capture_output=True, encoding='utf-8', errors='replace')
    except OSError:
        return None
    if inside.returncode != 0 or inside.stdout.strip() != 'true' or found.returncode == 0:
        return None
    return f"{location} is not ignored by git: add its folder to the project's .gitignore so its task folders are not committed by accident, or use the default .agents/{TASKS_DIRNAME}/ which is meant to be stageable"

def project_location(project: Path) -> Path | None:
    """The folder PROJECT's task folders are made in, or None for Memar's own.

    That is the folder its preferences name, else .agents/tasks/ inside the
    project (`default_location`); Memar's own tasks root answers None so the
    sweep and list treat those folders as Memar's.

    A value that resolves to the project's top folder itself, or to a drive or
    filesystem root, is refused before anything is made: the task folders
    would lie among the project's own folders, or the disk's.
    """
    location = configured_location(project)
    resolved = location.resolve()
    what = _refused(project, location)
    if what is not None:
        fail(f'`{TASKS_KEY}` in {preferences_path(project)} resolves to {resolved}, {what}; name a folder inside the project, relative to its top folder, or an absolute one')
    if _memar_own_tasks(location):
        return None
    return location

def memar_own_note(project: Path) -> str | None:
    """The one line `ensure` prints when PROJECT's `tasks` resolves to Memar's own tasks root, else None."""
    location = tasks_location(project)
    if location is None or not _memar_own_tasks(location):
        return None
    return f"{TASKS_KEY}: {location}, set in {preferences_path(project)}, is Memar's own tasks folder under .agents/{TASKS_DIRNAME}/, so it is not used as a project location: folders there are swept like Memar's"

def in_project_location(folder: Path) -> bool:
    """Whether FOLDER, a task folder, lies outside Memar's own tasks root (and outside temp scratch)."""
    return not _memar_own_tasks(folder)

def registered_locations() -> list[Path]:
    """Every project location Memar has made a task folder in that still exists, in the order recorded."""
    note_earlier_record()
    found: list[Path] = []
    for entry in read_entries():
        for each in entry.locations:
            location = Path(each)
            if location in found or not location.is_dir() or _memar_own_tasks(location):
                continue
            found.append(location)
    return found

def locations_of(project: Path) -> list[Path]:
    """The task locations that are PROJECT's own and exist: the one its preferences set, and each one on its registry entry.

    A value its preferences hold that `ensure` would refuse or not use is passed
    over: listing makes nothing, so there is nothing to refuse. A recorded
    location is the entry's own: it lies where its project put it, which need
    not be inside the project's folder.
    """
    note_earlier_record()
    found: list[Path] = []
    preferred = configured_location(project)
    if preferred.is_dir() and _refused(project, preferred) is None:
        if not _memar_own_tasks(preferred):
            found.append(preferred.resolve())
    for entry in read_entries():
        if not same_path(entry.path, project):
            continue
        for each in entry.locations:
            location = Path(each)
            if not location.is_dir() or _memar_own_tasks(location) or same_path(location, project):
                continue
            if not any((same_path(location, known) for known in found)):
                found.append(location)
    return found

def prune_registry() -> list[Path]:
    """Remove each recorded location whose folder no longer exists from its entry, and return those removed.

    The entry stays, and the registry is read again under its lock just before
    it is replaced, so a location a `ensure` recorded meanwhile is kept.
    """
    note_earlier_record()
    try:
        return forget_missing_locations()
    except OSError as error:
        print(f'warning: the project task locations could not be rewritten ({error})', file=sys.stderr)
        return []

def register(location: Path, project: Path | None=None) -> None:
    """Record LOCATION, once, on PROJECT's entry so the task verbs find its folders from any working directory.

    PROJECT is the project `ensure` works for. Given none, it is the git
    top-level of LOCATION, else the folder above it, never the folder the
    process runs in. A project with no entry gets one named from its folder;
    a name another project holds is reported and nothing is stored.
    """
    place = Path(location).resolve()
    if project is not None:
        owner = Path(project).resolve()
    else:
        owner = project_root(place)
        if same_path(owner, place):
            owner = place.parent
    try:
        add_location(owner, place)
    except SystemExit as stopped:
        print(f'warning: the project task location could not be recorded ({stopped.code})', file=sys.stderr)
    except OSError as error:
        print(f'warning: the project task location could not be recorded ({error})', file=sys.stderr)

def note_earlier_record() -> None:
    """Say on stderr that the earlier record tasks.projects is there, is not read, and how its locations come back; nothing when it is not."""
    old = project_tasks_registry()
    if old.is_file():
        print(f'memar: {old} is the earlier record of project task locations and is not read; {EARLIER_RECORD_REMEDY}', file=sys.stderr)

def project_location_note(folder: Path) -> str:
    """The one line `ensure` prints for a task folder in a project's own location."""
    return f"location: {folder.parent} is a project's own task location, set in its {PREFERENCES_RELATIVE.as_posix()} or, when that sets none, .agents/tasks/ in the project; Memar's sweep never moves a folder there — keeping or deleting it is the project's"
