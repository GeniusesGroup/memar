#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_Khayyam(DeclaredLabel):
    word = 'khayyam'
    id = '01a14a13-19e7-74d9-ba0b-8335ceaab682'
    meaning = 'Work on the Khayyam language and its toolchain: compiler, language server and targets.'
    takes = (Label_Topic,)
    labels = ('Topic',)
