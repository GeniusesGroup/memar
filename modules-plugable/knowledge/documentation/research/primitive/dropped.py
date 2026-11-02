#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Dropped(Word):
    word = 'Dropped'
    meaning = 'no longer sought'
    order = 4
    labels = ('goal-status',)
