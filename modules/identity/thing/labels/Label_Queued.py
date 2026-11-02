#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_plan import Plan

class Queued(StatusValue):
    word = 'Queued'
    meaning = 'Waiting to be taken up; nobody has started it.'
    order = 6
    id = '01a14a04-6528-796c-8a26-e8132b15f166'
    kinds = (Plan,)
    safe = 'No'
    report_ending = None

LABELS = (Queued.definition(),)
