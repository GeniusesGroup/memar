#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_Concept(DeclaredLabel):
    title = 'concept'
    id = '01a15043-2a68-792b-af93-53b6b152c023'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return 'Modeling a concept before it is placed in a module; no record the search reaches carries it, so this sentence is read from its word.'
