#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class AssumptionsAndConstraints(Section):
    heading = 'Assumptions and Constraints'
    purpose = 'the underlying assumptions a decision or design relies on (cost, schedule, available technology, and similar), and any additional constraints the environment imposes on it'
    use = "for what is taken as given for this document's purposes"
    distinct_from = "the paired handoff's Open Questions: an assumption or constraint is taken as given, not an open question the document is still trying to settle"
    order = 6
    labels = ('optional-section',)
