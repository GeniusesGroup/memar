#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class AnticipatedWork(Section):
    heading = 'Work'
    purpose = 'the extension, growth path or follow-up the discussion anticipates'
    use = 'so the anticipation is kept in one findable place'
    distinct_from = 'a question, where something is undecided, and a plan, which someone is doing now'
    order = 1
    labels = ('anticipated-work-field',)
