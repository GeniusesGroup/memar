#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class QuestionState(Section):
    heading = 'State'
    purpose = 'what is known and why the question matters, with no "this task" or "above" in it'
    use = 'so that a session with no memory of the task reads the entry alone and knows what is asked and what each answer would change'
    order = 2
    labels = ('question-field', 'warned')
