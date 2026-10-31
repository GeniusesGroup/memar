#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import re
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any
STORE_CAPSULES = 'modules-plugable.computer.memory.store'
BIND = 'bind'
_m_errors = import_module('bundles.memar.services.memory.errors.errors')
_m_store_errors = import_module('modules.computer.memory.store.errors.errors')
OpeningRefusal = _m_errors.OpeningRefusal
OpenRefused = _m_errors.OpenRefused
CAPABILITY_NAME = re.compile('[a-z0-9]+(?:-[a-z0-9]+)*')

def adapter_module(name: str) -> ModuleType | None:
    if not CAPABILITY_NAME.fullmatch(name):
        return None
    try:
        module = import_module(f'{STORE_CAPSULES}.{name}.{name}')
    except ImportError:
        return None
    return module if callable(getattr(module, BIND, None)) else None

def _close(store: Any) -> None:
    close = getattr(store, 'close', None)
    if callable(close):
        close()

def _shares(module: ModuleType, project: Path, other: str, adapter: Any) -> bool:
    try:
        return module.bind(project, other).store == adapter.store
    except _m_store_errors.Raised:
        return False

def open(project: Path, class_name: str, needs: Any) -> Any:
    preferences = import_module('modules.computer.software.edges.manifest.services.preferences')
    record = import_module(f'{STORE_CAPSULES}.record.record')
    where = preferences.preferences_path(project)
    bindings = preferences.memory_preference(project)
    if bindings is None:
        return OpenRefused(OpeningRefusal.MALFORMED, f'`{preferences.MEMORY_KEY}` in {where} is not `class=adapter` pairs separated by commas, each class once, so `{class_name}` cannot be opened')
    if class_name not in bindings:
        line = preferences.memory_binding_text({**bindings, class_name: '<adapter>'})
        return OpenRefused(OpeningRefusal.NOT_BOUND, f'the class `{class_name}` is bound to no adapter: put `{preferences.MEMORY_KEY}: {line}` in the `{preferences.BLOCK_KEY}:` block of {where}')
    name = bindings[class_name]
    module = adapter_module(name)
    if module is None:
        return OpenRefused(OpeningRefusal.MALFORMED, f'the class `{class_name}` is bound to `{name}` in {where}, and no module at {STORE_CAPSULES} of that name offers `{BIND}`')
    adapter = module.bind(project, class_name)
    others = sorted((other for other, bound in bindings.items() if other != class_name and bound == name and _shares(module, project, other, adapter)))
    if others:
        return OpenRefused(OpeningRefusal.SHARED_STORE, f'the class `{class_name}` and {", ".join((f"`{other}`" for other in others))} are bound to one store of `{name}` in {where}')
    store = adapter.open()
    if not record.layable(store):
        _close(store)
        return OpenRefused(OpeningRefusal.LESS_THAN_NEEDED, f'the class `{class_name}` is bound to `{name}`, whose store is not a sparse store of any address and value length')
    unmet = needs.unmet(store)
    if unmet:
        _close(store)
        return OpenRefused(OpeningRefusal.LESS_THAN_NEEDED, f'the class `{class_name}` needs of `{name}` ' + '; '.join(unmet))
    return record.Record(store)
