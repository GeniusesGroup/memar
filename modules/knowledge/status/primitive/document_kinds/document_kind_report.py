#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.document_kind_value import DocumentKindValue

class Report(DocumentKindValue):
    word = 'Report'
    meaning = 'A task report narrates how the run ended beside the task Status.'
    order = 3
