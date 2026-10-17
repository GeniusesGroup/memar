#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_temp.py — where a session's temporary files go, said in one sentence.

A session's folder holds its record and the files its report links to; a draft
that is later appended elsewhere (a changelog record before it is added), or a
script's output that carries no content, is neither. Those go in the session's
`temp/` role folder (`module_folders.TEMP_FOLDER`, which a session is given
with its other role folders, since every session is a module), which
`session_archive` never keeps. An agent is told once, in the sentence below,
where a session is opened (`new`), claimed (`claim`, `claims`) and started
(`start`); the sentence is kept here, apart from `session_layout`, because the
claim service names the claim file that `session_layout` lists at a folder's
top, and so cannot import it.
"""
from __future__ import annotations

from services.module_folders import TEMP_FOLDER

TEMP_SENTENCE = (
    "Temporary files — a draft changelog record before it is appended, a script's output without content "
    f"value — go in {TEMP_FOLDER}/ of the session folder, which is never archived."
)
"""The one sentence that tells an agent where temporary files go."""
