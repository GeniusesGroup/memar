#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word
from modules.knowledge.label.primitive.label import Label, LabelDefinition
STATUS_KIND_ID = '01a14a04-6522-7d19-9796-04f8a30e831f'
STATUS_LABEL = Label('Status', STATUS_KIND_ID)

class StatusValue(Word):
    labels = ('Status',)
    id = ''
    kinds: tuple[type, ...] = ()
    safe = ''
    report_ending: str | None = None

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls is StatusValue:
            return
        cls.key = cls.word.lower()
        cls.label = Label(cls.word, cls.id)

    @classmethod
    def definition(cls) -> LabelDefinition:
        return LabelDefinition(cls.label, (STATUS_LABEL,), cls.meaning)
