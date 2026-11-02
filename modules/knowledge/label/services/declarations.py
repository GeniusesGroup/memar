#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/declarations.py — the labels a project declares as code, found by walking its tree.

Each domain declares its own labels ([Label → Where labels are declared](../label.md#where-labels-are-declared)):
a module writes them in a Python file of its `labels/` folder as a Type named
`Label_<Word>` that subclasses `DeclaredLabel`
(`modules/knowledge/label/labels/declared_label.py`). Discovery finds those types;
where they are registered is not the file's choice, and here they are
registered in a `LabelRegistry` held for the run and kept in no store.

Why a walk and not an import. This module is a kernel module, and the modules
that declare labels are any of the project's, pluggable ones and bundles
among them; a kernel module never names a pluggable one
([Kernel Neutrality → The rule](../../modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)),
and a list of the declaring modules kept here would be a second copy of what
the tree already says. So the tree is walked for such files, and each is run
by its path. A file of a `labels/` folder that defines no `Label_*` DeclaredLabel
declares nothing here.

What the walk skips: a folder whose name begins with a dot (`.git`, and
`.agents`, whose task folders are records and not domains), and
`node_modules`, `__pycache__` and `temp`, which hold no declaration.
"""
from __future__ import annotations
import hashlib
import importlib.util
import os
from dataclasses import dataclass
from pathlib import Path
from machine.console import fail
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.primitive.label import LabelDefinition
FOLDER = 'labels'
NAME = 'Label_'
SKIPPED = frozenset({'node_modules', '__pycache__', 'temp'})
SKIP_FILES = frozenset({'__init__.py', 'declared_label.py'})

@dataclass(frozen=True)
class Declared:
    """One label's definition, with the file that declares it."""
    definition: LabelDefinition
    source: Path

def declaring_files(project: Path) -> list[Path]:
    """The Python files of PROJECT's `labels/` folders that define a Label_* DeclaredLabel, in path order."""
    found: list[Path] = []
    for folder, children, files in os.walk(project):
        children[:] = sorted((child for child in children if not child.startswith('.') and child not in SKIPPED))
        if Path(folder).name != FOLDER:
            continue
        for name in sorted(files):
            path = Path(folder) / name
            if name.endswith('.py') and name not in SKIP_FILES and name.startswith('Label_'):
                found.append(path)
    return found

def _run(path: Path) -> tuple[LabelDefinition, ...]:
    """The Label_* DeclaredLabel the file at PATH defines, run by its path."""
    name = '_memar_labels_' + hashlib.sha1(str(path).encode('utf-8')).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    found: list[LabelDefinition] = []
    for attr in vars(module).values():
        if isinstance(attr, type) and issubclass(attr, DeclaredLabel) and attr is not DeclaredLabel and attr.__name__.startswith('Label_'):
            found.append(attr.definition())
    if not found:
        fail(f'{path}: declare class Label_<Word>(DeclaredLabel); this file defines none')
    if len(found) != 1:
        fail(f'{path}: one Label_<Word> per file; this file holds {len(found)}')
    return tuple(found)

def declared(project: Path) -> tuple[Declared, ...]:
    """Every label PROJECT declares, file by file in path order."""
    return tuple((Declared(definition, path) for path in declaring_files(project) for definition in _run(path)))
