#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_LegacyArchive(DeclaredLabel):
    title = 'legacy-archive'
    id = '01a154a5-4510-7194-965d-0273c985375f'
    labels = (Label_Topic,)

    @classmethod
    def Overview(cls) -> str:
        return "Reviewing the old archive of services and GUI against Memar's modules, and deciding what of it is kept."
