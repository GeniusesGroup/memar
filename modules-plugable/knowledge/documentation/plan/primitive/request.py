#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Request(Section):
    heading = 'Request'
    purpose = 'what was asked, and what checks it is done'
    order = 1
    labels = ('plan-part',)
