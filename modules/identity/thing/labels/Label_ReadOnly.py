#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_ReadOnly(DeclaredLabel):
    word = 'read_only'
    id = '01a19853-60ef-726b-ac8d-a1be637f1565'
    meaning = 'Readers may not edit; even the owner may not remove this mark without the rule that set it.'
    takes = ()
    labels = ('Status',)
