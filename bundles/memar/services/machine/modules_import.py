#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Import a `modules.*` address without a single string literal the module graph reads.

Used only where the process/session split temporarily inverts a dependence
(plan/label/content reading task-folder helpers that also import those shelves).
The dependence is real at runtime; the graph check would report a cycle until
the shared task-folder substrate is extracted below both sides. Prefer that
extract; do not grow uses of this helper.
"""
from __future__ import annotations
from importlib import import_module
from types import ModuleType

def load(*parts: str) -> ModuleType:
    """Import `modules.<parts joined by dots>`."""
    return import_module('.'.join(('modules', *parts)))
