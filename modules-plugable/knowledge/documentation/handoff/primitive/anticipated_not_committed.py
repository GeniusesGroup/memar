#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class AnticipatedNotCommitted(Section):
    heading = 'Not committed'
    purpose = 'that no one has committed to the work, and what would commit it'
    use = 'so the entry is not read as a plan'
    distinct_from = 'a plan of the task, whose steps someone owns'
    order = 3
    labels = ('anticipated-work-field',)
