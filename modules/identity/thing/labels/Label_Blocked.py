#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Blocked(DeclaredLabel):
    word = 'Blocked'
    id = '01a14a04-652b-7a44-a88d-5f132d3b675d'
    meaning = 'Cannot continue until something outside the work arrives: an answer, an approval, a dependency; the record states what it waits for.'
    order = 9
    takes = (Label_Status,)
    kinds = ('Plan', 'Report', 'Handoff',)
    safe = 'No'
    report_ending = 'it waits on an answer or an approval: say which'
    labels = ('Status',)
