#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/project_registry.py — the file that says which folder a project's name is.

Why a registry. A verb that acts on a project must be told which one: no script
keeps a default project path, and none reads the folder it was started in,
because both are guesses that are right on the day they are written. A name
told to a service is not a guess, so the names live in one file,
temp/projects.log at the root of Memar's temp (its path is `machine/fs_memar.py`'s),
and `project_find` turns a word into a folder through it.

The format is one project a line, each line a JSON object with the folder and
an array of names: `{"path": "C:\\\\work\\\\org", "names": ["organization", "org", "سازمان"]}`.
A line may also hold `"locations"`, an array of the folders outside Memar's temp
where the project's session folders are made (`session_location`); it is absent
when there are none, and a damaged value costs the locations, not the entry.
JSON, not a column format, because names are free text in any language and a
separator character would one day be inside one. The first name is the
project's own; the rest are aliases, in any language. Names are unique across
the whole file without regard to case or Unicode composition, so a word names
at most one project; adding a project already there (the same folder) merges
names into its line instead of making a second.

The file is rewritten whole through a temporary file beside it and an atomic
replace, under a short lock, so a reader never sees half a line and two agents
adding at once lose neither. A missing or unreadable file reads as empty, and
lines that are not entries are skipped: a damaged registry costs the names it
damaged, never the verb. Memar's own checkout is an entry named memar
(`ensure_memar_entry`).

This file declares no verb; `project_add`, `project_list`, `project_remove`, and
`project_find` do, and share what is here.
"""
from __future__ import annotations

import json
import os
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path

from machine.console import fail
from machine.fs_lock import try_lock
import machine.fs_memar as memar_fs
from machine.fs_memar import projects_log

MEMAR_NAME = "memar"
LOCK_SUFFIX = ".lock"
LOCK_WAIT_SECONDS = 10.0
LOCK_STALE_SECONDS = 30.0
LOCK_POLL_SECONDS = 0.05


@dataclass(frozen=True)
class Entry:
    """One project: its folder as text, and its names, the project's own first."""

    path: str
    names: tuple[str, ...]
    locations: tuple[str, ...] = ()


def normalized(text: str) -> str:
    """TEXT as names are compared: Unicode-normalised (NFKC), case-folded, trimmed."""
    return unicodedata.normalize("NFKC", text).strip().casefold()


def path_key(path: Path | str) -> str:
    """The form in which two spellings of one folder are equal."""
    return os.path.normcase(str(Path(path).resolve()))


def _entry_of(line: str) -> Entry | None:
    try:
        record = json.loads(line)
    except ValueError:
        return None
    if not isinstance(record, dict):
        return None
    path, names = record.get("path"), record.get("names")
    if not isinstance(path, str) or not path or not isinstance(names, list):
        return None
    kept = tuple(name.strip() for name in names if isinstance(name, str) and name.strip())
    where = record.get("locations")
    places = tuple(each for each in where if isinstance(each, str) and each) if isinstance(where, list) else ()
    return Entry(path, kept, places) if kept else None


def read_entries() -> list[Entry]:
    """The registered projects in the order added; none when the file is missing or unreadable."""
    try:
        text = projects_log().read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return []
    return [entry for entry in map(_entry_of, text.splitlines()) if entry is not None]


def _line(entry: Entry) -> str:
    record = {"path": entry.path, "names": list(entry.names)}
    if entry.locations:
        record["locations"] = list(entry.locations)
    return json.dumps(record, ensure_ascii=False)


def _write(entries: list[Entry]) -> None:
    target = projects_log()
    temporary = target.with_name(f"{target.name}.{os.getpid()}.tmp")
    text = "".join(_line(entry) + "\n" for entry in entries)
    try:
        temporary.write_text(text, encoding="utf-8", newline="\n")
        os.replace(temporary, target)
    finally:
        try:
            temporary.unlink()
        except OSError:
            pass


def _update(change):
    """Run CHANGE(entries) -> (entries, result) under the registry's lock and write the entries it returns."""
    target = projects_log()
    lock = target.with_name(target.name + LOCK_SUFFIX)
    deadline = time.monotonic() + LOCK_WAIT_SECONDS
    while not try_lock(lock, LOCK_STALE_SECONDS):
        if time.monotonic() > deadline:
            fail(f"the projects registry {target} is locked by another run; if none is running, remove {lock}")
        time.sleep(LOCK_POLL_SECONDS)
    try:
        entries, result = change(read_entries())
        if entries is not None:
            _write(entries)
        return result
    finally:
        try:
            lock.unlink()
        except OSError:
            pass


