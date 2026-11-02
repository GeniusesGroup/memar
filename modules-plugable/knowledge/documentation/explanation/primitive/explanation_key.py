#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.record_key import ID_FIELD, START_DATE_FIELD, RecordKey
from modules.knowledge.content.primitive.record_key_set import RecordKeySet

class ExplanationKey(RecordKeySet):
    TITLE = RecordKey('title', 'a short, unique, human-readable name for the document, in double quotes', 'Title')
    LABELS = RecordKey('labels', "comma-separated label words on this content (Status-kind and others), e.g. Draft or Draft, guest — the written form of the content record's label edges", 'Labels')
    START_DATE = START_DATE_FIELD
    ID = ID_FIELD
