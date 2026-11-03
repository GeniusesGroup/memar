#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.LabelKind import Label_LabelKind

class Label_TaskKind(DeclaredLabel):
    title = 'TaskKind'
    id = '01a14a04-652e-7dc2-8926-f2b0b5b2ba1b'
    labels = (Label_LabelKind,)

    @classmethod
    def Overview(cls) -> str:
        return (
            'A label other labels take when they name what act a task is '
            '(design, critique, implement, document, mechanical). '
            'Each act word is its own Label_<Word> Type under the task domain.'
        )
