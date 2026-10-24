#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""primitive/word.py — a word of a closed vocabulary of a documentation record, declared once.

A facet's specification fixes some vocabularies (the confidence a decision
carries, the state of a propagation); each is a closed set a program may read,
so each is code, written once in a facet's own `primitive/` as a subclass of
`Word` ([A Fact in Code Is Written Once](../../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).
The specification keeps why the vocabulary is fixed; the type holds the words
and what each means.
"""
from __future__ import annotations
from enum import Enum

class Word(Enum):
    """A word as written, and what it means."""

    def __init__(self, word: str, meaning: str) -> None:
        self.word = word
        self.meaning = meaning

    @classmethod
    def words(cls) -> tuple[str, ...]:
        """Every word, in the order declared."""
        return tuple((member.word for member in cls))

    @classmethod
    def read(cls, text: str):
        """The word TEXT names, stripped and in any case; None for any other."""
        wanted = text.strip().lower()
        return next((member for member in cls if member.word.lower() == wanted), None)

    @classmethod
    def listing(cls) -> str:
        """The words as a sentence: `Pending, Done, or Rejected`."""
        words = cls.words()
        return f"{', '.join(words[:-1])}, or {words[-1]}" if len(words) > 1 else words[0]
