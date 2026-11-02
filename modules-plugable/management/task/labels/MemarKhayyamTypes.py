#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarKhayyamTypes(DeclaredLabel):
    word = 'memar-khayyam-types'
    id = '01a14a13-1980-7a5f-8be8-e766626965a0'
    meaning = "Memar's own types written as Khayyam types."
    labels = (Label_Topic,)
