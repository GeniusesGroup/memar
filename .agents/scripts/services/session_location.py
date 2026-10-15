#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_location.py — where a session's folder is made: Memar's own temp/sessions/, or the project's own session location.

A project keeps its own session folders. Unless it says otherwise with the
`sessions` key of its preferences (`project_preferences`), they are made in
temp/sessions/ inside the project, as Memar's are inside Memar's checkout; the
project's VCS is expected to ignore temp/ (`new` says when git does not, and
changes nothing). The one project that does not get that default is the Memar
checkout itself, whose folders are made under the Memar root
(`machine/fs_memar.py`) and swept from there once their task is done. A
project may put them elsewhere — to commit them, or read them beside its
own work — with the `sessions` key. Those folders are the project's, not
Memar's: the sweep (`session_gc`) and the move out of temp/
(`session_migrate`) never touch them, and keeping or deleting one is the
project's business, which `new` says each time it makes or continues one there
and `gc` says by naming the locations it did not sweep.

A project's location is outside every Memar root, so the other session verbs —
`list`, `close`, `new --session-id` — could not find a folder there from
another working directory without searching the disk. Memar keeps the
locations instead, on the project's own entry in temp/projects.log
(`project_registry`, the `locations` array beside its names): `new` adds a
location each time it makes or continues a session there and the entry does
not hold it, making the entry from the project's folder name when there is
none, and reporting, never renaming, a name another project holds. Every
other reader passes over a location that no longer exists rather than
removing it, since it may be a drive that is not mounted now. Only `gc`, which
a person runs, removes those locations (`prune_registry`) and names each one,
and a location used again is recorded again by the next `new` there.

The earlier record, temp/sessions/sessions.projects (one location a line, no
project), is not read here. A reader of locations that finds it says so on
stderr, and that a location it lists is recorded again the next time `new`
makes or continues a session there, as every location is; it names no
conversion, and leaves the file as it is.

Which project a folder is in is answered here (`project_root`), because
`new` records it in a plan and `list --project` compares against it, and the
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
answers to whether it may go. `new` says so each time, since the person who
set it expects otherwise. A location that resolves to the project's top folder,
or to a drive or filesystem root, is refused: its session folders would sit
among folders that are not sessions, which only the test in `session_folder`
keeps every session verb out of.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from machine.console import fail
from machine.fs_memar import SESSIONS_DIRNAME, TEMP_DIRNAME, project_sessions_registry, scratch_root
from services.project_registry import add_location, forget_missing_locations, read_entries
from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY, preferences_path, sessions_location

