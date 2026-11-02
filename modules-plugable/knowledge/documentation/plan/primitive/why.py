#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Why(Section):
    heading = 'Why'
    purpose = "the reason, in the writer's own words"
    order = 2
    labels = ('plan-part',)
