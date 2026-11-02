#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Block(DeclaredLabel):
    word = 'block'
    id = '01a19853-60ef-726b-ac8d-a1bf52a42973'
    meaning = 'Blocked from progress until a condition clears.'
    takes = (Label_Status,)
    labels = ('Status',)
