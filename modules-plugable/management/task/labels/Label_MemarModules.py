#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.labels.declared_label import DeclaredLabel
from modules.knowledge.label.labels.Label_Topic import Label_Topic

class Label_MemarModules(DeclaredLabel):
    word = 'memar-modules'
    id = '01a14a13-19fb-729d-838f-ca7b1fd0e043'
    meaning = "Surveying Memar's modules and upgrading them one module at a time."
    takes = (Label_Topic,)
    labels = ('Topic',)
