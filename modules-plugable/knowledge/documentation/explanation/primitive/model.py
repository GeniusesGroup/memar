#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Model(Section):
    heading = 'Model'
    purpose = 'a description of the domain or data model the document concerns: entities, relationships, structure'
    use = "when the document's subject is itself a model rather than a decision, a proposal, or a narrative explanation"
    order = 7
    labels = ('optional-section',)
