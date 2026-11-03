#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Mechanical(DeclaredLabel):
    title = 'mechanical'
    id = '01a14a04-6535-780b-bfa4-4a451f6e5d70'
    labels = (Label_TaskKind,)
    carried = True

    @classmethod
    def Overview(cls) -> str:
        return 'The task searches, counts, moves or rewrites by a rule given to it in full, and no step of it decides anything.'
