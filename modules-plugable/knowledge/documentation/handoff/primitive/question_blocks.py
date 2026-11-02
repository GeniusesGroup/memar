#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class QuestionBlocks(Section):
    heading = 'Blocks'
    purpose = 'what cannot continue until it is answered, and the assumption made meanwhile'
    use = 'the assumption named here is also recorded as an assumption content'
    distinct_from = 'the state of the question, which says why it matters and not what waits on it'
    order = 5
    labels = ('question-field', 'warned')
