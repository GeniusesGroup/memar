#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Status import Label_Status

class Label_Expired(DeclaredLabel):
    title = 'expired'
    id = '01a19853-60ef-726b-ac8d-a1b7be557fe3'
    labels = (Label_Status,)

    @classmethod
    def Overview(cls) -> str:
        return 'The invoice passed its due window without settlement.'
