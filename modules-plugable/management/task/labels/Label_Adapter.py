#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_Adapter(DeclaredLabel):
    word = 'adapter'
    id = '01a14aae-4f4c-7618-a0e2-ab43ef3da0ab'
    meaning = "The adapter executable a project such as organization gives Memar's `.agents/`."
    takes = (Label_Topic,)
    labels = ('Topic',)
