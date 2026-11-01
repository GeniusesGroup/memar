#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class QuestionOptions(Section):
    heading = 'Options'
    purpose = 'the ways it can be answered, the recommended one first with its cost'
    use = 'so the owner can choose without reconstructing the alternatives'
    distinct_from = 'the options of a decision, which were considered and rejected after a choice was made'
    order = 3
    labels = ('question-field', 'warned')
