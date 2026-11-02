#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from importlib import import_module
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_DocumentKind(DeclaredLabel):
    word = 'DocumentKind'
    id = '01a14a04-6539-7a01-8a01-000000000001'
    meaning = (
        'A label other labels take when they name what kind of documentation record a word is '
        '(Plan, Report, Explanation, Handoff, Research).'
    )
    order = 1
    labels = ('LabelKind',)

    @classmethod
    def DevActionNote(cls) -> str:
        return (
            'Declare each document-kind word as Label_<Word>(DeclaredLabel) with takes=(Label_DocumentKind,). '
            'Ask members() on this type.'
        )

    @classmethod
    def _ensure_members(cls) -> None:
        if getattr(cls, '_members_loaded', False):
            return
        import_module('modules-plugable.knowledge.documentation.explanation.labels.Label_Explanation')
        import_module('modules-plugable.knowledge.documentation.plan.labels.Label_Plan')
        import_module('modules-plugable.knowledge.documentation.report.labels.Label_Report')
        import_module('modules-plugable.knowledge.documentation.handoff.labels.Label_Handoff')
        import_module('modules-plugable.knowledge.documentation.research.labels.Label_Research')
        cls._members_loaded = True

    @classmethod
    def members(cls) -> tuple[type, ...]:
        cls._ensure_members()
        return DeclaredLabel.taking(cls)

    @classmethod
    def read(cls, text: str):
        return DeclaredLabel.read_among(cls.members(), text)

    @classmethod
    def keys(cls) -> tuple[str, ...]:
        return DeclaredLabel.keys_of(cls.members())

    @classmethod
    def listing(cls) -> str:
        return DeclaredLabel.listing_of(cls.members())
