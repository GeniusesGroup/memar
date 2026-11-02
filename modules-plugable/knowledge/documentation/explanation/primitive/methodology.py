#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Methodology(Section):
    heading = 'Methodology'
    purpose = 'the method the content rests on: analytical moves, layering constraints, verification discipline, what is deliberately excluded as a standing rule of the document'
    use = 'only when that method itself is load-bearing for understanding the claims, as most documents can omit it; commonly placed under Introduction, alongside but independent of Motivation, and either can be used without the other; it is not a miniature changelog, so participant names, session dates, review-pass narratives and pointers whose only payload is that history lives elsewhere must not appear here'
    distinct_from = 'Motivation, with which it is unrelated in content'
    order = 4
    labels = ('optional-section',)
