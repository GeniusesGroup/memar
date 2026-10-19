#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/label.py — the `Labels` field of a documentation record, declared once.

A **label** is a word that links a record to others outside the structure of
their ids ([Label](../../label/label.md)). It is written with its identifier,
`design(01a14a04-6531-73d5-8eeb-6e37ddce016d)`, because the word alone is no
identity (a topic `design` and the task kind `design` are two labels): the
identifier is what a search finds every record that took one label by, and the
word is what a reader sees. The identifier is a UUID version 7, so identifiers
sort by the time they were made, as a session id does.

A label is **defined once**, in one place (`LabelDefinition`), and its
definition takes labels of its own: the label `design` takes the label
`TaskKind`, which is what makes it a task kind; `memar-scripts` takes `Topic`;
a Status value takes `Status`. So a *kind* is not a separate thing written
beside every label: it is a label other labels take (`LabelKind`), declared
with the rule that makes a word of it valid. A closed kind lists its words in
code; a free kind makes a definition when a word is first used, and the
definition is kept where the project keeps its own (`LabelRegistry`).

A record takes as many labels as it needs and none it does not: nothing counts
them, and a label is added only when another record is to be found by it. In
front matter the field is a block, one `- word(id)` line a label:

    Labels:
      - design(01a14a04-6531-73d5-8eeb-6e37ddce016d)
      - memar-scripts(01a14a07-1a2b-7c3d-8e4f-5a6b7c8d9e0f)

