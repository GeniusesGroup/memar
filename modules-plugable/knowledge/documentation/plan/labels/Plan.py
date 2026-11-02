#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.identity.thing.labels.Label_Queued import Label_Queued
from modules.identity.thing.labels.Label_Active import Label_Active
from modules.identity.thing.labels.Label_Blocked import Label_Blocked
from modules.identity.thing.labels.Label_Complete import Label_Complete
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.Label_DocumentKind'
).Label_DocumentKind

class Label_Plan(DeclaredLabel):
    word = 'Plan'
    id = '01a14a04-653a-7a01-8a01-000000000002'
    meaning = 'A task plan holds the task Status; the plan content does not repeat it.'
    order = 2
    labels = (Label_DocumentKind,)

    @classmethod
    def statuses(cls) -> tuple[type, ...]:
        return (Label_Queued, Label_Active, Label_Blocked, Label_Complete)
