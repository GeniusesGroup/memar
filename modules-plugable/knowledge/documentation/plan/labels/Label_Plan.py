#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.Label_DocumentKind'
).Label_DocumentKind

class Label_Plan(DeclaredLabel):
    word = 'Plan'
    id = '01a14a04-653a-7a01-8a01-000000000002'
    meaning = 'A task plan holds the task Status; the plan content does not repeat it.'
    order = 2
    takes = (Label_DocumentKind,)
    labels = ('DocumentKind',)
