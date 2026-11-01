#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class Explanation(Section):
    heading = 'Explanation'
    purpose = "the document's actual content, as topic subsections in the order the author judges most useful"
    use = "the third top-level section; the naming and cross-referencing rules of the specification's Conventions apply, and what belongs in the body versus the companion facets follows the Relevance discipline"
    order = 3
    labels = ('body-section',)
