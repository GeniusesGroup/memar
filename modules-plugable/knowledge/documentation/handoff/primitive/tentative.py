#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Tentative(Word):
    word = 'Tentative'
    meaning = 'assumed meanwhile, to firm up or be dropped'
    order = 2
    labels = ('confidence',)
