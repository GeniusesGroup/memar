#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Label(DeclaredLabel):
    title = 'label'
    id = '01a14aad-cfcb-727d-a8c7-f94c2a6dee2e'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return 'A reference to the label module (what a label is, where labels are declared, and the label verbs); not a Topic.'
