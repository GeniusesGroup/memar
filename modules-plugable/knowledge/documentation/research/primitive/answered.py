#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Answered(Word):
    word = 'Answered'
    meaning = 'answered, even before the conclusion is written'
    order = 2
    labels = ('question-status',)
