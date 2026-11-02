#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_ImportRelocation(DeclaredLabel):
    word = 'import-relocation'
    id = '01a1508b-7a5d-7448-870a-396c655df680'
    meaning = 'Moving imports to the modules that now hold what they import; no record the search reaches carries it, so this sentence is read from its word.'
    labels = (Label_Topic,)
