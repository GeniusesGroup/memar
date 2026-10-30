#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/management/task/labels/task_kind.py — the kinds of task, declared once.

A kind says what act a task is (the label kind `TaskKind` of a plan's `Labels`, `LABEL_KIND` below), so that the agent doing it has read, in its
own context, the sections of Memar's documents that govern that act. This file
declares the closed set of act words and nothing about what each reads: which
sections an act reads is the lists of the rule
[Normative References](../../../knowledge/content/rules/normative_references/normative_references.md),
one per kind, named `normative_references-<word>.md` after the word declared
here, and read by `modules-plugable/knowledge/documentation/services/normative_references.py`. It is code and not a
section of a document because programs read it — the kind a plan carries is
checked against it, the help of `memar task ensure` lists it, and a kind's
list is found by its word — and a closed set a program reads, written as prose,
is a copy no check keeps true ([A Fact in Code Is Written Once](../../../modules-plugable/knowledge/documentation/documentation.md#a-fact-in-code-is-written-once)).

Per kind it holds: the word; one sentence on when the kind applies, which says
when to choose it and does not restate what a Practice's own `description`
says of itself; and whether a plan may carry it. Two words are kinds of
context and not of task: `answer`, a question answered in the conversation,
which opens no task and so has no plan; and `plan`, the coordinating acts —
writing, queuing and handing over other tasks' plans, asking for a review —
which a coordinating task adds to the kind of its own task, whatever that
is. A plan carries neither.

Which agent runs a kind, and how able it must be, is not said here and is not
a fact of the kind: a plan's own AI is the Labels design's concern
(task 20261014T120306Z-20292-0), and until it lands the reader of these words
(`task_plan_labels`) cites the rule that says it (its constant `MODEL_RULE`).

This file moves whole to the `protocol/` folder of the `task` module once the
scripts are modules (study 20261015-T112819Z-23712, R7); the move of services
into modules is its own task (20261015-T123046Z-17544).
"""
from __future__ import annotations
from enum import Enum
from modules.knowledge.label.primitive.label import Label, LabelDefinition, LabelKind, LabelProblem

class TaskKind(Enum):
    """One kind, in the order a task usually meets them: (word, when it applies, whether a plan may carry it)."""
    ANSWER = ('answer', 'A question is answered in the conversation itself, which opens no task and so writes no plan.', False)
    PLAN = ('plan', 'A task coordinates other tasks — writes, queues or hands over their plans, or asks for a review of their work — and adds this to the kind of its own task, so no plan carries it.', False)
    DESIGN = ('design', 'The task decides what something is — a concept, an abstraction, a protocol, a language construct, a rule — or chooses between proposals for one, before anything is built from it.', True)
    CRITIQUE = ('critique', 'The task judges work it did not make against the documents that govern that work, and returns a verdict on each part.', True)
    IMPLEMENT = ('implement', 'The task builds or changes code, a test or a tool whose design is already settled, one checked step at a time.', True)
    DOCUMENT = ('document', 'The task writes or revises a document whose content is already settled.', True)
    MECHANICAL = ('mechanical', 'The task searches, counts, moves or rewrites by a rule given to it in full, and no step of it decides anything.', True)

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
    def words(cls, carried: bool=False) -> tuple[str, ...]:
        """Every kind's word in order; with CARRIED, only those a plan may carry."""
        return tuple((kind.word for kind in cls if kind.carried or not carried))
LABEL_KIND_NAME = 'TaskKind'
TASK_KIND_LABEL = Label(LABEL_KIND_NAME, '01a14a04-652e-7dc2-8926-f2b0b5b2ba1b')
_IDS = {'design': '01a14a04-6531-73d5-8eeb-6e37ddce016d', 'critique': '01a14a04-6532-76bf-b48e-4b7cc539bf44', 'implement': '01a14a04-6533-7efe-98ac-0e9e47dc1376', 'document': '01a14a04-6534-78ea-b510-9d2abcdcba79', 'mechanical': '01a14a04-6535-780b-bfa4-4a451f6e5d70'}

def _word(text: str) -> str:
    kind = TaskKind.read(text)
    if kind is None:
        raise LabelProblem(f"a kind is one of {', '.join(TaskKind.words(carried=True))}; {text.strip()!r} is not one")
    if not kind.carried:
        raise LabelProblem(f"a plan does not carry the kind {kind.word}: {kind.applies} A plan's kind is one of {', '.join(TaskKind.words(carried=True))}")
    return kind.word
LABEL_KIND = LabelKind(TASK_KIND_LABEL, 'what act the task is, one of the words above that a plan may carry', "`get-task-init-context`, which reads an act's sections, and `content get-act-context --kind`", _word, tuple((LabelDefinition(Label(word, _IDS[word]), (TASK_KIND_LABEL,)) for word in TaskKind.words(carried=True))))
