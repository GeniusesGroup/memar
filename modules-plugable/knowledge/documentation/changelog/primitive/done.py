#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Done(Word):
    word = 'Done'
    meaning = 'closed: the propagation was carried out'
    order = 2
    labels = ('propagation-state',)
