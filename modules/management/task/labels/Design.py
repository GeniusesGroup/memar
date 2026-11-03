#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Design(DeclaredLabel):
    title = 'design'
    id = '01a14a04-6531-73d5-8eeb-6e37ddce016d'
    labels = (Label_TaskKind,)
    carried = True

    @classmethod
    def Overview(cls) -> str:
        return 'The task decides what something is — a concept, an abstraction, a protocol, a language construct, a rule — or chooses between proposals for one, before anything is built from it.'
