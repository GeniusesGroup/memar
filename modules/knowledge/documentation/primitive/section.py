#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/section.py — a named section of a documentation record, declared once.

A facet's specification names the sections its documents carry; the names are a
closed or an open catalog, so each is code and is written once, in a facet's own
`primitive/` as a subclass of `Section`
([A Fact in Code Is Written Once](../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reason a section exists and how it is used; the type
holds its heading and what it is for, and a help text or a check asks it.
"""
from __future__ import annotations

from enum import Enum


class Section(Enum):
    """A section: the heading as written, and what it is for."""

    def __init__(self, heading: str, purpose: str) -> None:
        self.heading = heading
        self.purpose = purpose

    @classmethod
    def headings(cls) -> tuple[str, ...]:
        """Every heading, in the order declared."""
        return tuple(member.heading for member in cls)

    @classmethod
    def read(cls, text: str):
        """The section TEXT names, stripped and in any case; None for any other heading."""
        wanted = text.strip().lower()
        return next((member for member in cls if member.heading.lower() == wanted), None)
