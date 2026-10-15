#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_temp.py — where a session's temporary files go, said in one sentence.

A session's folder holds its record and the files its report links to; a draft
that is later appended elsewhere (a changelog record before it is added), or a
script's output that carries no content, is neither. Those go in the session's
`temp/` folder (`TEMP_FOLDER` below; `temp` is a general rule of Memar, not a module role), which `session_archive`
never keeps. An agent is told once, in the sentence below,
where a session is opened (`new`), claimed (`claim`, `claims`) and started
(`start`); the sentence is kept here, apart from `session_layout`, because the
claim service names the claim file that `session_layout` lists at a folder's
top, and so cannot import it.
"""
from __future__ import annotations

from pathlib import Path

TEMP_FOLDER = "temp"
"""The folder for what the work makes and the record does not need: a draft, a tool's output without content. A session's is never archived (`session_archive`). It is no module role (`module_folders`)."""


def ensure_temp_folder(folder: Path) -> None:
    """Make FOLDER's `temp/` when it is missing; never touch one that is there."""
    (folder / TEMP_FOLDER).mkdir(exist_ok=True)

TEMP_SENTENCE = (
    "Temporary files — a draft changelog record before it is appended, a script's output without content "
    f"value — go in {TEMP_FOLDER}/ of the session folder, which is never archived."
)
"""The one sentence that tells an agent where temporary files go."""
