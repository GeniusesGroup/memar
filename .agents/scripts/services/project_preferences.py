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

from machine.fs_memar import CONSUMER_README_RELATIVE, RECORDS_RELATIVE
from services.session_plan import front_matter

PREFERENCES_RELATIVE = CONSUMER_README_RELATIVE.with_name("preferences.md")
# The folder new session folders are made in, relative to the project's top
# folder or absolute; unset, they are made in temp/sessions/ inside the project (Memar's own, for the Memar checkout).
SESSIONS_KEY = "sessions"
# Whether a finished session's records are kept in the project, to be committed
# with its work (`session_archive`); unset, they are (owner, 2026-10-14).
RECORDS_KEY = "records"


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
---
# Memar preferences
This file is this project's own: `memar install` creates it when it is absent and never rewrites it, unlike the README beside it, which an install rewrites. The front matter holds what Memar's tools read. `{SESSIONS_KEY}` is the folder new session folders are made in: a path relative to the project's top folder, or an absolute one, but neither that top folder itself nor a drive or filesystem root; left empty, they are made in temp/sessions/ inside the project, which its VCS should ignore. Memar's daily sweep never touches a session folder made in the `{SESSIONS_KEY}` folder: keeping, committing, or deleting it is the project's. `{RECORDS_KEY}` says whether a session's records — its plan, its report, and the files its report links to — are copied into {RECORDS_RELATIVE.as_posix()}/ in the project, to be committed with the task's work, before its folder is closed or swept: {Records.listing()}; left empty, they are. Below this paragraph, write any preference agents should follow on this project.
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


def records_preference(project: Path) -> Records | None:
    """Whether PROJECT keeps its sessions' records: ON when its preferences say nothing, None for a value `records` may not take."""
    value = read_preferences(project).get(RECORDS_KEY, "").strip().strip("\"'").strip().lower()
    if not value:
        return Records.ON
    return next((each for each in Records if each.value == value), None)
