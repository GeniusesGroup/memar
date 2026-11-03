#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_OwnerSitting(DeclaredLabel):
    title = 'owner-sitting'
    id = '01a150bd-710b-7bab-8bcb-0eafafa6f3b3'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return 'Work done in a sitting with the owner present; no record the search reaches carries it, so this sentence is read from its word.'
