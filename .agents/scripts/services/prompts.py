#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/prompts.py — `memar prompts`: its help, which groups the verbs that print a prompt for an agent.

A prompt is its own kind of output (owner, 2026-10-16): a fixed text an agent
is handed, built from a session's id alone, with its own rule — the agent that
hands it over adds nothing to it, because whatever else a task needs is in the
session's plan. Kept under `session`, a prompt was mixed with the record of a
task; a group named for what it makes lets later prompts join it.

Each verb is named for what the prompt makes happen, not by one word, so a
reader of `memar prompts --help` knows which one to hand over without opening
any: `prompts_plan_brief` hands a session's plan to a sub-agent to carry out,
`prompts_questions_brief` hands a session's questions to an agent to answer, and
`prompts_answering` is what that agent runs first, writing nothing.

`memar session start` stays under `session`: its output is also read by an
agent first, but running it takes the session up — it is `new --session-id`, so
the report, the role folders and the log line are written — and an act on a
session's record belongs to `session`; every verb here writes nothing.

**Each help states its own work, and no sub-verb's** (owner, 2026-10-14): the
help below says what a prompt is, and each verb's command line and what it
prints are in that verb's own `--help`. The domain only groups its verbs:
nothing is owed before every one, so its `describe` returns no run.

Usage is the interface. Do not duplicate these recipes as prose catalogs.
"""
from __future__ import annotations

PROMPTS_COMMAND = "prompts"

SUMMARY = "print the fixed text an agent is handed: to carry out a session's plan, or to answer its questions"

DESCRIPTION = """memar prompts — the texts an agent is handed

A prompt is a fixed text, built from a session's id alone, that is handed to
an agent as it is printed, with nothing added: whatever else the agent needs is
in the session's plan, which the session handing it over writes first. Each
verb below prints one prompt, and is named for what the prompt makes happen.
None of them writes anything.

Each verb below says what it prints, and for whom, in its own --help.
"""


def describe(verbs) -> None:
    """`memar prompts`, which only groups its verbs, each declared by its own service: nothing is owed before every one."""
    verbs.add_parser(PROMPTS_COMMAND, help=SUMMARY, description=DESCRIPTION)
    return None
