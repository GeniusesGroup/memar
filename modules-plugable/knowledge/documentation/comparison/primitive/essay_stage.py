#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/essay_stage.py — the ten stages a comparison essay carries, as numbered sections in this order, declared once.

[Documentation — Comparison](../comparison.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class EssayStage(Section):
    WHAT_EACH_PROJECT_IS = ('What each project is', "the other project's self-definition quoted first, the examining project's own, and the category distinction")
    SOURCE_STATUS = ('Source status of the inspected checkout', 'what was inspected and in what state')
    WHAT_THE_OTHER_HAS = ('What the other project has that this one does not', 'credited strengths, each with its evidence')
    WHERE_THIS_IS_STRONGER = ('Where this project is stronger', "the examining project's strengths")
    FAILURE_MODES = ('Failure modes in the other project', 'stated without calling it worthless')
    COSTS_AND_LIMITS = ('Costs and limits on both sides', 'what each side pays and cannot do')
    ADOPTION_FILTER = ('The adoption filter', 'absorb, adapt, reject, and any further disposition, each item naming its home')
    RELATIONSHIP = ('The possible relationship between the projects', 'how the two could stand to each other')
    DECISION = ('The decision', 'what the examining project does')
    OPEN_FOR_CRITIQUE = ('Open for critique', 'what could not be verified, the disclosure quota')
