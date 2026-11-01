#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Implications(Section):
    heading = 'Implications'
    purpose = 'what a decision or design requires beyond itself: new decisions it forces, new or modified requirements it creates, scope or schedule renegotiation it demands'
    use = "for consequences that follow from adopting the document's decision, whether or not anyone wants them to"
    distinct_from = "the paired handoff's Anticipated Work, which holds optional extensions"
    order = 9
    labels = ('optional-section',)
