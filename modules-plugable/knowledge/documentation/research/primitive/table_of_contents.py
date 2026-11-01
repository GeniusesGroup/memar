#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class TableOfContents(Section):
    heading = 'Table of Contents'
    purpose = "mandatory: a linked list of the file's `##` sections, in order"
    order = 1
    labels = ('research-section', 'mandatory')