# What the note about the earlier record says comes of the locations it lists.
EARLIER_RECORD_REMEDY = (
    "a location it lists is recorded again the next time `memar session new` makes or continues a session there"
)


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
        found = subprocess.run(
            ["git", "-C", str(where), "rev-parse", "--show-toplevel"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
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
    """What LOCATION is when it may not hold PROJECT's session folders, else None."""
    resolved = location.resolve()
    if resolved == project.resolve():
        return "the project's top folder"
    if resolved == Path(resolved.anchor):
        return "a drive or filesystem root"
    return None


def default_location(project: Path) -> Path:
    """The folder PROJECT's session folders are made in when its preferences name none: temp/sessions/ inside it.

    Memar is an entry like any other project: its checkout's default is the same
    rule, which is Memar's own sessions folder (`machine/fs_memar.py`), so
    `project_location` answers None for it as for a location inside Memar's scratch.
    """
    return project / TEMP_DIRNAME / SESSIONS_DIRNAME


def configured_location(project: Path) -> Path:
    """The folder PROJECT's preferences name, else its default."""
    named = sessions_location(project)
    return named if named is not None else default_location(project)


def unignored_note(location: Path) -> str | None:
    """The one line `new` prints when LOCATION lies in a git work tree that does not ignore it, else None."""
    probe = location if location.exists() else location.parent
    if not probe.exists():
        probe = probe.parent
    try:
        found = subprocess.run(
            ["git", "-C", str(probe), "check-ignore", "-q", "--no-index", str(location / "x")],
            capture_output=True,
        )
        inside = subprocess.run(
            ["git", "-C", str(probe), "rev-parse", "--is-inside-work-tree"],
            capture_output=True,
            encoding="utf-8",
            errors="replace",
        )
    except OSError:
        return None
    if inside.returncode != 0 or inside.stdout.strip() != "true" or found.returncode == 0:
        return None
    return (
        f"{location} is not ignored by git: add its folder to the project's .gitignore "
        "so its session folders are not committed by accident"
    )


def project_location(project: Path) -> Path | None:
    """The folder PROJECT's session folders are made in, or None for Memar's own.

    That is the folder its preferences name, else temp/sessions/ inside the
    project (`default_location`); a folder inside Memar's scratch, which is
    where the Memar checkout's default lies, is Memar's own and answers None.

    A value that resolves to the project's top folder itself, or to a drive or
    filesystem root, is refused before anything is made: the session folders
    would lie among the project's own folders, or the disk's.
    """
    location = configured_location(project)
    resolved = location.resolve()
    what = _refused(project, location)
    if what is not None:
        fail(
            f"`{SESSIONS_KEY}` in {preferences_path(project)} resolves to {resolved}, {what}; "
            "name a folder inside the project, relative to its top folder, or an absolute one"
        )
    if _inside(location, scratch_root()):
        return None
    return location


def memar_own_note(project: Path) -> str | None:
    """The one line `new` prints when PROJECT's `sessions` resolves inside Memar's own scratch, else None."""
    location = sessions_location(project)
    if location is None or not _inside(location, scratch_root()):
        return None
    return (
        f"{SESSIONS_KEY}: {location}, set in {preferences_path(project)}, lies inside Memar's own "
        "temp/, so it is not used: the folder is Memar's own, under temp/sessions/, and swept like one"
    )


def in_project_location(folder: Path) -> bool:
    """Whether FOLDER, a session folder, lies outside Memar's own scratch root."""
    return not _inside(folder, scratch_root())


def registered_locations() -> list[Path]:
    """Every project location Memar has made a session folder in that still exists, in the order recorded."""
    note_earlier_record()
    found: list[Path] = []
    for entry in read_entries():
        for each in entry.locations:
            location = Path(each)
            if location in found or not location.is_dir() or _inside(location, scratch_root()):
                continue
            found.append(location)
    return found


def locations_of(project: Path) -> list[Path]:
    """The session locations that are PROJECT's own and exist: the one its preferences set, and each one on its registry entry.

    A value its preferences hold that `new` would refuse or not use is passed
    over: listing makes nothing, so there is nothing to refuse. A recorded
    location is the entry's own: it lies where its project put it, which need
    not be inside the project's folder.
    """
    note_earlier_record()
    found: list[Path] = []
    preferred = configured_location(project)
    if preferred.is_dir() and _refused(project, preferred) is None:
        if not _inside(preferred, scratch_root()):
            found.append(preferred.resolve())
    for entry in read_entries():
        if not same_path(entry.path, project):
            continue
        for each in entry.locations:
            location = Path(each)
            if not location.is_dir() or _inside(location, scratch_root()) or same_path(location, project):
                continue
            if not any(same_path(location, known) for known in found):
                found.append(location)
    return found


def prune_registry() -> list[Path]:
    """Remove each recorded location whose folder no longer exists from its entry, and return those removed.

    The entry stays, and the registry is read again under its lock just before
    it is replaced, so a location a `new` recorded meanwhile is kept.
    """
    note_earlier_record()
    try:
        return forget_missing_locations()
    except OSError as error:
        print(f"warning: the project session locations could not be rewritten ({error})", file=sys.stderr)
        return []


def register(location: Path, project: Path | None = None) -> None:
    """Record LOCATION, once, on PROJECT's entry so the session verbs find its folders from any working directory.

    PROJECT is the project `new` works for. Given none, it is the git
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
        print(f"warning: the project session location could not be recorded ({stopped.code})", file=sys.stderr)
    except OSError as error:
        print(f"warning: the project session location could not be recorded ({error})", file=sys.stderr)


def note_earlier_record() -> None:
    """Say on stderr that the earlier record sessions.projects is there, is not read, and how its locations come back; nothing when it is not."""
    old = project_sessions_registry()
    if old.is_file():
        print(
            f"memar: {old} is the earlier record of project session locations and is not read; "
            f"{EARLIER_RECORD_REMEDY}",
            file=sys.stderr,
        )


def project_location_note(folder: Path) -> str:
    """The one line `new` prints for a session folder in a project's own location."""
    return (
        f"location: {folder.parent} is a project's own session location, set in its "
        f"{PREFERENCES_RELATIVE.as_posix()} or, when that sets none, temp/sessions/ in the project; Memar's sweep never moves a folder there — "
        "keeping or deleting it is the project's"
    )
