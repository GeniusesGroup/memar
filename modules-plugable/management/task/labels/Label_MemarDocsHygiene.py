#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_MemarDocsHygiene(DeclaredLabel):
    word = 'memar-docs-hygiene'
    id = '01a14a13-1a27-798f-bbc4-16921e7f67a0'
    meaning = "Keeping each of Memar's documents in its facet and home: handoffs swept, questions moved to the document they concern."
    takes = (Label_Topic,)
    labels = ('Topic',)
