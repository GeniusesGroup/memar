#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from typing import Protocol
from machine.console import fail
from modules.knowledge.label.primitive.label import Label, Labels

class LabelStore(Protocol):
    def get(self, thing: object) -> Labels: ...

    def put(self, thing: object, labels: Labels) -> None: ...

def replace(store: LabelStore, thing: object, old: Label, new: Label) -> None:
    held = store.get(thing)
    if not any(item.id == old.id for item in held):
        fail(f'{thing} does not carry the label {old.title}, so it cannot be replaced by {new.title}')
    items = []
    for item in held:
        if item.id == old.id:
            if not any(other.id == new.id for other in items):
                items.append(new)
        elif item.id != new.id:
            items.append(item)
    store.put(thing, Labels(tuple(items)))
