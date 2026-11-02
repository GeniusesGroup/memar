#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_LabelKind(DeclaredLabel):
    word = 'LabelKind'
    id = '01a14a04-6530-7000-8000-000000000001'
    meaning = (
        'A label other labels take when they name a kind of label '
        '(Status, Topic, TaskKind, DocumentKind).'
    )
    order = 0
    labels = ()