def _distinct(names: list[str]) -> list[str]:
    seen: dict[str, str] = {}
    for name in names:
        seen.setdefault(normalized(name), name.strip())
    return list(seen.values())


def add_project(name: str, path: Path | str, aliases=()) -> Entry:
    """Register the folder PATH under NAME and ALIASES, merging into its line when it is there.

    Refused: a blank name, a path that is no folder, and any name already
    another project's, whatever its case. Returns the entry as stored.
    """
    names = _distinct([name, *aliases])
    if not names or not normalized(name):
        fail("a project needs a name; give NAME as the first argument")
    if any(not normalized(each) for each in names):
        fail("an alias cannot be blank")
    folder = Path(path).resolve()
    if not folder.is_dir():
        fail(f"{path} is not a folder, so no project can be registered there")

    def change(entries: list[Entry]):
        mine = path_key(folder)
        for entry in entries:
            if path_key(entry.path) == mine:
                continue
            taken = {normalized(each) for each in entry.names}
            for wanted in names:
                if normalized(wanted) in taken:
                    fail(f"the name {wanted} is already the project {entry.names[0]} at {entry.path}; choose another")
        merged: Entry | None = None
        rest: list[Entry] = []
        for entry in entries:
            if path_key(entry.path) == mine:
                merged = Entry(entry.path, tuple(_distinct([*entry.names, *names])), entry.locations)
                rest.append(merged)
            else:
                rest.append(entry)
        if merged is None:
            merged = Entry(str(folder), tuple(names))
            rest.append(merged)
        return rest, merged

    return _update(change)


def add_location(project: Path | str, location: Path | str) -> Entry:
    """Record LOCATION, a folder holding PROJECT's session folders, on PROJECT's entry, once.

    A project with no entry gets one, named from its folder's name; a name
    another project already holds, or a folder with no name, is refused with the
    holder named, and nothing is renamed or stored.
    """
    folder = Path(project).resolve()
    place = str(Path(location).resolve())

    def change(entries: list[Entry]):
        mine = path_key(folder)
        for index, entry in enumerate(entries):
            if path_key(entry.path) != mine:
                continue
            if any(path_key(each) == path_key(place) for each in entry.locations):
                return None, entry
            changed = Entry(entry.path, entry.names, (*entry.locations, place))
            return [*entries[:index], changed, *entries[index + 1 :]], changed
        name = folder.name
        if not normalized(name):
            fail(f"the folder {folder} has no name to register its project under; use `memar project add NAME PATH`")
        for entry in entries:
            if normalized(name) in {normalized(each) for each in entry.names}:
                fail(
                    f"the name {name} is already the project {entry.names[0]} at {entry.path}, so {folder} "
                    f"was not registered with its session location {place}; use `memar project add NAME {folder}` with another name"
                )
        made = Entry(str(folder), (name,), (place,))
        return [*entries, made], made

    return _update(change)


def forget_missing_locations() -> list[Path]:
    """Remove from every entry each location whose folder is not there, and return those removed; an entry stays whatever it holds."""
    removed: list[Path] = []

    def change(entries: list[Entry]):
        rewritten: list[Entry] = []
        for entry in entries:
            gone = [each for each in entry.locations if not Path(each).is_dir()]
            removed.extend(Path(each) for each in gone)
            rewritten.append(Entry(entry.path, entry.names, tuple(each for each in entry.locations if each not in gone)))
        return (rewritten if removed else None), None

    _update(change)
    return removed


def remove_project(word: str) -> Entry:
    """Unregister the project WORD names (a name or alias in any case, or its folder); the folder is untouched."""
    key = normalized(word)

    def change(entries: list[Entry]):
        for entry in entries:
            if key in {normalized(each) for each in entry.names} or (Path(word).is_absolute() and path_key(entry.path) == path_key(word)):
                return [other for other in entries if other is not entry], entry
        fail(f"no registered project is named {word}; `memar project list` shows them")

    return _update(change)


def ensure_memar_entry() -> None:
    """Make sure Memar's own checkout is an entry, named memar; leave a taken name or an unwritable file alone."""
    root = memar_fs.memar_root().resolve()
    if any(path_key(entry.path) == path_key(root) for entry in read_entries()):
        return
    try:
        add_project(MEMAR_NAME, root)
    except (SystemExit, OSError):
        pass
