#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.LabelKind import Label_LabelKind

class Label_DocumentKind(DeclaredLabel):
    id = '01a14a04-6539-7a01-8a01-000000000001'
    labels = (Label_LabelKind,)
    SEQUENCE: tuple[str, ...] = ('Explanation', 'Plan', 'Report', 'Handoff', 'Research')

    @classmethod
    def DevActionNote(cls) -> str:
        return (
            'Declare each document-kind word as Label_<Word>(DeclaredLabel) with labels=(Label_DocumentKind,). '
            'Declare statuses() as the Status-kind types that kind may take. Ask members() on this type.'
        )

    @classmethod
    def members(cls) -> tuple[type, ...]:
        DeclaredLabel.ensure_under('modules-plugable.knowledge.documentation')
        held = {member.__name__[len('Label_'):]: member for member in DeclaredLabel.having(cls)}
        listed = tuple(held[name] for name in cls.SEQUENCE if name in held)
        return listed + tuple(member for name, member in held.items() if name not in cls.SEQUENCE)

    @classmethod
    def read(cls, text: str):
        return DeclaredLabel.read_among(cls.members(), text)

    @classmethod
    def keys(cls) -> tuple[str, ...]:
        return DeclaredLabel.keys_of(cls.members())

    @classmethod
    def listing(cls) -> str:
        return DeclaredLabel.listing_of(cls.members())

    @classmethod
    def Overview(cls) -> str:
        return (
            'A label other labels take when they name what kind of documentation record a word is '
            '(Plan, Report, Explanation, Handoff, Research).'
        )
