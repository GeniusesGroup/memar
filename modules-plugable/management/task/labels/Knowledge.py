#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_Knowledge(DeclaredLabel):
    title = 'knowledge'
    id = '01a14f34-bd79-73d9-b20c-3ccb0034fe0a'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return 'Work across the modules of the knowledge category; a category holds modules and no declarations, so the stream is declared here.'
