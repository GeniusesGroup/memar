#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""view/services/refresh.py — `memar view refresh`: build a project's view again from its store.

The verb reads the project's `view` key (the builder's module declares it), opens the class it names through `open` of
`bundles/memar` (`services/memory/memory.py`), and hands the `record` it returns, with the presentation registered for
the class, to `build` of `modules-plugable/computer/memory/store/view/view.py`. Nothing is imported until it runs.
"""
from __future__ import annotations
import argparse
import sys
from importlib import import_module
COMMAND = 'refresh'

def describe(verbs):
    parser = verbs.add_parser(COMMAND, help="build the project's view again from the committed nodes of its class", description="Build the folder the project's `view` key names (`class=folder`, the folder relative to the\nproject's top) from the committed nodes of that class, as the class's presentation shows\nthem. Only the files the builder wrote before are touched: a file changed by hand is\nrestored and counted, a file no node shows any more is removed. A folder version control\ndoes not ignore, or one holding a file the builder did not write, is refused and nothing\nis written. Exit 1 when the build is refused or the class cannot be opened.")
    import_module('modules.process.project.services.find').add_project_flags(parser, 'the project whose view to build', required=True)
    return run

def _refuse(said: str) -> int:
    print(f'memar view refresh: {said}', file=sys.stderr)
    return 1

def run(args: argparse.Namespace) -> int:
    find = import_module('modules.process.project.services.find')
    view = import_module('modules-plugable.computer.memory.store.view.view')
    preferences = import_module('modules.process.project.services.preferences')
    project = find.project_from_args(args)
    if project is None:
        return _refuse('name the project with --project or --project-path')
    where = preferences.preferences_path(project)
    chosen = view.view_preference(project)
    if chosen is None:
        return _refuse(f'`{view.VIEW_KEY}` in {where} is not one `class=folder` pair')
    if not chosen:
        return _refuse(f'the project defines no view: put `{view.VIEW_KEY}: <class>=<folder>` in the `{preferences.BLOCK_KEY}:` block of {where}')
    (class_name, folder), = chosen.items()
    shown = view.presentation(class_name)
    if shown is None:
        return _refuse(f'no presentation is registered for the class `{class_name}`, so nothing can show its nodes')
    memory = import_module('bundles.memar.services.memory.memory')
    record = import_module('modules-plugable.computer.memory.store.record.record')
    opened = memory.open(project, class_name, record.Needs())
    if isinstance(opened, memory.OpenRefused):
        return _refuse(opened.detail or opened.reason.summary())
    try:
        built = view.build(opened, shown, project / folder)
    finally:
        close = getattr(opened.store, 'close', None)
        if callable(close):
            close()
    if isinstance(built, view.ViewRefused):
        return _refuse(built.summary())
    print(f'{project / folder}: {built.summary()}')
    return 0
