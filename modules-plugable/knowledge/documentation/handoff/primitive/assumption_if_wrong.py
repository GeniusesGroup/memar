#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class AssumptionIfWrong(Section):
    heading = 'If wrong'
    purpose = 'what would change if the assumption proved wrong'
    use = 'so the cost of the assumption is known before it is relied on'
    order = 3
    labels = ('assumption-field',)
