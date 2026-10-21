#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules-plugable/computer/git/git.py — `memar git`: archive-task-records, show-task-records, sweep-idle-task-folders, trash-task-folder.

Groups git-backed task-folder record verbs that left process/task. Lives under
modules-plugable/computer as a sibling shelf of filesystem/, not inside it.
"""
from __future__ import annotations
GIT_COMMAND = 'git'
SUMMARY = 'keep, show, sweep, and trash task-folder records on the records branch'
DESCRIPTION = "memar git — task folder records on the project's records branch\n\n`archive-task-records` keeps a finished task's records; `show-task-records` prints them from the folder or\nthe branch; `sweep-idle-task-folders` sweeps idle folders; `trash-task-folder` moves an archived folder to Trash.\nHelpers keep, branch, and log sit beside these verbs.\n\nEach verb below says what it does in its own --help.\n"

def describe(verbs) -> None:
    """`memar git`, which only groups its verbs."""
    verbs.add_parser(GIT_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
