#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Answer(DeclaredLabel):
    title = 'answer'
    id = ''
    labels = (Label_TaskKind,)
    carried = False

    @classmethod
    def Overview(cls) -> str:
        return 'A question is answered in the conversation itself, which opens no task and so writes no plan.'
