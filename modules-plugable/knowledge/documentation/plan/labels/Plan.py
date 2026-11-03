#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.identity.thing.labels.Queued import Label_Queued
from modules.identity.thing.labels.Active import Label_Active
from modules.identity.thing.labels.Blocked import Label_Blocked
from modules.identity.thing.labels.Complete import Label_Complete
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.DocumentKind'
).Label_DocumentKind

class Label_Plan(DeclaredLabel):
    id = '01a14a04-653a-7a01-8a01-000000000002'
    labels = (Label_DocumentKind,)

    @classmethod
    def statuses(cls) -> tuple[type, ...]:
        return (Label_Queued, Label_Active, Label_Blocked, Label_Complete)

    @classmethod
    def Overview(cls) -> str:
        return 'A task plan holds the task Status; the plan content does not repeat it.'
