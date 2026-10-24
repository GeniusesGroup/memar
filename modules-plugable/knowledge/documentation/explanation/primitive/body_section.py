#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/body_section.py — the top-level (`##`) sections every Explanation-facet document has, in order, declared once.

[Documentation — Explanation](../explanation.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class BodySection(Section):
    ABSTRACT = ('Abstract', "one self-contained paragraph stating the document's actual claim or decision")
    INTRODUCTION = ('Introduction', 'document-wide context needed before the technical content; carries no direct content itself')
    EXPLANATION = ('Explanation', "the document's actual content, as topic subsections in the order the author judges most useful")
