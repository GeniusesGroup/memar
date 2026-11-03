#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarTasks(DeclaredLabel):
    title = 'memar-tasks'
    id = '01a14a13-19cc-7794-96e1-38952aab81f5'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return "Memar's task records and the tooling that opens, queues, claims, archives and sweeps them."
