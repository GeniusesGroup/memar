#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.document_kind_value import DocumentKindValue

class Handoff(DocumentKindValue):
    word = 'Handoff'
    meaning = 'A handoff content of a task; the task holds Status.'
    order = 4
