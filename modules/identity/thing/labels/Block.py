#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Block(DeclaredLabel):
    title = 'block'
    id = '01a19853-60ef-726b-ac8d-a1bf52a42973'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'Blocked from progress until a condition clears.'
