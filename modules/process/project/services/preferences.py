#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/services/preferences.py — a project's Memar preferences: where they are, what they hold, and reading them.

What a project wants of Memar's tools is a `memar:` block in the project's own
manifest, `manifest.yaml` at its top folder: one indented `key: value` line per
key, each key named here. It is read by Memar's tools alone, never by an agent,
so it is data and not a document: no agent loads it, and nothing in it is
written for one. A preference agents should follow is a Memar rule or a line of
the project's AGENTS.md, not a key here.

    memar:
      sessions: work/sessions
      records: off

`sessions` is the folder new task folders are made in: a path relative to
the project's top folder, or an absolute one, but neither that top folder
itself nor a drive or filesystem root; unset, they are made in `.agents/tasks/`
inside the project, which git can stage so a branch switch does not drop them
silently. Memar's daily sweep never touches a task folder made in a project's
own location: keeping, committing, or deleting it is the project's. `records`
says whether a task's records — its whole folder except the claim, caches,
binary files, files over 256 KB that are not documents, and its own temp folder
— are kept on the records branch of the project's own repository by
`memar git archive-task-records` (and added by the sweep before it moves a
folder): `on` or `off`; unset, they are. Nothing is pushed. `most-characters` is
the most characters one printed part of a long text holds, the text `memar ai get-task-init-context` and `memar content get-act-context` print in ordered parts: a whole
number below the smallest output cut of the agent runtimes the project uses;
unset, Memar's default, `MOST_CHARACTERS` in machine/console_parts.py.
`normative_references` names the folders where the project's own lists of the
sections an act reads before it starts are kept, as Memar's rule Normative
References says: paths relative to the project's top folder, separated by
commas, each a folder inside the project and none the top folder itself.

The manifest is the project's own: `memar install` neither creates nor writes
it. The block is read without a YAML library, the way a plan's front matter is
(`session_plan`): the line `memar:` at the left margin, then the indented
`key: value` lines below it, up to the next line at the margin; a key left
empty, `sessions:` alone, reads as unset, and the rest of the manifest is not
read. A file that is absent, has no block, or cannot be read sets nothing: what
a project has not said is Memar's default.
"""
from __future__ import annotations
from enum import Enum
from pathlib import Path
from machine.console import fail
from machine.console_parts import MOST_FLAG
PREFERENCES_RELATIVE = Path('manifest.yaml')
BLOCK_KEY = 'memar'
NORMATIVE_REFERENCES_KEY = 'normative_references'
SESSIONS_KEY = 'sessions'
RECORDS_KEY = 'records'
MOST_CHARACTERS_KEY = MOST_FLAG.removeprefix('--')
FOLDER_SEPARATOR = ','

class Records(Enum):
    """What the `records` key may say: keep a session's records in the project, or not."""
    ON = 'on'
    OFF = 'off'

    @classmethod
    def listing(cls) -> str:
        return ', '.join((f'`{each.value}`' for each in cls))

def preferences_text(values: dict[str, str]) -> str:
    """The `memar:` block of a manifest setting VALUES, keyed as this file names the keys."""
    return ''.join([f'{BLOCK_KEY}:\n', *(f'  {key}: {value}\n' for key, value in values.items())])

def preferences_path(project: Path) -> Path:
    """PROJECT's preferences file, whether or not it is there."""
    return project / PREFERENCES_RELATIVE

def read_preferences(project: Path) -> dict[str, str]:
    """The keys PROJECT's preferences file sets; none when it is absent or cannot be read."""
    try:
        lines = preferences_path(project).read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    found: dict[str, str] = {}
    inside = False
    for line in lines:
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line[:1] not in (' ', '\t'):
            inside = line.split('#', 1)[0].strip() == f'{BLOCK_KEY}:'
            continue
        if inside and ':' in line:
            key, value = line.split(':', 1)
            value = value.strip()
            if value:
                found[key.strip()] = value
    return found

def sessions_location(project: Path) -> Path | None:
    """The folder PROJECT's session folders are made in, or None for Memar's own.

    A relative value is under PROJECT's top folder; an absolute one is used as
    it is.
    """
    value = read_preferences(project).get(SESSIONS_KEY, '').strip().strip('"\'').strip()
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
    value = read_preferences(project).get(MOST_CHARACTERS_KEY, '').strip().strip('"\'').strip()
    if not value:
        return None
    if not value.isdigit() or int(value) <= 0:
        fail(f'{preferences_path(project)}: {MOST_CHARACTERS_KEY} must be a positive whole number of characters, not {value!r}')
    return int(value)

def records_preference(project: Path) -> Records | None:
    """Whether PROJECT keeps its sessions' records: ON when its preferences say nothing, None for a value `records` may not take."""
    value = read_preferences(project).get(RECORDS_KEY, '').strip().strip('"\'').strip().lower()
    if not value:
        return Records.ON
    return next((each for each in Records if each.value == value), None)
