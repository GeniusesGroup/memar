#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Paused(DeclaredLabel):
    word = 'Paused'
    id = '01a14a04-652a-76eb-beb2-33541b611374'
    meaning = 'Stopped temporarily; resumption is expected.'
    order = 8
    labels = (Label_Status,)
    safe = 'No'
    report_ending = None
