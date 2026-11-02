#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class PartiallyMet(Word):
    word = 'Partially met'
    meaning = 'the inquiry delivered part of it'
    order = 2
    labels = ('goal-status',)
