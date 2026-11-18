#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from machine.console import fail
from modules.knowledge.label.primitive.label import Label, Labels
from modules.knowledge.label.primitive.label_store import LabelStore

def replace(store: LabelStore, thing: object, old: Label, new: Label) -> None:
    def make(held: Labels) -> Labels | None:
        if not any(item.id == old.id for item in held):
            fail(f'{thing} does not carry the label {old.title}, so it cannot be replaced by {new.title}')
        items = []
        for item in held:
            if item.id == old.id:
                if not any(other.id == new.id for other in items):
                    items.append(new)
            elif item.id != new.id:
                items.append(item)
        wanted = Labels(tuple(items))
        return None if wanted == held else wanted
    store.edit(thing, make)
