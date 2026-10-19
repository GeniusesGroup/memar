#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/handoff_section.py — the open catalog of state sections a handoff may carry, declared once.

[Documentation — Handoff](../handoff.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.section import Section


class HandoffSection(Section):
    TOPIC_AND_PURPOSE = ("Topic & Purpose", "what is being discussed and why, in one short paragraph")
    STATUS = ("Status", "one line naming the topic's overall state")
    DECISIONS = ("Decisions", "for each decision, what was decided, the reasoning and its confidence")
    AMBIGUITIES_RESOLVED = ("Ambiguities Resolved", "what was unclear, what is now clear, and what resolved it")
    OPEN_QUESTIONS = ("Open Questions", "questions still to be answered, each standing alone")
    ANTICIPATED_WORK = ("Anticipated Work", "extensions and follow-up the discussion anticipates but no one has committed to")
    ASSUMPTIONS = ("Assumptions", "what is assumed, its stability, and what would change if it proved wrong")
    KEY_DEFINITIONS_ESTABLISHED = ("Key Definitions Established", "terms defined, refined or confirmed during the discussion")
    PROPOSED_NEXT_STEPS = ("Proposed Next Steps", "ordered steps toward continuation, with dependencies")
    RELATED_ARTIFACTS = ("Related Artifacts", "documents, models or records affected by or affecting the discussion")
    NOTES = ("Notes", "anything that does not fit above but may matter later")
