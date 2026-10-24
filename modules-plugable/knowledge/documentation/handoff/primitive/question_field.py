#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/question_field.py — the fields an Open Questions entry carries, declared once.

[Documentation — Handoff](../handoff.md) names six: an entry written during a
task, for the owner to answer later, stands alone by carrying them. The Heading
is the entry's own title line; the other five are bullets. `content check` warns,
never errors, on an entry missing one of the four it looks for, because entries
written before the rule are still valid (`warned`).
"""
from __future__ import annotations
from modules.knowledge.content.primitive.word import Word

class QuestionField(Word):
    HEADING = ('Heading', 'the question itself, in one line')
    STATE = ('State', 'what is known and why the question matters, with no "this task" or "above" in it')
    OPTIONS = ('Options', 'the ways it can be answered, the recommended one first with its cost')
    ANCHOR = ('Anchor', 'the file and line, or the section, where the question arose and where the answer lands')
    BLOCKS = ('Blocks', 'what cannot continue until it is answered, and the assumption made meanwhile')
    ASKED = ('Asked', 'the date and who asked')

    @property
    def warned(self) -> bool:
        """Whether `content check` warns when an entry lacks the field: the four every entry has carried since the rule."""
        return self in (QuestionField.STATE, QuestionField.OPTIONS, QuestionField.ANCHOR, QuestionField.BLOCKS)
