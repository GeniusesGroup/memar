#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Definition(Section):
    heading = 'Definition'
    purpose = 'a formal definition of the concept or term this document is about'
    use = "when the document's central purpose is describing what something is (a concept, a term, a domain entity), rather than proposing or explaining a decision"
    distinct_from = "Abstract, which states a claim about a document's own content, not a definition of a subject"
    order = 1
    labels = ('optional-section',)
