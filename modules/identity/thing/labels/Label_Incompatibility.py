#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Incompatibility(DeclaredLabel):
    word = 'incompatibility'
    id = '01a19853-60ef-726b-ac8d-a1c16af7dc98'
    meaning = 'Incompatible under a rule that enforces it.'
    takes = (Label_Status,)
    labels = ('Status',)
