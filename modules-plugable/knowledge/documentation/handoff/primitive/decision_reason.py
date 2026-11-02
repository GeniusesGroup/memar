#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class DecisionReason(Section):
    heading = 'Reason'
    purpose = 'why it was decided, including what tipped the balance'
    use = 'so the decision can be revised or defended later; a decision without its reason cannot'
    order = 2
    labels = ('decision-field',)
