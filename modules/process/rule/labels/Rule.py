#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Rule(DeclaredLabel):
    title = 'rule'
    id = '01a1bb11-a141-74b7-b914-f7fece812d1f'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'A content that states a rule: a condition on a subject an owner governs, whose reader follows it when the step concerns that subject.'
