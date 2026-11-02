#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarBoundary(DeclaredLabel):
    word = 'memar-boundary'
    id = '01a14a13-19b8-7327-94b4-e9a6c6f53ce4'
    meaning = 'What belongs in Memar and what belongs outside it, in organization, a library or another project, and the moves that follow.'
    labels = (Label_Topic,)
