#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.LabelKind import Label_LabelKind

class Label_Topic(DeclaredLabel):
    word = 'Topic'
    id = '01a14a04-6536-7c2e-8cc6-276de9a45ba5'
    meaning = (
        'A label other labels take when they name the subject a content record is about. '
        'Each subject word is its own Label_<Word> Type in the domain that owns it '
        '(a stream of work under task). A word that only names a module is a reference '
        'to that module, not a Topic.'
    )
    order = 2
    labels = (Label_LabelKind,)
