#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.management.task.labels.TaskKind import Label_TaskKind

class Label_Document(DeclaredLabel):
    word = 'document'
    id = '01a14a04-6534-78ea-b510-9d2abcdcba79'
    meaning = 'The task writes or revises a document whose content is already settled.'
    labels = (Label_TaskKind,)
    order = 6
    carried = True
