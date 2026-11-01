#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_explanation import Explanation

class Superseded(StatusValue):
    word = 'Superseded'
    meaning = 'Replaced by a newer document, which the cited relation names.'
    order = 4
    id = '01a14a04-6526-7818-93c4-ad6502671d9b'
    kinds = (Explanation,)
    safe = 'No: depend on the superseding document'
    report_ending = None

LABELS = (Superseded.definition(),)
