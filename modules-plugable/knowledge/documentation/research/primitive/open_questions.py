#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class OpenQuestions(Section):
    heading = 'Open Questions'
    purpose = 'questions raised that the inquiry does not answer'
    order = 7
    labels = ('research-section',)
