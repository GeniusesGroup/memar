#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Paid(DeclaredLabel):
    word = 'paid'
    id = '01a19853-60ef-726b-ac8d-a1b44b006589'
    meaning = 'The customer has fully paid the invoice amount.'
    labels = (Label_Status,)
