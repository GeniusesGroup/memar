#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation

class Final(StatusValue):
    word = 'Final'
    meaning = 'Reflected in canonical documentation.'
    order = 3
    id = '01a14a04-6525-7362-b4b2-3654fb2c06a6'
    kinds = (Explanation,)
    safe = 'Yes'
    report_ending = None

LABELS = (Final.definition(),)
