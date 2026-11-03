#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Task(DeclaredLabel):
    title = 'task'
    id = '01a14aad-9352-77c5-970f-1bc2b884b5dc'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'A reference to the task module (what a task is, its records and its verbs); not a Topic.'
