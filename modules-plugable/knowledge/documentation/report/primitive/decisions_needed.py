#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class DecisionsNeeded(Section):
    heading = 'Decisions needed'
    purpose = 'the decisions the task hands back; at most ten lines'
    order = 5
    max_lines = 10
    labels = ('report-part', 'hand-back')
