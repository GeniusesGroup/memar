#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class QuestionHeading(Section):
    heading = 'Heading'
    purpose = 'the question itself, in one line'
    use = "the entry's own title line, so the question is found by its heading alone"
    order = 1
    labels = ('question-field',)
