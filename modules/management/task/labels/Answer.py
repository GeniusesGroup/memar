#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Answer(DeclaredLabel):
    word = 'answer'
    id = ''
    meaning = 'A question is answered in the conversation itself, which opens no task and so writes no plan.'
    labels = (Label_TaskKind,)
    order = 1
    carried = False
