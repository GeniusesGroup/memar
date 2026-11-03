#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.identity.thing.labels.Active import Label_Active
from modules.identity.thing.labels.Paused import Label_Paused
from modules.identity.thing.labels.Complete import Label_Complete
from modules.identity.thing.labels.Withdrawn import Label_Withdrawn
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.DocumentKind'
).Label_DocumentKind

class Label_Research(DeclaredLabel):
    title = 'Research'
    id = '01a14a04-653a-7a01-8a01-000000000005'
    labels = (Label_DocumentKind,)

    @classmethod
    def statuses(cls) -> tuple[type, ...]:
        return (Label_Active, Label_Paused, Label_Complete, Label_Withdrawn)

    @classmethod
    def Overview(cls) -> str:
        return 'A research task; the task holds Status of the inquiry.'
