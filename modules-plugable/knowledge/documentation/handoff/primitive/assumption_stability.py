#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class AssumptionStability(Section):
    heading = 'Stability'
    purpose = 'how likely the assumption is to change, one of the levels of Stability'
    use = 'so a reader tells a firm premise from a provisional one without guessing what the writer meant'
    distinct_from = 'the confidence of a decision, which is how firm the conclusion is'
    order = 2
    labels = ('assumption-field',)
