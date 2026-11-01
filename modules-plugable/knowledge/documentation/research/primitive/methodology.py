#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Methodology(Section):
    heading = 'Methodology'
    purpose = 'mandatory: how the inquiry was conducted, with its limits'
    order = 2
    labels = ('research-section', 'mandatory')
