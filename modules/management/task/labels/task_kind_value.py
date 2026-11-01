#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class TaskKindValue(Word):
    labels = ('TaskKind',)
    carried = False
    id = ''

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        if cls is TaskKindValue:
            return
        cls.applies = cls.meaning
