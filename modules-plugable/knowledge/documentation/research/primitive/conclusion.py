#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Conclusion(Section):
    heading = 'Conclusion'
    purpose = 'the final outcome for each question, and where it landed'
    order = 8
    labels = ('research-section',)
