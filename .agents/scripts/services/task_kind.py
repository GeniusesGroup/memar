#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/task_kind.py — the kinds of task, declared once.

A kind says what act a task is, so that the agent doing it has read, in its
own context, the sections of Memar's documents that govern that act. This file
declares the closed set of act words and nothing about what each reads: which
sections an act reads is the lists of the rule
[Normative References](../rules/normative_references/normative_references.md),
one per kind, named `normative_references-<word>.md` after the word declared
here, and read by `services/normative_references.py`. It is code and not a
section of a document because programs read it — the kind a plan carries is
checked against it, the help of `memar session new` lists it, and a kind's
list is found by its word — and a closed set a program reads, written as prose,
is a copy no check keeps true ([A Fact in Code Is Written Once](../../../modules/content/documentation/documentation.md#a-fact-in-code-is-written-once)).

Per kind it holds: the word; one sentence on when the kind applies, which says
when to choose it and does not restate what a Practice's own `description`
says of itself; and whether a plan may carry it. Two words are kinds of
context and not of task: `answer`, a question answered in the conversation,
which opens no session and so has no plan; and `plan`, the coordinating acts —
writing, queuing and handing over other sessions' plans, asking for a review —
which a coordinating session adds to the kind of its own task, whatever that
is. A plan carries neither.

Which agent runs a kind, and how able it must be, is not said here and is not
a fact of the kind: a plan's own AI is the Labels design's concern
(session 20261014T120306Z-20292-0), and until it lands the reader of these words
(`session_plan_kind`) keeps the rule `start` applies, as a transitional rule
with its reason.

This file moves whole to the `protocol/` folder of the `task` module once the
scripts are modules (study 20261015-T112819Z-23712, R7); the move of services
into modules is its own session (20261015-T123046Z-17544).
"""
from __future__ import annotations

from enum import Enum


class TaskKind(Enum):
    """One kind, in the order a task usually meets them: (word, when it applies, whether a plan may carry it)."""

    ANSWER = (
        "answer",
        "A question is answered in the conversation itself, which opens no session and so writes no plan.",
        False,
    )
    PLAN = (
        "plan",
        "A session coordinates other sessions — writes, queues or hands over their plans, or asks for a review of their work — "
        "and adds this to the kind of its own task, so no plan carries it.",
        False,
    )
    DESIGN = (
        "design",
        "The task decides what something is — a concept, an abstraction, a protocol, a language construct, a rule — "
        "or chooses between proposals for one, before anything is built from it.",
        True,
    )
    CRITIQUE = (
        "critique",
        "The task judges work it did not make against the documents that govern that work, and returns a verdict on each part.",
        True,
    )
    IMPLEMENT = (
        "implement",
        "The task builds or changes code, a test or a tool whose design is already settled, one checked step at a time.",
        True,
    )
    DOCUMENT = (
        "document",
        "The task writes or revises a document whose content is already settled.",
        True,
    )
    MECHANICAL = (
        "mechanical",
        "The task searches, counts, moves or rewrites by a rule given to it in full, and no step of it decides anything.",
        True,
    )

    def __init__(self, word: str, applies: str, carried: bool) -> None:
        self.word = word
        self.applies = applies
        self.carried = carried

    @classmethod
    def read(cls, text: str) -> TaskKind | None:
        """The kind TEXT names, stripped and in any case; None for any other word."""
        wanted = text.strip().lower()
        return next((kind for kind in cls if kind.word == wanted), None)

    @classmethod
    def words(cls, carried: bool = False) -> tuple[str, ...]:
        """Every kind's word in order; with CARRIED, only those a plan may carry."""
        return tuple(kind.word for kind in cls if kind.carried or not carried)