This file holds no kind and no definition: they are declared with the types
they belong to ([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass
from typing import Callable, Iterable

FLAG_SEPARATOR = "="
_ID = r"[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
_LABEL = re.compile(rf"^(?:[-*]\s+)?(?P<word>[^()\s][^()]*?)\s*\((?P<id>{_ID})\)$")
_DEFINITION = re.compile(r"^(?:[-*]\s+)?(?P<label>.+?\([0-9a-f-]{36}\))\s*:\s*(?P<takes>.*)$")


class LabelProblem(ValueError):
    """A word its kind's rule refuses, or a label that is not defined; the message says what is accepted."""


def new_id() -> str:
    """A new UUID version 7: 48 bits of Unix time in milliseconds, then random bits, so identifiers sort by when they were made."""
    stamp = int(time.time() * 1000)
    random_bits = int.from_bytes(os.urandom(10), "big")
    number = (stamp << 80) | (0x7 << 76) | (((random_bits >> 68) & 0xFFF) << 64) | (0b10 << 62) | (random_bits & ((1 << 62) - 1))
    digits = f"{number:032x}"
    return f"{digits[:8]}-{digits[8:12]}-{digits[12:16]}-{digits[16:20]}-{digits[20:]}"


@dataclass(frozen=True)
class Label:
    """A word and the identifier of the label it names: `design(01a14a04-...)`."""

    word: str
    id: str

    def __str__(self) -> str:
        return f"{self.word}({self.id})"

    @classmethod
    def read(cls, text: str) -> Label | None:
        """The label TEXT writes, as a block line (`- design(id)`) or bare (`design(id)`); None when it is no label."""
        found = _LABEL.match(text.strip())
        return cls(found["word"].strip(), found["id"]) if found else None


@dataclass(frozen=True)
class LabelDefinition:
    """The one place a label is defined: the label, and the labels its definition takes (the kinds it is a member of)."""

    label: Label
    takes: tuple[Label, ...] = ()

    def is_a(self, kind: Label) -> bool:
        """Whether this definition takes the label KIND."""
        return any(taken.id == kind.id for taken in self.takes)

    def line(self) -> str:
        """The definition as a registry line: `- word(id): kind(id), ...`."""
        return f"- {self.label}: " + ", ".join(str(taken) for taken in self.takes)

    @classmethod
    def read(cls, text: str) -> LabelDefinition | None:
        """The definition a registry line writes; None when the line is none."""
        found = _DEFINITION.match(text.strip())
        label = Label.read(found["label"]) if found else None
        if not label:
            return None
        taken = tuple(item for item in (Label.read(part) for part in found["takes"].split(",")) if item)
        return cls(label, taken)


@dataclass(frozen=True)
class LabelKind:
    """A label other labels take, with the rule that makes a word of it valid.

    NORMALIZE returns the word as the kind writes it, or raises `LabelProblem`
    saying what the kind accepts. A closed kind lists CLOSED, the definitions
    of all its words, in code; a free kind has none, and a word it accepts is
    defined when first used.
    """

    label: Label
    summary: str
    read_by: str
    normalize: Callable[[str], str]
    closed: tuple[LabelDefinition, ...] = ()

    @property
    def name(self) -> str:
        return self.label.word

    def define(self, text: str) -> LabelDefinition:
        """A new definition of the word TEXT makes under this kind, with a new identifier; `LabelProblem` when the rule refuses it."""
        return LabelDefinition(Label(self.normalize(text), new_id()), (self.label,))


@dataclass(frozen=True)
class Labels:
    """The labels of one record, in the order written, none twice; as many as the record needs."""

    items: tuple[Label, ...] = ()

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __bool__(self) -> bool:
        return bool(self.items)

    @classmethod
    def read(cls, value: str) -> Labels:
        """The labels a front-matter reader's value for the block holds, one per line; a line that is no label is left out."""
        found: list[Label] = []
        for line in value.splitlines():
            label = Label.read(line)
            if label is not None and label not in found:
                found.append(label)
        return cls(tuple(found))

    def with_label(self, label: Label) -> Labels:
        """These labels and LABEL last; unchanged when the record already carries that label (by identifier)."""
        return self if any(item.id == label.id for item in self.items) else Labels((*self.items, label))

    def without(self, label: Label) -> Labels:
        """These labels but LABEL (by identifier); unchanged when it is not one."""
        return Labels(tuple(item for item in self.items if item.id != label.id))

    def lines(self) -> list[str]:
        """The block's lines under the key, one `  - word(id)` a label."""
        return [f"  - {label}" for label in self.items]


class LabelRegistry:
    """The definitions known to one project: those the kinds declare in code, and those the project keeps for its free kinds.

    The project's own are a text file of `- word(id): kind(id), ...` lines
    (`parse`, `render`), tracked with the project so every clone reads one
    identifier for one label.
    """

    def __init__(self, kinds: Iterable[LabelKind], kept: Iterable[LabelDefinition] = ()) -> None:
        self.kinds = {kind.name: kind for kind in kinds}
        self._by_id: dict[str, LabelDefinition] = {}
        for kind in self.kinds.values():
            self._by_id[kind.label.id] = LabelDefinition(kind.label)
            for definition in kind.closed:
                self._by_id[definition.label.id] = definition
        for definition in kept:
            self._by_id.setdefault(definition.label.id, definition)

    @staticmethod
    def parse(text: str) -> tuple[LabelDefinition, ...]:
        """The definitions a registry file holds; a line that is no definition is left out."""
        return tuple(item for item in (LabelDefinition.read(line) for line in text.splitlines()) if item)

    def definition(self, label: Label) -> LabelDefinition | None:
        """The definition of LABEL, by identifier; None when it is defined nowhere known."""
        return self._by_id.get(label.id)

    def kinds_of(self, label: Label) -> tuple[Label, ...]:
        """The labels the definition of LABEL takes; none when it is undefined."""
        definition = self.definition(label)
        return definition.takes if definition else ()

    def words(self, labels: Labels, kind: str) -> tuple[str, ...]:
        """The words of the labels among LABELS whose definition takes the kind named KIND, in the order written."""
        wanted = self.kinds[kind].label
        return tuple(label.word for label in labels if any(taken.id == wanted.id for taken in self.kinds_of(label)))

    def add(self, definition: LabelDefinition) -> None:
        """Know DEFINITION from now on (one made in this run, before it is kept)."""
        self._by_id.setdefault(definition.label.id, definition)

    def resolve(self, text: str) -> tuple[Label, LabelDefinition | None]:
        """TEXT, `KIND=WORD`, as the label it names, and the new definition it needs (None when the label is already defined).

        A closed kind accepts only a word it lists; a free kind accepts any
        word its rule makes, and defines one not yet known. `LabelProblem`
        names what is accepted when it is not.
        """
        kind_name, found, word = text.partition(FLAG_SEPARATOR)
        if not found or not kind_name.strip() or not word.strip():
            raise LabelProblem(f"a label is written KIND{FLAG_SEPARATOR}WORD, e.g. {self._example()}; {text!r} is not one")
        kind = self.kinds.get(kind_name.strip())
        if kind is None:
            raise LabelProblem(f"a plan carries labels of the kinds {', '.join(self.kinds)}; {kind_name.strip()!r} is none of them")
        if kind.closed:
            made = kind.normalize(word)
            for definition in kind.closed:
                if definition.label.word == made:
                    return definition.label, None
            raise LabelProblem(f"{made!r} is not a {kind.name}")
        made = kind.normalize(word)
        for definition in self._by_id.values():
            if definition.label.word == made and definition.is_a(kind.label):
                return definition.label, None
        fresh = kind.define(made)
        return fresh.label, fresh

    def _example(self) -> str:
        free = next((kind for kind in self.kinds.values() if not kind.closed), next(iter(self.kinds.values())))
        return f"{free.name}{FLAG_SEPARATOR}memar-scripts"
