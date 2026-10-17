#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/process/session/services/labels.py — the labels a project's sessions carry, by kind, with how many.

Why a listing. A topic is free text (`modules/knowledge/documentation/plan/primitive/topic.py`), so nothing but the
sessions themselves says which subjects are in use; whoever queues a task needs
to see them to reuse one rather than write the same subject a second way, and
the owner needs them to see what is waiting by subject. It is read from the
plans, as `list` is, and kept nowhere else.

A project is named as `list --project` names it: a name the registry resolves, or
a folder whose project is meant; the folder the command runs in is never read. Every session of the project is counted,
wherever its folder lies and whatever its status, with how many of them are
queued, since the queued ones are what `claims` batches by topic. The largest
first, then by kind and word, so the order does not depend on the order folders were read.
"""
from __future__ import annotations

import argparse
from typing import Callable

from machine.console import fail, note
from modules.knowledge.documentation.primitive.status import Status
from modules.process.project.services.find import add_project_flags, project_from_args
from modules.process.session.services.find import find_sessions, project_of
from modules.process.session.services.folder import Session
from modules.process.session.services.plan_labels import labels_of
from modules.process.project.primitive.project_name import ProjectName

LABELS_COMMAND = "labels"
PROJECT_REQUIRED = f"{LABELS_COMMAND} needs {ProjectName.either_words()}: name the project whose labels to list"


def labels_in_use(project) -> dict[str, list[Session]]:
    """The labels PROJECT's sessions carry, each written `Kind: word`, with its sessions."""
    found: dict[str, list[Session]] = {}
    for session in find_sessions(project=project):
        for label in dict.fromkeys(labels_of(session.front)):
            found.setdefault(str(label), []).append(session)
    return found


def list_labels(project: str | None) -> None:
    """`labels`: print each label of PROJECT's sessions with its counts, or say that none is in use; a missing or empty PROJECT is refused."""
    if project is None:
        fail(PROJECT_REQUIRED)
    found = labels_in_use(project_of(project))
    if not found:
        note("no label in use in this project")
        return
    for label, sessions in sorted(found.items(), key=lambda item: (-len(item[1]), item[0])):
        queued = sum(1 for session in sessions if session.status == Status.QUEUED.key)
        count = f"{len(sessions)} session" + ("" if len(sessions) == 1 else "s")
        print(f"{label}  {count}, {queued} queued")


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session labels`."""
    lister = verbs.add_parser(
        LABELS_COMMAND,
        help="list the labels a project's sessions carry, with how many",
        description=(
            "List the labels the project's sessions carry, each written Kind: word,\n"
            "the most used first, each with how many sessions have it and how many of\n"
            "those are queued. Use it before queuing a task, to reuse a topic rather\n"
            f"than write the same subject another way. {ProjectName.either_words()} names the\n"
            "project; one is required, and the current folder is never read."
        ),
    )
    add_project_flags(lister, "the project whose labels to list", required=True)
    return run


def run(args: argparse.Namespace) -> None:
    list_labels(project_from_args(args))
