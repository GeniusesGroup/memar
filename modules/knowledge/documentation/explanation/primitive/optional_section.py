#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/optional_section.py — the catalog of building blocks an Explanation-facet author may use; none is mandatory and the list may grow, declared once.

[Documentation — Explanation](../explanation.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.section import Section


class OptionalSection(Section):
    DEFINITION = ("Definition", "a formal definition of the concept or term the document is about")
    CONVENTIONS = ("Conventions", "a non-binding convention a topic proposes")
    MOTIVATION = ("Motivation", "the concrete failure mode that motivated writing the document")
    METHODOLOGY = ("Methodology", "the method the content rests on, when that method is load-bearing")
    PROBLEM = ("Problem", "the problem the document addresses, from the reader's, user's or business's perspective")
    ASSUMPTIONS_AND_CONSTRAINTS = ("Assumptions and Constraints", "what a decision or design relies on, and the constraints the environment imposes")
    MODEL = ("Model", "the domain or data model the document concerns")
    RISKS = ("Risks", "known threats to whatever the document proposes succeeding")
    IMPLICATIONS = ("Implications", "what a decision requires beyond itself")
    EXAMPLES = ("Examples", "concrete instances of the concept, rule or pattern the document defines")
