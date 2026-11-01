#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.document_kind_value import DocumentKindValue

class Explanation(DocumentKindValue):
    word = 'Explanation-facet document'
    meaning = 'An Explanation-facet document carries Status as Status-kind labels on its record.'
    order = 1
