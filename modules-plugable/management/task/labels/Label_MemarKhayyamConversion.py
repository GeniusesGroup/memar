#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Label_Topic import Label_Topic

class Label_MemarKhayyamConversion(DeclaredLabel):
    word = 'memar-khayyam-conversion'
    id = '01a14a13-1aab-74ec-84e2-c78cd526f2b2'
    meaning = 'Converting the Go left in Khayyam files to Khayyam, module by module.'
    takes = (Label_Topic,)
    labels = ('Topic',)
