#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.status.primitive.status_value import StatusValue, STATUS_LABEL
from modules.knowledge.status.primitive.document_kinds.document_kind_handoff import Handoff
from modules.knowledge.status.primitive.document_kinds.document_kind_research import Research

class Paused(StatusValue):
    word = 'Paused'
    meaning = 'Stopped temporarily; resumption is expected.'
    order = 8
    id = '01a14a04-652a-76eb-beb2-33541b611374'
    kinds = (Handoff, Research,)
    safe = 'No'
    report_ending = None

LABELS = (Paused.definition(),)
