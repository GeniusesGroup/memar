#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Decided(Word):
    word = 'Decided'
    meaning = 'settled, with its reasoning'
    order = 1
    labels = ('confidence',)
