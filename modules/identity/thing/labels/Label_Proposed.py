#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Proposed(DeclaredLabel):
    word = 'Proposed'
    id = '01a14a04-6524-7dda-8f7d-d0005f0d99d4'
    meaning = 'Design discussion reached consensus; ready for final review before being reflected in canonical documentation.'
    order = 2
    takes = (Label_Status,)
    kinds = ('Explanation',)
    safe = 'Not yet'
    report_ending = None
    labels = ('Status',)
