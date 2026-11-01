#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Risks(Section):
    heading = 'Risks'
    purpose = 'known threats or uncertainties to whatever the document proposes succeeding'
    use = 'for what could go wrong externally, not what the design itself costs'
    distinct_from = 'open questions (recorded in the paired handoff), which are about what the design has not decided yet'
    order = 8
    labels = ('optional-section',)
