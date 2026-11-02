#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Examples(Section):
    heading = 'Examples'
    purpose = 'concrete instances of the concept, rule, or pattern the document defines, showing what following (or violating) it actually looks like in practice'
    use = 'for a document whose primary content is a definition or a rule, where worked instances are the clearest way to convey what that rule permits or forbids'
    distinct_from = "Explanation's own illustrative content"
    order = 10
    labels = ('optional-section',)
