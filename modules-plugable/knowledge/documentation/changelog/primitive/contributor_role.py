#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/contributor_role.py — role tags of a changelog entry's Contributors bullet that code or the documents name; the vocabulary is open, so another tag is written freely, declared once.

[Documentation — Changelog](../changelog.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.word import Word


class ContributorRole(Word):
    CLAIMED = ("claimed", "took the task")
    ARGUED = ("argued", "argued a position")
    REVIEWED = ("reviewed", "reviewed the work")
    REWROTE = ("rewrote", "rewrote existing text")
    TESTED = ("tested", "tested the work")
    REQUESTED = ("requested", "asked for the work")
    APPROVED = ("approved", "judged the entry correct, and did not do the work it judged")
