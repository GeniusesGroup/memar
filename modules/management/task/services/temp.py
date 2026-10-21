#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/temp.py — where a session's temporary files go, said in one sentence.

A session's folder holds its record and the files its report links to; a draft
that is later appended elsewhere (a changelog record before it is added), or a
script's output that carries no content, is neither. Those go in the session's
`temp/` folder (`TEMP_FOLDER`, named once in `modules-plugable/computer/filesystem/services/fs_memar.py`, which a
session is given with the other folders of its layout, `session_layout`), which
`session_archive` never keeps. An agent is told once, in the sentence below,
where a session is opened (`new`), claimed (`claim`, `claims`) and started
(`start`); the sentence is kept here, apart from `session_layout`, because the
claim service names the claim file that `session_layout` lists at a folder's
top, and so cannot import it.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
TEMP_SENTENCE = f"Temporary files — a draft changelog record before it is appended, a script's output without content value — go in {TEMP_FOLDER}/ of the session folder, which is never archived."
'The one sentence that tells an agent where temporary files go.'
