#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/project_preferences.py — a project's Memar preferences: where they are, what they hold, and reading them.

A project Memar is installed into has a `.agents/memar/README.md` that
`install_project` writes again on every install, so nothing the project says
there survives the next one. What the project wants of Memar goes in the file
beside it, `preferences.md`, which an install creates when it is absent and
never touches again — in the Memar repository too, whose README is written by
hand and skipped.

The file has two readers. Its front matter holds the keys Memar's tools read,
each named here; its body is free prose for the agents that work on the
project, which no tool reads. Both the path and the keys are this file's, so
the installer that writes the file and the session service that reads it
cannot disagree about either.

The front matter is read the way a session's plan is (`session_plan`), one
`key: value` per line, so a key left empty, `sessions:` alone, reads as unset.
A file that is absent or cannot be read sets nothing: what a project has not
said is Memar's default.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path

from machine.console import fail
from machine.console_parts import MOST_FLAG
from machine.fs_memar import CONSUMER_README_RELATIVE, RECORDS_BRANCH, RECORDS_RELATIVE
from services.normative_references import PREFERENCE, Place
from services.session_plan import front_matter

PREFERENCES_RELATIVE = CONSUMER_README_RELATIVE.with_name("preferences.md")
# The folder new session folders are made in, relative to the project's top
# folder or absolute; unset, they are made in temp/sessions/ inside the project (Memar's own, for the Memar checkout).
SESSIONS_KEY = "sessions"
# Whether a session's records are kept on the project's records branch
# (`session_archive`); unset, they are.
RECORDS_KEY = "records"
# The most characters one printed part of a long text holds (`machine/console_parts.py`),
# for the runtimes this project uses; unset, Memar's default. The key is the flag's name.
MOST_CHARACTERS_KEY = MOST_FLAG.removeprefix("--")
# The folders, comma-separated and relative to the project's top folder, where its own
# normative-references lists are read (`services/normative_references.py`); its name is `PREFERENCE`.
FOLDER_SEPARATOR = ","


class Records(Enum):
    """What the `records` key may say: keep a session's records in the project, or not."""

    ON = "on"
    OFF = "off"

    @classmethod
    def listing(cls) -> str:
        return ", ".join(f"`{each.value}`" for each in cls)


PREFERENCES_TEXT = f"""---
{SESSIONS_KEY}:
{RECORDS_KEY}:
{MOST_CHARACTERS_KEY}:
{PREFERENCE}:
---
# Memar preferences
This file is this project's own: `memar install` creates it when it is absent and never rewrites it, unlike the README beside it, which an install rewrites. The front matter holds what Memar's tools read. `{SESSIONS_KEY}` is the folder new session folders are made in: a path relative to the project's top folder, or an absolute one, but neither that top folder itself nor a drive or filesystem root; left empty, they are made in temp/sessions/ inside the project, which its VCS should ignore. Memar's daily sweep never touches a session folder made in the `{SESSIONS_KEY}` folder: keeping, committing, or deleting it is the project's. `{RECORDS_KEY}` says whether a session's records — its whole folder except the claim, caches, binary files, files over 256 KB that are not documents, and its own temp folder — are kept on the branch {RECORDS_BRANCH} of the project's own repository, at {RECORDS_RELATIVE.as_posix()}/<id>/ there, by `memar session archive` (and added by the sweep before it moves a folder): {Records.listing()}; left empty, they are. Nothing is pushed. `{MOST_CHARACTERS_KEY}` is the most characters one printed part of a long text holds, the text `memar session start` and `memar content context` print in ordered parts: a whole number below the smallest output cut of the agent runtimes this project uses; left empty, Memar's default, `MOST_CHARACTERS` in Memar's .agents/scripts/machine/console_parts.py. `{PREFERENCE}` names the folders where this project's own lists of the sections an act reads before it starts are kept, as Memar's rule Normative References says: paths relative to the project's top folder, separated by commas, each a folder inside the project and none the top folder itself; a list is read only directly in a folder named here, and a file named like a list anywhere else is not read; left empty, the project has no lists of its own and its sessions read Memar's alone. Below this paragraph, write any preference agents should follow on this project.
"""


def preferences_path(project: Path) -> Path:
    """PROJECT's preferences file, whether or not it is there."""
    return project / PREFERENCES_RELATIVE


def read_preferences(project: Path) -> dict[str, str]:
    """The keys PROJECT's preferences file sets; none when it is absent or cannot be read."""
    try:
        lines = preferences_path(project).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    front, _ = front_matter(lines)
    return front or {}


def sessions_location(project: Path) -> Path | None:
    """The folder PROJECT's session folders are made in, or None for Memar's own.

    A relative value is under PROJECT's top folder; an absolute one is used as
    it is.
    """
    value = read_preferences(project).get(SESSIONS_KEY, "").strip().strip("\"'").strip()
    if not value:
        return None
    return project / value


def most_characters_preference(project: Path | None) -> int | None:
    """The most characters a printed part holds that PROJECT's preferences set; None when PROJECT is None or sets none.

    A value that is not a positive whole number is refused, naming the file:
    a bound silently dropped would cut the text where the project said it must not.
    """
    if project is None:
        return None
    value = read_preferences(project).get(MOST_CHARACTERS_KEY, "").strip().strip("\"'").strip()
    if not value:
        return None
    if not value.isdigit() or int(value) <= 0:
        fail(f"{preferences_path(project)}: {MOST_CHARACTERS_KEY} must be a positive whole number of characters, not {value!r}")
    return int(value)


def records_preference(project: Path) -> Records | None:
    """Whether PROJECT keeps its sessions' records: ON when its preferences say nothing, None for a value `records` may not take."""
    value = read_preferences(project).get(RECORDS_KEY, "").strip().strip("\"'").strip().lower()
    if not value:
        return Records.ON
    return next((each for each in Records if each.value == value), None)


def normative_reference_places(project: Path | None, memar: Path) -> tuple[list[Place], list[str]]:
    """The places PROJECT's preferences declare for its own normative-references lists, and the problems with what they name.

    One place for each folder the key names, in the order named, under the project's folder name and with MEMAR, the
    Memar checkout, as the checkout its links to Memar's published pages are read from. A folder that is not a folder, is
    the top folder itself, is an absolute path or leaves the project is a problem naming the file and the value, and gives no
    place; the others still do. None for no project, or an empty or absent key.
    """
    if project is None:
        return [], []
    value = read_preferences(project).get(PREFERENCE, "").strip().strip("\"'").strip()
    top = project.resolve()
    places: list[Place] = []
    problems: list[str] = []
    for named in (each.strip() for each in value.split(FOLDER_SEPARATOR)):
        if not named:
            continue
        folder = (top / named).resolve()
        if Path(named).is_absolute() or named.startswith(("/", "\\")):
            refused = "an absolute path; name a folder relative to the project's top folder"
        elif folder == top:
            refused = "the project's top folder itself"
        elif top not in folder.parents:
            refused = "a folder outside the project"
        elif not folder.is_dir():
            refused = "not a folder"
        else:
            place = Place(project.name, project, project / named, memar)
            if place not in places:
                places.append(place)
            continue
        problems.append(f"{preferences_path(project).as_posix()}: {PREFERENCE} {named!r} is {refused}")
    return places, problems
