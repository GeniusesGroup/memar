#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.document_kind_value import DocumentKindValue

class Plan(DocumentKindValue):
    word = 'Plan'
    meaning = 'A task plan holds the task Status; the plan content does not repeat it.'
    order = 2
