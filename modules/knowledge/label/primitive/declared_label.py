#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word
from modules.knowledge.label.primitive.label import Label, LabelDefinition

class DeclaredLabel(Word):
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

    @classmethod
    def definition(cls) -> LabelDefinition:
        return LabelDefinition(
            cls.as_label,
            tuple(taken.as_label for taken in cls.takes),
            cls.meaning,
            cls.ended,
            tuple(replaced.as_label for replaced in cls.replaced_by),
        )
