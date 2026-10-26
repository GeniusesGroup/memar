#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""Open a class of nodes: `open(project, class_name, needs)`, `record` laid over the adapter the project binds the class to.

What it does, and why a service asks for a class and never for an adapter, is
[Memory Record → Binding adapters to classes](../../../../modules-plugable/computer/memory/store/record/record.md#binding-adapters-to-classes);
the form of the key it reads, `memory`, is `modules/process/project/services/preferences.py`'s. The entry point of
`bundles/memar` declares this `open`, and it is written here because that file routes and nothing else; a bundle may
import pluggable modules, and a kernel module may not, so no kernel module imports an adapter.

An adapter is named by its module's capability name: the module of that name at
`modules-plugable/computer/memory/store/<capability>/`, which offers `bind(project, class_name)`, the adapter that
serves the class, an object whose `open()` opens its store and whose `store` names the store it keeps the class in.
Nothing heavy is imported until `open` is called.
"""
from __future__ import annotations
import enum
import re
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from types import ModuleType
from typing import Any
STORE_CAPSULES = 'modules-plugable.computer.memory.store'
BIND = 'bind'
CAPABILITY_NAME = re.compile('[a-z0-9]+(?:-[a-z0-9]+)*')

class OpeningRefusal(enum.Enum):
    """Why opening a class is refused."""
    NOT_BOUND = 'NotBound'
    LESS_THAN_NEEDED = 'LessThanNeeded'
    SHARED_STORE = 'SharedStore'
    MALFORMED = 'Malformed'

    def summary(self) -> str:
        return {OpeningRefusal.NOT_BOUND: "the project's `memory` key does not name the class", OpeningRefusal.LESS_THAN_NEEDED: 'the adapter declares less than the class needs, or keeps a store `record` cannot be laid over', OpeningRefusal.SHARED_STORE: 'another class is bound to the same store', OpeningRefusal.MALFORMED: "the project's `memory` key is not in its form, or names an adapter no module offers"}[self]

@dataclass(frozen=True)
class OpenRefused:
    """Opening is refused and nothing is opened; `detail` names the class and what to add or mend, for a reader."""
    reason: OpeningRefusal
    detail: str = field(default='', compare=False)

def adapter_module(name: str) -> ModuleType | None:
    """The module the capability name NAME names, when it offers `bind`; None otherwise."""
    if not CAPABILITY_NAME.fullmatch(name):
        return None
    try:
        module = import_module(f'{STORE_CAPSULES}.{name}.{name}')
    except ImportError:
        return None
    return module if callable(getattr(module, BIND, None)) else None

def open(project: Path, class_name: str, needs: Any) -> Any:
    """`record` laid over a new handle of the store the adapter bound to CLASS_NAME keeps, or OpenRefused."""
    preferences = import_module('modules.process.project.services.preferences')
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
    others = sorted((other for other, bound in bindings.items() if other != class_name and bound == name and module.bind(project, other).store == adapter.store))
    if others:
        return OpenRefused(OpeningRefusal.SHARED_STORE, f'the class `{class_name}` and {", ".join((f"`{other}`" for other in others))} are bound to one store of `{name}` in {where}')
    store = adapter.open()
    if not record.layable(store):
        return OpenRefused(OpeningRefusal.LESS_THAN_NEEDED, f'the class `{class_name}` is bound to `{name}`, whose store is not a sparse store of any address and value length')
    unmet = needs.unmet(store)
    if unmet:
        return OpenRefused(OpeningRefusal.LESS_THAN_NEEDED, f'the class `{class_name}` needs of `{name}` ' + '; '.join(unmet))
    return record.Record(store)
