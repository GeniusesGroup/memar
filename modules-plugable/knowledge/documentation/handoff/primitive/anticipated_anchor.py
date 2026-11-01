#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class AnticipatedAnchor(Section):
    heading = 'Anchor'
    purpose = 'the file and line, or the section, where the work was anticipated and where it would land'
    use = 'so the work is found from the document that anticipates it; a base document records its future here'
    order = 4
    labels = ('anticipated-work-field',)
