#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class DecisionConfidence(Section):
    heading = 'Confidence'
    purpose = 'the level, one of the levels of Confidence, the decision is held at'
    use = 'so a reader tells a firm conclusion from a provisional one without guessing what the writer meant'
    distinct_from = 'the stability of an assumption, which is how likely it is to change'
    order = 4
    labels = ('decision-field',)
