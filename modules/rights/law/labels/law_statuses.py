#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition
from modules.knowledge.status.primitive.status import STATUS_LABEL
VOTING = Label('voting', '01a19853-60ef-726b-ac8d-a1b850d803e4')
GET_CRITIQUE = Label('get-critique', '01a19853-60ef-726b-ac8d-a1b97fbe53be')
LABELS = (
    LabelDefinition(VOTING, (STATUS_LABEL,), 'Binding signatures are open on this law; the payload stays as what was signed.'),
    LabelDefinition(GET_CRITIQUE, (STATUS_LABEL,), 'The law is open for public critique; companions can still change.'),
)
