#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Plan(DeclaredLabel):
    title = 'plan'
    id = ''
    labels = (Label_TaskKind,)
    carried = False

    @classmethod
    def Overview(cls) -> str:
        return 'A task coordinates other tasks — writes, queues or hands over their plans, or asks for a review of their work — and adds this to the kind of its own task, so no plan carries it.'
