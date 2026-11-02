#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.Label_TaskKind import Label_TaskKind

class Label_Critique(DeclaredLabel):
    word = 'critique'
    id = '01a14a04-6532-76bf-b48e-4b7cc539bf44'
    meaning = 'The task judges work it did not make against the documents that govern that work, and returns a verdict on each part.'
    takes = (Label_TaskKind,)
    order = 4
    carried = True
    labels = ('TaskKind',)
