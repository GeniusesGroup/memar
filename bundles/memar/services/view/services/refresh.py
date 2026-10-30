#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import argparse
import sys
from importlib import import_module
COMMAND = 'refresh'

def describe(verbs):
    parser = verbs.add_parser(COMMAND, help="build the project's view again from the committed nodes of its class", description="Build the folder the project's `view` key names (`class=folder`, the folder relative to the\nproject's top) from the committed nodes of that class, as the class's presentation shows\nthem. Only the files the builder wrote before are touched: a file changed by hand is\nrestored and counted, a file no node shows any more is removed. A folder version control\ndoes not ignore, or one holding a file the builder did not write, is refused and nothing\nis written. Exit 1 when the build is refused or the class cannot be opened.")
    import_module('modules.process.project.services.find').add_project_flags(parser, 'the project whose view to build', required=True)
    return run

def refresh(project):
    errors = import_module('bundles.memar.services.view.errors.errors')
    if project is None:
        return errors.RefreshRefused(errors.RefreshRefusal.NO_PROJECT, 'name the project with --project or --project-path')
    view = import_module('modules-plugable.computer.memory.store.view.view')
    view_errors = import_module('modules-plugable.computer.memory.store.view.errors.errors')
    preferences = import_module('modules.process.project.services.preferences')
    where = preferences.preferences_path(project)
    chosen = view.view_preference(project)
    if chosen is None:
        return view_errors.BadPreference(f'`{view.VIEW_KEY}` in {where}')
    if not chosen:
        return errors.RefreshRefused(errors.RefreshRefusal.NO_VIEW, f'put `{view.VIEW_KEY}: <class>=<folder>` in the `{preferences.BLOCK_KEY}:` block of {where}')
    (class_name, folder), = chosen.items()
    shown = view.presentation(class_name)
    if shown is None:
        return errors.RefreshRefused(errors.RefreshRefusal.NO_PRESENTATION, f'the class `{class_name}` has none, so nothing can show its nodes')
    memory = import_module('bundles.memar.services.memory.memory')
    record = import_module('modules-plugable.computer.memory.store.record.record')
    opened = memory.open(project, class_name, record.Needs())
    if isinstance(opened, memory.OpenRefused):
        return opened
    try:
        return view.build(opened, shown, project / folder)
    finally:
        opened.close()

def _refuse(said: str) -> int:
    print(f'memar view refresh: {said}', file=sys.stderr)
    return 1

def run(args: argparse.Namespace) -> int:
    find = import_module('modules.process.project.services.find')
    view = import_module('modules-plugable.computer.memory.store.view.view')
    memory = import_module('bundles.memar.services.memory.memory')
    project = find.project_from_args(args)
    answer = refresh(project)
    if isinstance(answer, view.Built):
        (folder,) = view.view_preference(project).values()
        print(f'{project / folder}: {answer.summary()}')
        return 0
    if isinstance(answer, memory.OpenRefused):
        return _refuse(answer.detail or answer.reason.summary())
    return _refuse(answer.summary())
