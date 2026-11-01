#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Check(Section):
    heading = 'Check'
    purpose = "what the task's own check found"
    order = 2
    labels = ('report-part',)
