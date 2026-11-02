#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Active(DeclaredLabel):
    word = 'Active'
    id = '01a14a04-6529-77f7-9f29-c657a634a824'
    meaning = 'Being worked on or investigated now.'
    order = 7
    takes = (Label_Status,)
    kinds = ('Plan', 'Report', 'Handoff', 'Research',)
    safe = 'No'
    report_ending = 'its budget ended or it made no progress: another pass is owed'
    labels = ('Status',)
