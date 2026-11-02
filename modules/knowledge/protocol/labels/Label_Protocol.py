#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Topic import Label_Topic

class Label_Protocol(DeclaredLabel):
    word = 'protocol'
    id = '01a19249-6472-7b5a-abf6-cba2a3e7921c'
    meaning = 'Work on the protocol module itself: what a protocol is, how a protocol is written.'
    takes = (Label_Topic,)
    labels = ('Topic',)
