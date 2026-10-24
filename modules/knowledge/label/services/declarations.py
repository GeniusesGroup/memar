#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/declarations.py — the labels a project declares as code, found by walking its tree.

Each domain declares its own labels ([Label → Where labels are declared](../label.md#where-labels-are-declared)):
a module writes them in a Python file of its `labels/` folder, as a
module-level `LABELS`, a tuple of `LabelDefinition`s
(`modules/knowledge/label/primitive/label.py`). The file only returns
the values; where they are registered is not its choice, and here they are
registered in a `LabelRegistry` held for the run and kept in no store.

Why a walk and not an import. This module is a kernel module, and the modules
that declare labels are any of the project's, pluggable ones and bundles
among them; a kernel module never names a pluggable one
([Kernel Neutrality → The rule](../../modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)),
and a list of the declaring modules kept here would be a second copy of what
the tree already says. So the tree is walked for such files, and each is run
by its path. A file of a `labels/` folder that assigns no `LABELS` declares
nothing here: a kind (`TaskKind`, `Topic`) is a type its readers import.

What the walk skips: a folder whose name begins with a dot (`.git`, and
`.agents`, whose task folders are records and not domains), and
`node_modules`, `__pycache__` and `temp`, which hold no declaration.
"""
from __future__ import annotations
import hashlib
import importlib.util
import os
import re
from dataclasses import dataclass
from pathlib import Path
from machine.console import fail
from modules.knowledge.label.primitive.label import LabelDefinition
FOLDER = 'labels'
NAME = 'LABELS'
SKIPPED = frozenset({'node_modules', '__pycache__', 'temp'})
_ASSIGNED = re.compile(f'^{NAME}\\s*(?::[^=]*)?=', re.MULTILINE)

@dataclass(frozen=True)
class Declared:
    """One label's definition, with the file that declares it."""
    definition: LabelDefinition
    source: Path

def declaring_files(project: Path) -> list[Path]:
    """The Python files of PROJECT's `labels/` folders that assign `LABELS`, in path order."""
    found: list[Path] = []
    for folder, children, files in os.walk(project):
        children[:] = sorted((child for child in children if not child.startswith('.') and child not in SKIPPED))
        if Path(folder).name != FOLDER:
            continue
        for name in sorted(files):
            path = Path(folder) / name
            if name.endswith('.py') and name != '__init__.py' and _ASSIGNED.search(path.read_text(encoding='utf-8')):
                found.append(path)
    return found

def _run(path: Path) -> tuple[LabelDefinition, ...]:
    """The `LABELS` the file at PATH returns, run by its path; refused when it holds anything but definitions."""
    name = '_memar_labels_' + hashlib.sha1(str(path).encode('utf-8')).hexdigest()
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    labels = getattr(module, NAME, ())
    if not isinstance(labels, tuple) or not all((isinstance(item, LabelDefinition) for item in labels)):
        fail(f'{path}: {NAME} is a tuple of LabelDefinition, as `topic()` returns; it holds something else')
    return labels

def declared(project: Path) -> tuple[Declared, ...]:
    """Every label PROJECT declares, file by file in path order."""
    return tuple((Declared(definition, path) for path in declaring_files(project) for definition in _run(path)))
