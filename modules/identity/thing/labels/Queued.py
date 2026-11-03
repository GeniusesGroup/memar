#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Queued(DeclaredLabel):
    title = 'Queued'
    id = '01a14a04-6528-796c-8a26-e8132b15f166'
    labels = (Label_Status,)
    safe = 'No'
    report_ending = None

    @classmethod
    def Overview(cls) -> str:
        return 'Waiting to be taken up; nobody has started it.'
