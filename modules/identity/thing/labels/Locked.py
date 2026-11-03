#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Locked(DeclaredLabel):
    title = 'locked'
    id = '01a19853-60ef-726b-ac8d-a1bb3825a8a8'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'Locked by its owner against further change.'
