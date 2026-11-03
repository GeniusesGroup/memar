#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Active(DeclaredLabel):
    title = 'Active'
    id = '01a14a04-6529-77f7-9f29-c657a634a824'
    labels = (Label_Status,)
    safe = 'No'
    report_ending = 'its budget ended or it made no progress: another pass is owed'

    @classmethod
    def Overview(cls) -> str:
        return 'Being worked on or investigated now.'
