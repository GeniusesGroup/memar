#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Problem(Section):
    heading = 'Problem'
    purpose = "the problem the document addresses, stated from the reader's, user's or business's perspective"
    use = "when the document's subject is a problem someone else is experiencing, not the document's own reason for existing; for most documents the two coincide and only Motivation is needed"
    distinct_from = 'Motivation, which explains why the document itself was worth writing'
    order = 5
    labels = ('optional-section',)
