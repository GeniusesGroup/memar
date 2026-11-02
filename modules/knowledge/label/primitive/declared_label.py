#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word
from modules.knowledge.label.primitive.label import Label, LabelDefinition

_REGISTRY: list[type] = []

class DeclaredLabel(Word):
    """A label declared as a Type `Label_<Word>`; subclasses register themselves in memory.

    Registration is process-local: a Label_* is known to `taking` only after its
    module has been imported. That is weaker than a graph of label edges, and
    stronger than walking the filesystem for every query ([detail.kh](../../../computer/type/protocol/detail.kh)
    for human-facing text of a type).
    """
    id = ''
    takes: tuple[type, ...] = ()
    ended = ''
    replaced_by: tuple[type, ...] = ()
    kinds: tuple[str, ...] = ()
    safe = ''
    report_ending: str | None = None
    carried = True

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls is DeclaredLabel:
            return
        if not cls.__name__.startswith('Label_'):
            raise TypeError(f'{cls.__name__} must be named Label_<Word>')
        cls.key = cls.word.lower()
        cls.as_label = Label(cls.word, cls.id) if cls.id else Label(cls.word, '')
        cls.label = cls.as_label
        if cls not in _REGISTRY:
            _REGISTRY.append(cls)

    @classmethod
    def definition(cls) -> LabelDefinition:
        return LabelDefinition(
            cls.as_label,
            tuple(taken.as_label for taken in cls.takes),
            cls.meaning,
            cls.ended,
            tuple(replaced.as_label for replaced in cls.replaced_by),
        )

    @classmethod
    def Domain(cls) -> str:
        return 'Label'

    @classmethod
    def Summary(cls) -> str:
        text = (cls.meaning or cls.word).strip()
        if not text:
            return cls.word
        end = text.find('.')
        return text[: end + 1] if end >= 0 else text

    @classmethod
    def Overview(cls) -> str:
        return (cls.meaning or '').strip()

    @classmethod
    def UserActionNote(cls) -> str:
        return ''

    @classmethod
    def DevActionNote(cls) -> str:
        return ''

    @classmethod
    def all_declared(cls) -> tuple[type, ...]:
        return tuple(_REGISTRY)

    @classmethod
    def taking(cls, kind: type) -> tuple[type, ...]:
        """Declared Label_* types whose `takes` include KIND (only among modules already imported)."""
        return tuple(member for member in _REGISTRY if kind in getattr(member, 'takes', ()))

    @classmethod
    def read_among(cls, members: tuple[type, ...], text: str):
        wanted = text.strip().lower()
        return next((member for member in members if member.key == wanted), None)

    @classmethod
    def keys_of(cls, members: tuple[type, ...]) -> tuple[str, ...]:
        return tuple(member.key for member in members)

    @classmethod
    def listing_of(cls, members: tuple[type, ...]) -> str:
        words = [member.word for member in members]
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else (words[0] if words else '')

    @classmethod
    def definitions_of(cls, members: tuple[type, ...]):
        return tuple(member.definition() for member in members)
