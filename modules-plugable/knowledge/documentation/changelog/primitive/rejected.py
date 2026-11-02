#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Rejected(Word):
    word = 'Rejected'
    meaning = 'closed: considered and deliberately not done, with the reason recorded'
    order = 3
    labels = ('propagation-state',)
