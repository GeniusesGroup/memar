#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Priority(DeclaredLabel):
    title = 'Priority'
    id = '01a1b00c-9bdf-7bac-ba8b-6a4b1804caa5'
    labels = ()

    @classmethod
    def Overview(cls) -> str:
        return (
            'Attached to a thing that holds a priority rank on its priority relation: '
            'how soon the thing is taken among peers that compete for limited attention. '
            'Absence of the field means the lowest rank. Completing work does not detach this label.'
        )
