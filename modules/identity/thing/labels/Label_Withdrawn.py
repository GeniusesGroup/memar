#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_research import Research

class Withdrawn(StatusValue):
    word = 'Withdrawn'
    meaning = 'Abandoned without an answer; the reason is recorded in the record itself.'
    order = 11
    id = '01a14a04-652d-7d1c-963b-a0fd21c182dd'
    kinds = (Research,)
    safe = 'No'
    report_ending = None

LABELS = (Withdrawn.definition(),)
