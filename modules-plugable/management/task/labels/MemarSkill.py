#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarSkill(DeclaredLabel):
    word = 'memar-skill'
    id = '01a155a9-fc6c-7489-8fbd-92cbdce9b6fc'
    meaning = 'The Memar skill file and what every task pays to read before its first step.'
    labels = (Label_Topic,)
