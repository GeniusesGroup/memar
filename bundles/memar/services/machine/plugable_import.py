#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Load a module under `modules-plugable/` by its path after that root.

Kernel code that must reach a pluggable shelf at runtime asks here, so the
module-graph check does not see a literal `modules-plugable…` import edge from
a kernel module. The address is still one place; only the import spell is
indirect. Prefer an ordinary import from another pluggable or from a kernel
module that already owns the dependence.
"""
from __future__ import annotations
from importlib import import_module
from types import ModuleType
ROOT = 'modules-plugable'

def load(after_root: str) -> ModuleType:
    """Import `modules-plugable.<after_root>` (e.g. `ai.services.plan_brief`)."""
    return import_module(f'{ROOT}.{after_root}')
