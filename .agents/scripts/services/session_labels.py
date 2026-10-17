#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_topics.py — the topics a project's sessions carry, with how many.

Why a listing. A topic is free text (`session_plan`), so nothing but the sessions
themselves says which subjects are in use; whoever queues a task needs to see
them to reuse one rather than write the same subject a second way, and the owner
needs them to see what is waiting by subject. It is read from the plans, as
`list` is, and kept nowhere else.

A project is named as `list --project` names it: a name the registry resolves, or
a folder whose project is meant; the folder the command runs in is never read. Every session of the project is counted,
wherever its folder lies and whatever its status, with how many of them are
queued, since the queued ones are what `claims` batches by topic. The largest
first, then by name, so the order does not depend on the order folders were read.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail, note
from services.status import Status
from services.project_find import add_project_flags, project_from_args
from services.session_find import project_of

from services.session_topic import topics_in_use
from services.project_name import ProjectName

TOPICS_COMMAND = "topics"
PROJECT_REQUIRED = f"{TOPICS_COMMAND} needs {ProjectName.either_words()}: name the project whose topics to list"


def list_topics(project: str | None) -> None:
    """`topics`: print each topic of PROJECT's sessions with its counts, or say that none is in use; a missing or empty PROJECT is refused."""
    if project is None:
        fail(PROJECT_REQUIRED)
    found = topics_in_use(project_of(project))
    if not found:
        note("no topic in use in this project")
        return
    for topic, sessions in sorted(found.items(), key=lambda item: (-len(item[1]), item[0])):
        queued = sum(1 for session in sessions if session.status == Status.QUEUED.key)
        count = f"{len(sessions)} session" + ("" if len(sessions) == 1 else "s")
        print(f"{topic}  {count}, {queued} queued")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session topics`."""
    lister = verbs.add_parser(
        TOPICS_COMMAND,
        help="list the topics a project's sessions carry, with how many",
        description=(
            "List the topics the project's sessions carry, the most used first, each\n"
            "with how many sessions have it and how many of those are queued. Use it\n"
            "before queuing a task, to reuse a topic rather than write the same\n"
            f"subject another way. {ProjectName.either_words()} names the\n"
            "project; one is required, and the current folder is never read."
        ),
    )
    add_project_flags(lister, "the project whose topics to list", required=True)
    return run


def run(args: argparse.Namespace) -> None:
    list_topics(project_from_args(args))
