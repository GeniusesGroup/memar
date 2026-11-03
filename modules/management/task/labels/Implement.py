#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Implement(DeclaredLabel):
    title = 'implement'
    id = '01a14a04-6533-7efe-98ac-0e9e47dc1376'
    labels = (Label_TaskKind,)
    carried = True

    @classmethod
    def Overview(cls) -> str:
        return 'The task builds or changes code, a test or a tool whose design is already settled, one checked step at a time.'
