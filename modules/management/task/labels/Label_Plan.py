#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_TaskKind import Label_TaskKind

class Label_Plan(DeclaredLabel):
    word = 'plan'
    id = ''
    meaning = 'A task coordinates other tasks — writes, queues or hands over their plans, or asks for a review of their work — and adds this to the kind of its own task, so no plan carries it.'
    takes = (Label_TaskKind,)
    order = 2
    carried = False
    labels = ('TaskKind',)
