#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class DecisionDecided(Section):
    heading = 'Decided'
    purpose = 'what was decided, in one line'
    use = 'so a reader knows the conclusion before its reasoning'
    distinct_from = 'an assumption, which is taken as given meanwhile and not settled'
    order = 1
    labels = ('decision-field',)
