#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Topic import Label_Topic

class Label_Task(DeclaredLabel):
    word = 'task'
    id = '01a14aad-9352-77c5-970f-1bc2b884b5dc'
    meaning = 'Work on the task module itself: what a task is, its records and its verbs.'
    takes = (Label_Topic,)
    labels = ('Topic',)
