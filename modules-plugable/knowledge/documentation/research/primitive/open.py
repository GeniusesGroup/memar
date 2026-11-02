#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Open(Word):
    word = 'Open'
    meaning = 'not yet answered'
    order = 1
    labels = ('question-status',)
