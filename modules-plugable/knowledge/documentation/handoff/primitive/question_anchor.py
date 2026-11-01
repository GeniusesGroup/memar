#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class QuestionAnchor(Section):
    heading = 'Anchor'
    purpose = 'the file and line, or the section, where the question arose and where the answer lands'
    use = 'so the answer is written where it applies'
    order = 4
    labels = ('question-field', 'warned')
