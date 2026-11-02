#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Met(Word):
    word = 'Met'
    meaning = 'the inquiry delivered it'
    order = 1
    labels = ('goal-status',)
