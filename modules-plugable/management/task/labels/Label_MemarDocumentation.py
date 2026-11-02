#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_MemarDocumentation(DeclaredLabel):
    word = 'memar-documentation'
    id = '01a14a13-19a1-73a4-9827-b2de020e5476'
    meaning = "Memar's documentation and the content services that read, check and write its documents."
    labels = (Label_Topic,)
