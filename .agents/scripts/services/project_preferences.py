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

from pathlib import Path

from machine.fs_memar import CONSUMER_README_RELATIVE
from services.session_plan import front_matter

PREFERENCES_RELATIVE = CONSUMER_README_RELATIVE.with_name("preferences.md")
# The folder new session folders are made in, relative to the project's top
# folder or absolute; unset, they are made in Memar's own temp/sessions/.
SESSIONS_KEY = "sessions"

PREFERENCES_TEXT = f"""---
{SESSIONS_KEY}:
---
# Memar preferences
This file is this project's own: `memar install` creates it when it is absent and never rewrites it, unlike the README beside it, which an install rewrites. The front matter holds what Memar's tools read. `{SESSIONS_KEY}` is the folder new session folders are made in: a path relative to the project's top folder, or an absolute one, but neither that top folder itself nor a drive or filesystem root; left empty, they are made in Memar's own temp/sessions/. Memar's daily sweep never touches a session folder made in the `{SESSIONS_KEY}` folder: keeping, committing, or deleting it is the project's. Below this paragraph, write any preference agents should follow on this project.
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
