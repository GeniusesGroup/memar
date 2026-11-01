#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class ExploredButUnresolved(Word):
    word = 'Explored-but-unresolved'
    meaning = 'looked into and not settled'
    order = 3
    labels = ('confidence',)
