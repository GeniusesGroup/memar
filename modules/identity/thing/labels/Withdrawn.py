#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Withdrawn(DeclaredLabel):
    word = 'Withdrawn'
    id = '01a14a04-652d-7d1c-963b-a0fd21c182dd'
    meaning = 'Abandoned without an answer; the reason is recorded in the record itself.'
    order = 11
    labels = (Label_Status,)
    safe = 'No'
    report_ending = None
