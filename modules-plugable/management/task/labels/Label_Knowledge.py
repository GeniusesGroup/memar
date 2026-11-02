#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_Knowledge(DeclaredLabel):
    word = 'knowledge'
    id = '01a14f34-bd79-73d9-b20c-3ccb0034fe0a'
    meaning = 'Work across the modules of the knowledge category; a category holds modules and no declarations, so the stream is declared here.'
    takes = (Label_Topic,)
    labels = ('Topic',)
