#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.record_key import RecordKey
from modules.knowledge.content.primitive.record_key_set import RecordKeySet

class PracticeKey(RecordKeySet):
    NAME = RecordKey('name', "the skill's name, lowercase with hyphens, and the name of the file it heads", 'name')
    DESCRIPTION = RecordKey('description', 'what the skill does and when to use it: the only thing an agent sees before it triggers', 'description')
