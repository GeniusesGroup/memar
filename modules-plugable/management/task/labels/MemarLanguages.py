#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarLanguages(DeclaredLabel):
    word = 'memar-languages'
    id = '01a14a13-1a3a-7365-bc2b-112e0ebb062e'
    meaning = 'The types of the human languages Memar supports, and the abstraction of how each is written.'
    labels = (Label_Topic,)
