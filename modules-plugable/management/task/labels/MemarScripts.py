#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_MemarScripts(DeclaredLabel):
    word = 'memar-scripts'
    id = '01a14a13-1972-7b1b-8056-e00b30bb0067'
    meaning = "Memar's own scripts and the `memar` command: what each verb does, and the module that holds it."
    labels = (Label_Topic,)
