#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation

class Proposed(StatusValue):
    word = 'Proposed'
    meaning = 'Design discussion reached consensus; ready for final review before being reflected in canonical documentation.'
    order = 2
    id = '01a14a04-6524-7dda-8f7d-d0005f0d99d4'
    kinds = (Explanation,)
    safe = 'Not yet'
    report_ending = None

LABELS = (Proposed.definition(),)
