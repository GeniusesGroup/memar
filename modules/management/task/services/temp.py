#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/services/temp.py — where a task's temporary files go, said in one sentence.

A task's folder holds its record and the files its report links to; a draft
that is later appended elsewhere (a changelog record before it is added), or a
script's output that carries no content, is neither. Those go in the task's
`temp/` folder (`TEMP_FOLDER`, named once in `modules-plugable/computer/filesystem/services/fs_memar.py`, which a
task is given with the other folders of its layout, `task_layout`), which
`task_archive` never keeps. An agent is told once, in the sentence below,
where a task is opened (`ensure`), claimed (`claim`, `claims`) and started
(`start`); the sentence is kept here, apart from `task_layout`, because the
claim service names the claim file that `task_layout` lists at a folder's
top, and so cannot import it.
"""
from __future__ import annotations
from machine.plugable_import import load as plugable_load
_m_fs_memar = plugable_load('computer.filesystem.services.fs_memar')
TEMP_FOLDER = _m_fs_memar.TEMP_FOLDER
TEMP_SENTENCE = f"Temporary files — a draft changelog record before it is appended, a script's output without content value — go in {TEMP_FOLDER}/ of the task folder, which is never archived."
'The one sentence that tells an agent where temporary files go.'
