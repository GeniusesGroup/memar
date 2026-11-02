#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.identity.thing.labels.Draft import Label_Draft
from modules.identity.thing.labels.Proposed import Label_Proposed
from modules.identity.thing.labels.Final import Label_Final
from modules.identity.thing.labels.Superseded import Label_Superseded
from modules.identity.thing.labels.Rejected import Label_Rejected
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.DocumentKind'
).Label_DocumentKind

class Label_Explanation(DeclaredLabel):
    word = 'Explanation'
    id = '01a14a04-653a-7a01-8a01-000000000001'
    meaning = 'An Explanation-facet document carries Status as Status-kind labels on its record.'
    order = 1
    labels = (Label_DocumentKind,)

    @classmethod
    def statuses(cls) -> tuple[type, ...]:
        return (Label_Draft, Label_Proposed, Label_Final, Label_Superseded, Label_Rejected)
