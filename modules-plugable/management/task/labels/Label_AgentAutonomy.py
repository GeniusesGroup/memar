#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Topic import Label_Topic

class Label_AgentAutonomy(DeclaredLabel):
    word = 'agent-autonomy'
    id = '01a16468-aa1d-765e-84f5-4bfabf5d1ec8'
    meaning = 'Why agents hand questions to the owner instead of finding the answers in Memar, and the fixes.'
    takes = (Label_Topic,)
    labels = ('Topic',)
