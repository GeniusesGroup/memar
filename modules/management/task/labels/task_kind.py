#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository
from __future__ import annotations
from modules.knowledge.label.primitive.label import Label, LabelDefinition, LabelKind, LabelProblem
from modules.management.task.labels.answer import Answer
from modules.management.task.labels.critique import Critique
from modules.management.task.labels.design import Design
from modules.management.task.labels.document import Document
from modules.management.task.labels.implement import Implement
from modules.management.task.labels.mechanical import Mechanical
from modules.management.task.labels.plan_kind import PlanKind
LABEL_KIND_NAME = 'TaskKind'
TASK_KIND_LABEL = Label(LABEL_KIND_NAME, '01a14a04-652e-7dc2-8926-f2b0b5b2ba1b')

class TaskKind:
    ANSWER = Answer
    PLAN = PlanKind
    DESIGN = Design
    CRITIQUE = Critique
    IMPLEMENT = Implement
    DOCUMENT = Document
    MECHANICAL = Mechanical

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return (cls.ANSWER, cls.PLAN, cls.DESIGN, cls.CRITIQUE, cls.IMPLEMENT, cls.DOCUMENT, cls.MECHANICAL)

    @classmethod
    def read(cls, text: str):
        wanted = text.strip().lower()
        return next((kind for kind in cls.all() if kind.word == wanted), None)

    @classmethod
    def words(cls, carried: bool=False) -> tuple[str, ...]:
        return tuple(kind.word for kind in cls.all() if kind.carried or not carried)

def _word(text: str) -> str:
    kind = TaskKind.read(text)
    if kind is None:
        raise LabelProblem(f"a kind is one of {', '.join(TaskKind.words(carried=True))}; {text.strip()!r} is not one")
    if not kind.carried:
        raise LabelProblem(f"a plan does not carry the kind {kind.word}: {kind.meaning} A plan's kind is one of {', '.join(TaskKind.words(carried=True))}")
    return kind.word

LABEL_KIND = LabelKind(
    TASK_KIND_LABEL,
    'what act the task is, one of the words above that a plan may carry',
    "`get-task-init-context`, which reads an act's sections, and `content get-act-context --kind`",
    _word,
    tuple(
        LabelDefinition(Label(kind.word, kind.id), (TASK_KIND_LABEL,))
        for kind in TaskKind.all()
        if kind.carried
    ),
)
