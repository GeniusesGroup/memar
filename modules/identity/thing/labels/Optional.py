#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Optional(DeclaredLabel):
    title = 'optional'
    id = '01a19853-60ef-726b-ac8d-a1bd0d8c0f78'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'The relation or part is optional.'
