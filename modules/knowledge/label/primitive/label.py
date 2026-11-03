#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
import os
import re
import time
from dataclasses import dataclass
from typing import Callable, Iterable
FLAG_SEPARATOR = '='
_ID = '[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}'
_LABEL = re.compile(f'^(?:[-*]\\s+)?(?P<title>[^()\\s][^()]*?)\\s*\\((?P<id>{_ID})\\)$')

class LabelProblem(ValueError):
    pass

def new_id() -> str:
    stamp = int(time.time() * 1000)
    random_bits = int.from_bytes(os.urandom(10), 'big')
    number = stamp << 80 | 7 << 76 | (random_bits >> 68 & 4095) << 64 | 2 << 62 | random_bits & (1 << 62) - 1
    digits = f'{number:032x}'
    return f'{digits[:8]}-{digits[8:12]}-{digits[12:16]}-{digits[16:20]}-{digits[20:]}'

@dataclass(frozen=True)
class Label:
    title: str
    id: str

    def __str__(self) -> str:
        return f'{self.title}({self.id})'

    @classmethod
    def read(cls, text: str) -> Label | None:
        found = _LABEL.match(text.strip())
        return cls(found['title'].strip(), found['id']) if found else None

@dataclass(frozen=True)
class LabelDefinition:
    label: Label
    labels: tuple[Label, ...] = ()
    meaning: str = ''
    ended: str = ''
    replaced_by: tuple[Label, ...] = ()

    def is_a(self, kind: Label) -> bool:
        return any(held.id == kind.id for held in self.labels)

@dataclass(frozen=True)
class LabelKind:
    label: Label
    summary: str
    read_by: str
    normalize: Callable[[str], str]
    closed: tuple[LabelDefinition, ...] = ()

    @property
    def name(self) -> str:
        return self.label.title

    def define(self, text: str) -> LabelDefinition:
        return LabelDefinition(Label(self.normalize(text), new_id()), (self.label,))

@dataclass(frozen=True)
class Labels:
    items: tuple[Label, ...] = ()

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __bool__(self) -> bool:
        return bool(self.items)

    @classmethod
    def read(cls, value: str) -> Labels:
        found: list[Label] = []
        for line in value.splitlines():
            label = Label.read(line)
            if label is not None and label not in found:
                found.append(label)
        return cls(tuple(found))

    def with_label(self, label: Label) -> Labels:
        return self if any(item.id == label.id for item in self.items) else Labels((*self.items, label))

    def without(self, label: Label) -> Labels:
        return Labels(tuple(item for item in self.items if item.id != label.id))

    def lines(self) -> list[str]:
        return [f'  - {label}' for label in self.items]

class LabelRegistry:

    def __init__(self, kinds: Iterable[LabelKind], declared: Iterable[LabelDefinition]=()) -> None:
        self.kinds = {kind.name: kind for kind in kinds}
        self._by_id: dict[str, LabelDefinition] = {}
        for kind in self.kinds.values():
            self._by_id[kind.label.id] = LabelDefinition(kind.label)
            for definition in kind.closed:
                self._by_id[definition.label.id] = definition
        for definition in declared:
            self._by_id.setdefault(definition.label.id, definition)

    def definitions(self, kind: str) -> tuple[LabelDefinition, ...]:
        wanted = self.kinds[kind].label
        return tuple(definition for definition in self._by_id.values() if definition.is_a(wanted))

    def definition(self, label: Label) -> LabelDefinition | None:
        return self._by_id.get(label.id)

    def labels_of(self, label: Label) -> tuple[Label, ...]:
        definition = self.definition(label)
        return definition.labels if definition else ()

    def titles(self, labels: Labels, kind: str) -> tuple[str, ...]:
        wanted = self.kinds[kind].label
        return tuple(
            self._by_id[label.id].label.title
            for label in labels
            if any(held.id == wanted.id for held in self.labels_of(label))
        )

    def add(self, definition: LabelDefinition) -> None:
        self._by_id.setdefault(definition.label.id, definition)

    def resolve(self, text: str) -> tuple[Label, LabelDefinition | None]:
        kind_name, found, title = text.partition(FLAG_SEPARATOR)
        if not found or not kind_name.strip() or (not title.strip()):
            raise LabelProblem(f'a label is written KIND{FLAG_SEPARATOR}WORD, e.g. {self._example()}; {text!r} is not one')
        kind = self.kinds.get(kind_name.strip())
        if kind is None:
            raise LabelProblem(f"a plan carries labels of the kinds {', '.join(self.kinds)}; {kind_name.strip()!r} is none of them")
        if kind.closed:
            made = kind.normalize(title)
            for definition in kind.closed:
                if definition.label.title == made:
                    return (definition.label, None)
            raise LabelProblem(f'{made!r} is not a {kind.name}')
        made = kind.normalize(title)
        for definition in self._by_id.values():
            if definition.label.title == made and definition.is_a(kind.label):
                return (definition.label, None)
        fresh = kind.define(made)
        return (fresh.label, fresh)

    def _example(self) -> str:
        free = next((kind for kind in self.kinds.values() if not kind.closed), next(iter(self.kinds.values())))
        return f'{free.name}{FLAG_SEPARATOR}memar-scripts'
