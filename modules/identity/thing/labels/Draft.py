#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Draft(DeclaredLabel):
    word = 'Draft'
    id = '01a14a04-6523-7916-969a-cedf7ef62566'
    meaning = "Direction is not yet settled; real, unresolved questions remain, recorded in the document's paired handoff."
    order = 1
    labels = (Label_Status,)
    safe = 'No'
    report_ending = None
