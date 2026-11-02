#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Status import Label_Status

class Label_Failed(DeclaredLabel):
    word = 'failed'
    id = '01a19853-60ef-726b-ac8d-a1c068c10945'
    meaning = 'The attempt failed.'
    takes = (Label_Status,)
    labels = ('Status',)
