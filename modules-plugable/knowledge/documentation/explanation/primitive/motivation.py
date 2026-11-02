#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Motivation(Section):
    heading = 'Motivation'
    purpose = 'the specific problem or friction the document solves: the concrete failure mode that motivated writing it, not a generic statement of importance'
    use = 'commonly placed under Introduction; names the failure mode, not the writing session that discovered it, so session narrative, requester identity and how-we-got-here chronology belong in the changelog'
    distinct_from = 'Problem, which states a problem someone else is experiencing; Motivation explains why the document itself was worth writing'
    order = 3
    labels = ('optional-section',)
