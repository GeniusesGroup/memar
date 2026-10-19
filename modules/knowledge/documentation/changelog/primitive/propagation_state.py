#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/propagation_state.py — where a change's propagation to another artifact stands, declared once.

[Documentation — Changelog](../changelog.md) names these; they are code and are written here and
nowhere else ([A Fact in Code Is Written Once](../../documentation.md#a-fact-in-code-is-written-once)).
The specification keeps the reasons and how each is used.
"""
from __future__ import annotations

from modules.knowledge.documentation.primitive.word import Word


class PropagationState(Word):
    PENDING = ("Pending", "the open state: undone propagation work a future contributor should search for")
    DONE = ("Done", "closed: the propagation was carried out")
    REJECTED = ("Rejected", "closed: considered and deliberately not done, with the reason recorded")

    @property
    def open(self) -> bool:
        """Whether the propagation is still to do: only `Pending` is."""
        return self is PropagationState.PENDING
