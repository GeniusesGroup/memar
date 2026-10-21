#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/project/project.py — `memar project`: the projects Memar knows by name.

This file declares the verb and nothing else of its own. Each sub-verb is one
service on this shelf: `project_add`, `project_list`, `project_remove`, and
`project_find`; `project_registry` holds the file they share and `project_find`
the lookup other verbs call. Why there is a registry at all is said in
`project_registry`: a verb is always told its project, by path or by a name
this registry resolves, and never reads the folder it was started in.
"""
from __future__ import annotations
from typing import Callable
PROJECT_COMMAND = 'project'
SUMMARY = 'the projects Memar knows by name: add, list, remove, and find one by a name that need not be exact'
DESCRIPTION = "memar project — which folder a project's name is\n\nA task always names its project: by its folder, or by a name. Memar keeps the\nnames in temp/projects.log at the root of its own temp: one project a line,\nits folder and an array of names (the first is its own, the rest aliases in\nany language). Memar's own checkout is an entry named memar. Names are unique\nwithout regard to case."

def describe(verbs) -> Callable[[object], None]:
    """`memar project`, whose sub-verbs its capabilities declare."""
    verbs.add_parser(PROJECT_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
