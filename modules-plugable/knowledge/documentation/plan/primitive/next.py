#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Next(Section):
    heading = 'Next'
    purpose = 'what the next task does first'
    order = 4
    labels = ('plan-part',)
