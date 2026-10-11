#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_location.py — where a session's folder is made: Memar's own temp/sessions/, or the project's own session location.

A session folder is Memar's scratch by default, made under the Memar root
(`machine/fs_memar.py`) and swept from there once its task is done. A project
may want its session folders in the project instead — to keep them, commit
them, or read them beside its own work — and says so with the `sessions` key
of its preferences (`project_preferences`). Those folders are the project's,
not Memar's: the sweep (`session_gc`) and the move out of temp/
(`session_migrate`) never touch them, and keeping or deleting one is the
project's business, which `new` says each time it makes or continues one there
and `gc` says by naming the locations it did not sweep.

A project's location is outside every Memar root, so the other session verbs —
`list`, `close`, `new --session-id` — could not find a folder there from
another working directory without searching the disk. Memar keeps the
locations instead, one path a line, in a file of its own state whose path
`machine/fs_memar.py` owns: `new` appends a location the first time it makes
or continues a session there, and a location that no longer exists is passed
over rather than removed, since it may be a drive that is not mounted now.

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

import sys
from pathlib import Path

from machine.console import fail
from machine.fs_memar import project_sessions_registry, scratch_root
from services.project_preferences import PREFERENCES_RELATIVE, SESSIONS_KEY, preferences_path, sessions_location


def _inside(path: Path, root: Path) -> bool:
    try:
        return path.resolve().is_relative_to(root.resolve())
    except OSError:
        return False


def project_location(project: Path) -> Path | None:
    """The folder PROJECT's preferences place its session folders in, or None for Memar's own.

    A value that resolves to the project's top folder itself, or to a drive or
    filesystem root, is refused before anything is made: the session folders
    would lie among the project's own folders, or the disk's.
    """
    location = sessions_location(project)
    if location is None:
        return None
    resolved = location.resolve()
    if resolved == project.resolve() or resolved == Path(resolved.anchor):
        what = "the project's top folder" if resolved == project.resolve() else "a drive or filesystem root"
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
    try:
        lines = project_sessions_registry().read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return []
    found: list[Path] = []
    for line in lines:
        if not line.strip():
            continue
        location = Path(line.strip())
        if location in found or not location.is_dir() or _inside(location, scratch_root()):
            continue
        found.append(location)
    return found


def register(location: Path) -> None:
    """Record LOCATION, once, so the session verbs find its folders from any working directory."""
    registry = project_sessions_registry()
    entry = str(location.resolve())
    try:
        known = registry.read_text(encoding="utf-8").splitlines() if registry.is_file() else []
        if entry in known:
            return
        with registry.open("a", encoding="utf-8", newline="\n") as file:
            file.write(entry + "\n")
    except (OSError, UnicodeDecodeError) as error:
        print(f"warning: the project session location could not be recorded ({error})", file=sys.stderr)


def project_location_note(folder: Path) -> str:
    """The one line `new` prints for a session folder in a project's own location."""
    return (
        f"location: {folder.parent} is a project's own session location, set in its "
        f"{PREFERENCES_RELATIVE.as_posix()}; Memar's sweep never moves a folder there — "
        "keeping or deleting it is the project's"
    )
