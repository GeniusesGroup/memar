#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Abstract(Section):
    heading = 'Abstract'
    purpose = "one self-contained paragraph stating this document's actual claim or decision"
    use = 'the first top-level section; states the claim or decision itself'
    distinct_from = "not a preview of what the reader is about to read, not usage instructions, and not a revision narrative (who reviewed it, which pass introduced which sentence, or a pointer to the changelog for the document's own history)"
    order = 1
    labels = ('body-section',)
