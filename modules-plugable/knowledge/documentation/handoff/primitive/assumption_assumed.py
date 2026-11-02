#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class AssumptionAssumed(Section):
    heading = 'Assumed'
    purpose = 'what is taken as given meanwhile'
    use = 'so the premise a later step stands on is visible'
    distinct_from = 'a decision, which is settled with its reason'
    order = 1
    labels = ('assumption-field',)
