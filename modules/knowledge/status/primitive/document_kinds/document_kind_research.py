#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.document_kind_value import DocumentKindValue

class Research(DocumentKindValue):
    word = 'Research'
    meaning = 'A research task; the task holds Status of the inquiry.'
    order = 5
