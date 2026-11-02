#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation

class Rejected(StatusValue):
    word = 'Rejected'
    meaning = 'Considered and explicitly not adopted; kept for the historical record.'
    order = 5
    id = '01a14a04-6527-7b35-8b8c-8438070c1c38'
    kinds = (Explanation,)
    safe = 'No'
    report_ending = None

LABELS = (Rejected.definition(),)
