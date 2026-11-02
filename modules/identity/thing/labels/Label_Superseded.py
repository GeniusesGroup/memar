#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Superseded(DeclaredLabel):
    word = 'Superseded'
    id = '01a14a04-6526-7818-93c4-ad6502671d9b'
    meaning = 'Replaced by a newer document, which the cited relation names.'
    order = 4
    takes = (Label_Status,)
    kinds = ('Explanation',)
    safe = 'No: depend on the superseding document'
    report_ending = None
    labels = ('Status',)
