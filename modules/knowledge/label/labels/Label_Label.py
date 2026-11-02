#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_Label(DeclaredLabel):
    word = 'label'
    id = '01a14aad-cfcb-727d-a8c7-f94c2a6dee2e'
    meaning = 'Work on the label module itself: what a label is, where labels are declared, and the label verbs.'
    takes = (Label_Topic,)
    labels = ('Topic',)
