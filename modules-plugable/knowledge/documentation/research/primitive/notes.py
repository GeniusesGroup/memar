#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Notes(Section):
    heading = 'Notes'
    purpose = 'anything that does not fit above but may matter later'
    order = 6
    labels = ('research-section',)
