#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Final(DeclaredLabel):
    word = 'Final'
    id = '01a14a04-6525-7362-b4b2-3654fb2c06a6'
    meaning = 'Reflected in canonical documentation.'
    order = 3
    labels = (Label_Status,)
    safe = 'Yes'
    report_ending = None
