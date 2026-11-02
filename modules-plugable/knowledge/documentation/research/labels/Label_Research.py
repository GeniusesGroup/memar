#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.labels.declared_label import DeclaredLabel
Label_DocumentKind = import_module(
    'modules-plugable.knowledge.documentation.labels.Label_DocumentKind'
).Label_DocumentKind

class Label_Research(DeclaredLabel):
    word = 'Research'
    id = '01a14a04-653a-7a01-8a01-000000000005'
    meaning = 'A research task; the task holds Status of the inquiry.'
    order = 5
    takes = (Label_DocumentKind,)
    labels = ('DocumentKind',)
