#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Rejected(DeclaredLabel):
    id = '01a14a04-6527-7b35-8b8c-8438070c1c38'
    labels = (Label_Status,)
    safe = 'No'
    report_ending = None

    @classmethod
    def Overview(cls) -> str:
        return 'Considered and explicitly not adopted; kept for the historical record.'
