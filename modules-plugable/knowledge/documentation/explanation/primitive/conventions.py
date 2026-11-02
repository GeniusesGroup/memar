#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.text.primitive.section import Section

class Conventions(Section):
    heading = 'Conventions'
    purpose = 'a non-binding convention a topic proposes: naming, structural, or otherwise'
    use = "typically as a sibling of that topic's other subsections; for any convention the topic introduces, explicitly non-binding, where enforcement, if any, is a per-organization Linter configuration choice"
    distinct_from = 'broader than naming alone'
    order = 2
    labels = ('optional-section',)
