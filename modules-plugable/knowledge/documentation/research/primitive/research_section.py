#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/research_section.py — the sections of a research: the mandatory core first, then the optional catalog, declared once.

[Documentation — Research](../research.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations
from modules.knowledge.content.primitive.section import Section

class ResearchSection(Section):
    TABLE_OF_CONTENTS = ('Table of Contents', "mandatory: a linked list of the file's `##` sections, in order")
    STATUS = ('Status', "mandatory: one line stating the inquiry's overall state")
    QUESTION_AND_GOALS = ('Question and Goals', "mandatory: the inquiry's identity, its questions and goals each with a standing, and its scope")
    PARTICIPANTS = ('Participants', 'mandatory: each participant with the roles they hold')
    METHODOLOGY = ('Methodology', 'mandatory: how the inquiry was conducted, with its limits')
    FINDINGS = ('Findings', 'what the inquiry has established so far, as claim-shaped statements')
    OPEN_QUESTIONS = ('Open Questions', 'questions raised that the inquiry does not answer')
    CONCLUSION = ('Conclusion', 'the final outcome for each question, and where it landed')
    RELATED_ARTIFACTS = ('Related Artifacts', 'documents, records or researches affected by or affecting the inquiry')
    NOTES = ('Notes', 'anything that does not fit above but may matter later')

    @property
    def mandatory(self) -> bool:
        """Whether every research carries the section: the core, not the catalog."""
        return self in (ResearchSection.TABLE_OF_CONTENTS, ResearchSection.STATUS, ResearchSection.QUESTION_AND_GOALS, ResearchSection.PARTICIPANTS, ResearchSection.METHODOLOGY)
