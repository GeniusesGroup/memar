#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class DecisionOptions(Section):
    heading = 'Options'
    purpose = 'the alternatives that were considered and rejected, each with the reason'
    use = 'to distinguish settled with reasoning from settled by fatigue'
    distinct_from = 'the options of a question, which are the ways it can still be answered'
    order = 3
    labels = ('decision-field',)
