#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class Pending(Word):
    word = 'Pending'
    meaning = 'the open state: undone propagation work a future contributor should search for'
    order = 1
    labels = ('propagation-state', 'open')
