#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_Localization(DeclaredLabel):
    word = 'localization'
    id = '01a14a13-1a0e-7dc1-aa1d-a880b7fd45b2'
    meaning = "How a type's words are given in each human language: its details and their files."
    labels = (Label_Topic,)
