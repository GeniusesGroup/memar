#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.declared_label import DeclaredLabel
from modules.knowledge.label.labels.LabelKind import Label_LabelKind

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
    labels = (Label_LabelKind,)

    @classmethod
    def Overview(cls) -> str:
        return cls.meaning

    @classmethod
    def DevActionNote(cls) -> str:
        return (
            'Declare each Status-kind word as Label_<Word>(DeclaredLabel) with labels=(Label_Status,). '
            'Document kinds declare which Status words apply via statuses(). '
            'Ask members() / for_document() / read() on this type.'
        )

    @classmethod
    def members(cls) -> tuple[type, ...]:
        """Document-life Status words under thing (ordered); domain Status words stay out until imported for their own queries."""
        DeclaredLabel.ensure_under('modules.identity.thing.labels')
        found = [
            member for member in DeclaredLabel.having(cls)
            if getattr(member, 'order', None) is not None
        ]
        return tuple(sorted(found, key=lambda member: member.order))

    @classmethod
    def for_document(cls, document_kind) -> tuple[type, ...]:
        """Status words the document kind declares via statuses(); a word looks up an imported kind."""
        if isinstance(document_kind, str):
            wanted = document_kind.strip().lower()
            document_kind = next(
                (
                    member for member in DeclaredLabel.all_declared()
                    if getattr(member, 'word', '').lower() == wanted and hasattr(member, 'statuses')
                ),
                None,
            )
            if document_kind is None:
                return ()
        statuses = getattr(document_kind, 'statuses', None)
        if statuses is None:
            return ()
        held = statuses() if callable(statuses) else statuses
        return tuple(held)

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
