#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_Comparison(DeclaredLabel):
    title = 'comparison'
    id = '019c5fe2-457a-7b1d-8df0-2aa1256d667b'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return 'A task whose work is a fair-comparison essay under the Comparison facet.'
