#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from machine.console import fail
from modules.knowledge.content.labels.Topic import Label_Topic
from modules.knowledge.label.primitive.label import Label, LabelDefinition, LabelKind, LabelProblem
TOPIC_LABEL = Label_Topic.as_label
LABEL_KIND_NAME = Label_Topic.title

class Topic(str):
    @classmethod
    def normalized(cls, text: str) -> Topic:
        return cls('-'.join(text.lower().split()))

    @classmethod
    def checked(cls, text: str) -> Topic:
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

LABEL_KIND = LabelKind(
    TOPIC_LABEL,
    'the subject a record is about; each subject is Label_<Word> taking Label_Topic',
    '`claims` and `labels`',
    _word,
)

def topic(word: str) -> LabelDefinition:
    raise LabelProblem(
        f"do not call topic(); declare class Label_<Word>(DeclaredLabel) with takes=(Label_Topic,) (refused for {word!r})"
    )
