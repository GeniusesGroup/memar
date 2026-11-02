#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Unmet(Word):
    word = 'Unmet'
    meaning = 'the inquiry did not deliver it'
    order = 3
    labels = ('goal-status',)
