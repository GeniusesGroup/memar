#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Status(Section):
    heading = 'Status'
    purpose = "mandatory: one line stating the inquiry's overall state"
    order = 2
    labels = ('research-section', 'mandatory')
