#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Unexamined(Word):
    word = 'Unexamined'
    meaning = 'taken as given and not looked at'
    order = 3
    labels = ('stability',)
