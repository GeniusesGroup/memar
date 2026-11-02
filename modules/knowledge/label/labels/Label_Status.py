#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel

class Label_Status(DeclaredLabel):
    word = 'Status'
    id = '01a14a04-6522-7d19-9796-04f8a30e831f'
    meaning = (
        'A label other labels take when they name where a record stands in its life. '
        'A Status-kind label may carry a rule; when it attaches, work may start. '
        'Attachment is only the Label edge on any record — including content. '
        'Status is not a separate domain vocabulary tree. '
        'General Status-kind words live under modules/identity/thing/labels as Label_<Word>; '
        'domain-specific Status-kind words stay in that domain\'s labels/.'
    )
    order = 1
    labels = ('LabelKind',)

    @classmethod
    def Overview(cls) -> str:
        return cls.meaning

    @classmethod
    def DevActionNote(cls) -> str:
        return (
            'Declare each Status-kind word as Label_<Word>(DeclaredLabel) with takes=(Label_Status,). '
            'Ask members() / for_document() / read() on this type; do not keep a parallel Status bag or status/ tree.'
        )

    @classmethod
    def _ensure_members(cls) -> None:
        if getattr(cls, '_members_loaded', False):
            return
        from modules.identity.thing.labels.Label_Active import Label_Active
        from modules.identity.thing.labels.Label_Blocked import Label_Blocked
        from modules.identity.thing.labels.Label_Complete import Label_Complete
        from modules.identity.thing.labels.Label_Draft import Label_Draft
        from modules.identity.thing.labels.Label_Final import Label_Final
        from modules.identity.thing.labels.Label_Paused import Label_Paused
        from modules.identity.thing.labels.Label_Proposed import Label_Proposed
        from modules.identity.thing.labels.Label_Queued import Label_Queued
        from modules.identity.thing.labels.Label_Rejected import Label_Rejected
        from modules.identity.thing.labels.Label_Superseded import Label_Superseded
        from modules.identity.thing.labels.Label_Withdrawn import Label_Withdrawn
        cls._members_loaded = True

    @classmethod
    def members(cls) -> tuple[type, ...]:
        """Document-life Status-kind Label_* that take this label (imported; ordered by `order`).

        Only members that declare `kinds` (which document kinds they apply to) are
        returned. Other Label_* that still `takes=(Label_Status,)` without `kinds`
        are not document-life Status words and stay out of this closed set.
        """
        cls._ensure_members()
        found = [
            member for member in DeclaredLabel.taking(cls)
            if getattr(member, 'kinds', ())
        ]
        return tuple(sorted(found, key=lambda member: getattr(member, 'order', 10**9)))

    @classmethod
    def for_document(cls, document_kind) -> tuple[type, ...]:
        """Members whose `kinds` lists DOCUMENT_KIND (a type with `.word`, or a word)."""
        word = document_kind if isinstance(document_kind, str) else document_kind.word
        return tuple(member for member in cls.members() if word in member.kinds)

    @classmethod
    def read(cls, text: str):
        return DeclaredLabel.read_among(cls.members(), text)

    @classmethod
    def keys(cls, document_kind=None) -> tuple[str, ...]:
        pool = cls.for_document(document_kind) if document_kind is not None else cls.members()
        return DeclaredLabel.keys_of(pool)

    @classmethod
    def listing(cls, document_kind=None) -> str:
        pool = cls.for_document(document_kind) if document_kind is not None else cls.members()
        return DeclaredLabel.listing_of(pool)

    @classmethod
    def definitions(cls):
        return DeclaredLabel.definitions_of(cls.members())
