#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.content.labels.Topic import Label_Topic

class Label_Project(DeclaredLabel):
    word = 'project'
    id = '01a19209-8533-75b4-af0c-275079dc1174'
    meaning = 'A task that is a project: the upstream task of a body of work, active until the work ends, which other tasks refer to; its names are its titles.'
    labels = (Label_Topic,)
