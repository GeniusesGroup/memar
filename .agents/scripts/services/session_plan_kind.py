#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_plan_kind.py — a plan's kind: what the task is, which says how strong a model it needs.
"""
from __future__ import annotations

from pathlib import Path

from machine.console import fail
from services.session_plan import front_matter
from services.session_plan_rewrite import key_of, line_end, rewrite
from services.session_record import PlanKey


# What kind of task a plan holds, which says how strong a model it needs: the
# kinds whose work is judgment run on the strongest model the runtime offers
# (the Memar skill, section Session and plan), the others on a cheaper one.
STRONG_KINDS = ("ideation", "plan", "modeling", "design", "critique")
CHEAPER_KINDS = ("mechanical",)
KINDS = (*STRONG_KINDS, *CHEAPER_KINDS)


def checked_kind(text: str) -> str:
    """TEXT as a kind, lower case; refused when it is not one of `KINDS`, so a misspelt kind never reads as a cheaper one."""
    kind = text.strip().lower()
    if kind not in KINDS:
        fail(f"a kind is one of {', '.join(KINDS)}; {text!r} is not one")
    return kind


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
