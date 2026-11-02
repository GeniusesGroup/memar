#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Topic import Label_Topic

class Label_Research(DeclaredLabel):
    word = 'research'
    id = '01a1928d-3597-70d5-acea-7408e9301e40'
    meaning = 'A task whose work is a research: an inquiry whose findings other tasks use and cite.'
    takes = (Label_Topic,)
    labels = ('Topic',)
