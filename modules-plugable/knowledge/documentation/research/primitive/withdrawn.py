#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Withdrawn(Word):
    word = 'Withdrawn'
    meaning = 'dissolved: its premise was invalidated, or it merged into another'
    order = 3
    labels = ('question-status',)
