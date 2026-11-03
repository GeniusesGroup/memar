#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Superseded(DeclaredLabel):
    id = '01a14a04-6526-7818-93c4-ad6502671d9b'
    labels = (Label_Status,)
    safe = 'No: depend on the superseding document'
    report_ending = None

    @classmethod
    def Overview(cls) -> str:
        return 'Replaced by a newer document, which the cited relation names.'
