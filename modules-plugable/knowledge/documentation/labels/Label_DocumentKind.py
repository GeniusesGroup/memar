#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_DocumentKind(DeclaredLabel):
    word = 'DocumentKind'
    id = '01a14a04-6539-7a01-8a01-000000000001'
    meaning = (
        'A label other labels take when they name what kind of documentation record a word is '
        '(Plan, Report, Explanation, Handoff, Research).'
    )
    order = 1
    labels = ('LabelKind',)
