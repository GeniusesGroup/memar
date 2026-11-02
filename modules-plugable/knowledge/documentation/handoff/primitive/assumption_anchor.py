#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class AssumptionAnchor(Section):
    heading = 'Anchor'
    purpose = 'the file and line, or the section, that relies on the assumption'
    use = 'so the places to revisit are found when the assumption fails'
    order = 4
    labels = ('assumption-field',)
