#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class QuestionAsked(Section):
    heading = 'Asked'
    purpose = 'the date and who asked'
    use = 'so the answer is addressed to the one who asked and the age of the question is known'
    order = 6
    labels = ('question-field',)
