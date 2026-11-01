#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Introduction(Section):
    heading = 'Introduction'
    purpose = 'document-wide context needed before the technical content'
    use = 'the second top-level section; carries no direct content itself, only subsections such as Motivation and Methodology'
    order = 2
    labels = ('body-section',)
