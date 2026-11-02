#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Deleted(DeclaredLabel):
    word = 'deleted'
    id = '01a19853-60ef-726b-ac8d-a1ba1ecaabe4'
    meaning = 'Soft-deleted; still addressable.'
    labels = ()
