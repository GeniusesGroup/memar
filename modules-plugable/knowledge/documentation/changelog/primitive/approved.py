#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.word import Word

class Approved(Word):
    word = 'approved'
    meaning = 'judged the entry correct, and did not do the work it judged'
    order = 1
    labels = ('contributor-role',)
