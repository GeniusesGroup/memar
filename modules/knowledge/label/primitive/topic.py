#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/primitive/topic.py — the kind of label `Topic`, declared once: the subjects `claims` batches by.

A topic is a label whose definition takes the label `Topic`
(`modules/knowledge/label/primitive/label.py`): a plan takes as many as
it needs, and `claims` batches the queued tasks that carry one. A task with two
subjects may carry two, but a topic is not assigned needlessly: it is added when
another task is to be found by it. Its word is normalized when written (lower
case, runs of white space as one hyphen). The kind lists no word: a topic is
declared, with `topic()` below, by the domain whose it is — a stream of work by
the task domain, and a topic that names a module by that module
([Label → Where labels are declared](../label.md#where-labels-are-declared)) —
so a new subject is a declaration written where it belongs, with the sentence
that says what it means, and a word nobody declared is refused naming the
declared ones near it (`modules-plugable/management/task/services/plan_labels.py`). A plan
without a topic has none.

It is a type so that the rule of normalizing and the check of a one-line value
are written here and nowhere else
([A Fact in Code Is Written Once](../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
"""
from __future__ import annotations
from machine.console import fail
from modules.knowledge.label.primitive.label import Label, LabelDefinition, LabelKind, LabelProblem
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
LABEL_KIND = LabelKind(TOPIC_LABEL, 'the subject a task is about, in lower case with spaces as hyphens, declared by the domain whose it is', '`claims`, which batches the queued tasks that carry one, and `labels`, which lists those in use', _word)

def topic(word: str, identifier: str, meaning: str, *, ended: str='', replaced_by: tuple[Label, ...]=()) -> LabelDefinition:
    """The declaration of the topic WORD: its IDENTIFIER, minted once and never changed, the one sentence of its MEANING, and, once it has ended, the date ENDED and the labels REPLACED_BY; refused when the word is not as the kind writes it or the meaning is empty."""
    if _word(word) != word:
        raise LabelProblem(f'a topic is declared as it is written, {_word(word)!r}, not {word!r}')
    if not meaning.strip():
        raise LabelProblem(f'the topic {word!r} is declared with the sentence that says what it means')
    if Label.read(f'{word}({identifier})') is None:
        raise LabelProblem(f'the topic {word!r} is declared with a UUID version 7 identifier, not {identifier!r}')
    return LabelDefinition(Label(word, identifier), (TOPIC_LABEL,), meaning.strip(), ended, replaced_by)
