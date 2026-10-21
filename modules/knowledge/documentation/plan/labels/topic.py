#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/documentation/plan/labels/topic.py — the kind of label `Topic`, declared once: the subjects `claims` batches by.

A topic is a label whose definition takes the label `Topic`
(`modules/knowledge/documentation/primitive/label.py`): a plan takes as many as
it needs, and `claims` batches the queued tasks that carry one. A task with two
subjects may carry two, but a topic is not assigned needlessly: it is added when
another task is to be found by it. It is free text normalized when written
(lower case, runs of white space as one hyphen), and it is defined when first
used, in the project's own label registry, not in a list this code keeps: a kept
list in code would stop a new subject at the moment it appears. A typo that
splits one subject in two is met by showing the labels in use and by warning of
a near match (`session_label`). A plan without a topic has none.

It is a type so that the rule of normalizing and the check of a one-line value
are written here and nowhere else
([A Fact in Code Is Written Once](../../../modules/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations
from machine.console import fail
from modules.knowledge.documentation.primitive.label import Label, LabelKind, LabelProblem
LABEL_KIND_NAME = 'Topic'
TOPIC_LABEL = Label(LABEL_KIND_NAME, '01a14a04-6536-7c2e-8cc6-276de9a45ba5')

class Topic(str):
    """A topic's word: lower case, each run of white space one hyphen; empty when there is none."""

    @classmethod
    def normalized(cls, text: str) -> Topic:
        """TEXT as a topic: stripped, lower case, each run of white space one hyphen; empty when nothing is left."""
        return cls('-'.join(text.lower().split()))

    @classmethod
    def checked(cls, text: str) -> Topic:
        """TEXT as a topic, normalized; refused when it holds a line break, since a topic is a one-line front-matter value."""
        if '\n' in text or '\r' in text:
            fail('a topic is one line; this one holds a line break')
        return cls.normalized(text)

def _word(text: str) -> str:
    if '\n' in text or '\r' in text:
        raise LabelProblem('a topic is one line; this one holds a line break')
    word = Topic.normalized(text)
    if not word:
        raise LabelProblem('a topic is not empty; to remove one, remove its label')
    return str(word)
LABEL_KIND = LabelKind(TOPIC_LABEL, 'the subject a task is about, free text in lower case with spaces as hyphens', '`claims`, which batches the queued tasks that carry one, and `labels`, which lists those in use', _word)
