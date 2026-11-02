#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_MemoryPort(DeclaredLabel):
    word = 'memory-port'
    id = '01a167b9-f20e-7305-95a0-e055447a1869'
    meaning = 'The memory port and its adapters, and the task verbs and records moved onto it.'
    labels = (Label_Topic,)
