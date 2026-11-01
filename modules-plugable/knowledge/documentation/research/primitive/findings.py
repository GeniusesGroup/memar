#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Findings(Section):
    heading = 'Findings'
    purpose = 'what the inquiry has established so far, as claim-shaped statements'
    order = 6
    labels = ('research-section',)
