#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_GetCritique(DeclaredLabel):
    word = 'get-critique'
    id = '01a19853-60ef-726b-ac8d-a1b97fbe53be'
    meaning = 'The law is open for public critique; companions can still change.'
    labels = (Label_Status,)
