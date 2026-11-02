#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Result(Section):
    heading = 'Result'
    purpose = 'how the run ended; the task holds its Status, and this part narrates which kind of end it was'
    order = 3
    labels = ('report-part',)
