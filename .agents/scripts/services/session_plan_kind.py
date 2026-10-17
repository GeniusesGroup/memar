#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan_kind.py — a plan's kind: reading and writing the `Kind` key, with the words `task_kind` declares.

The words are not declared here: `services/task_kind.py` holds them, with
whether a plan may carry each, and this file only reads them. What this file
adds is the rule `start` applies to say how able an agent a kind needs, which
is transitional (below).
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from services.session_plan import front_matter
from services.session_plan_rewrite import key_of, line_end, rewrite
from services.session_record import PlanKey
from services.task_kind import TaskKind


# The kinds a plan may carry.
KINDS = TaskKind.words(carried=True)
# Transitional, until the plan names its own AI model (the Labels design's
# AIModel, its core step 4, replaces `start`'s model part): every kind's work is
# judgment and runs on the strongest model the runtime offers, except
# `TaskKind.MECHANICAL`, which runs on a cheaper one. The reason: a kind does not
# say how hard its task is, and a judgment task run on a weaker model costs more
# in rework than the model saves (the Memar skill, section Session and plan), so
# only work that decides nothing is moved down. The kinds a plan may not carry
# are listed among the judgment ones, so a plan an earlier Memar wrote with one is
# not read as mechanical.
CHEAPER_KINDS = (TaskKind.MECHANICAL.word,)
STRONG_KINDS = tuple(word for word in TaskKind.words() if word not in CHEAPER_KINDS)


def checked_kind(text: str) -> str:
    """TEXT as a kind a plan may carry, lower case; refused when it is no kind, so a misspelt kind never reads as a cheaper one, or a kind no plan carries."""
    kind = TaskKind.read(text)
    if kind is None:
        fail(f"a kind is one of {', '.join(KINDS)}; {text!r} is not one")
    if not kind.carried:
        fail(f"a plan does not carry the kind {kind.word}: {kind.applies} A plan's kind is one of {', '.join(KINDS)}")
    return kind.word


def kind_of(front: dict[str, str] | None) -> str:
    """The kind FRONT matter gives its plan, lower case as written; empty when it has none. It is not checked: a plan is edited by hand."""
    return (front or {}).get(PlanKey.KIND.key, "").strip().lower()


def set_kind(path: Path, kind: str) -> None:
    """Write KIND as PATH's `kind`, replacing the key or adding it last in the front matter; every other line is kept."""
    kind = checked_kind(kind)

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip("\r\n") for line in lines])
        if not start:
            fail(f"{path} has no front matter, so its kind cannot be set")
        written = f"{PlanKey.KIND.written}: {kind}{line_end(lines[0])}"
        for index in range(1, start - 1):
            if key_of(lines[index]) == PlanKey.KIND.written:
                return [*lines[:index], written, *lines[index + 1:]]
        return [*lines[:start - 1], written, *lines[start - 1:]]

    rewrite(path, change)
