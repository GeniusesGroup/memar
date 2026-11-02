#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class SourceStatusOfTheInspectedCheckout(Section):
    heading = 'Source status of the inspected checkout'
    purpose = 'what was inspected and in what state'
    order = 2
    labels = ('essay-stage',)
