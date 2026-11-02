#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/declarations.py — the labels a project declares as code.

Each domain declares its own labels ([Label → Where labels are declared](../label.md#where-labels-are-declared)):
a module writes them in a Python file of its `labels/` folder as a Type named
`Label_<Word>` that subclasses `DeclaredLabel`. Discovery finds those files and
loads them into the in-memory `DeclaredLabel` registry; queries then read the
registry, not the tree again.

Why a tree scan and not a fixed import list. This module is a kernel module, and
the modules that declare labels are any of the project's ([Kernel Neutrality](
../../modularity/rules/kernel-neutrality/kernel-neutrality.md#the-rule)). The scan
is only for discovery; `taking` and kind helpers never walk the tree.

What the scan skips: a folder whose name begins with a dot (`.git`, `.agents`),
and `node_modules`, `__pycache__` and `temp`.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from machine.console import fail
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
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
    root = project.resolve()
    found: list[Path] = []
    for path in root.rglob('Label_*.py'):
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part.startswith('.') or part in SKIPPED for part in relative.parts):
            continue
        if path.parent.name != FOLDER or path.name in SKIP_FILES:
            continue
        found.append(path)
    return sorted(found)

def _run(path: Path) -> LabelDefinition:
    """Load PATH into the DeclaredLabel registry and return its definition."""
    try:
        declared = DeclaredLabel.import_path(path)
    except TypeError as refused:
        fail(str(refused))
    return declared.definition()

def declared(project: Path) -> tuple[Declared, ...]:
    """Every label PROJECT declares, file by file in path order; registry is filled as a side effect."""
    return tuple(Declared(_run(path), path) for path in declaring_files(project))
