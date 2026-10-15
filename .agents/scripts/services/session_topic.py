#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""services/session_topic.py — a session's topic set or removed, and what is said when it nearly matches another.

Why a verb of its own, as `priority` is. The subject of a queued task is known
when it is queued, but is also seen later: the owner reads the topics in use
(`session_topics`) and finds one subject written two ways, or a task filed
under too wide a subject. Anyone may re-tag it, so it is a verb, not a hand
edit that would be one more place the key could be written two ways. What a
topic is and how it is written into the plan is `session_plan`'s; this file
finds the session, says what changed, and says when the new topic is close to
one already in use.

Why a warning and not a refusal. Topics are free text so that a new subject is
never stopped; the cost is that a typo makes a second topic for one subject, and
`claims` then batches the two apart. A topic one or two edits from another one
the project uses is probably that typo, so it is named with the one it
resembles and written anyway: refusing would stop a subject that really is
different (`docs` and `doc-tests`), and the person can always re-tag. Only the
project's own topics are compared, and not the session's own old one.

An empty topic removes it. Any status is accepted, as a priority is: a session
open or blocked now may be queued later.
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from machine.console import fail, note
from services.session_find import find_sessions
from services.session_folder import Session, folder_of, is_session_folder
from services.session_plan import PLAN_NAME, read_plan
from services.session_plan_topic import checked_topic, set_topic, topic_of

TOPIC_COMMAND = "topic"
# A topic this many edits or fewer from another in use is taken for the same subject mistyped.
NEAR_EDITS = 2


def edit_distance(one: str, two: str) -> int:
    """How many single-character insertions, deletions, or substitutions turn ONE into TWO."""
    previous = list(range(len(two) + 1))
    for row, first in enumerate(one, 1):
        current = [row]
        for column, second in enumerate(two, 1):
            current.append(min(previous[column] + 1, current[column - 1] + 1, previous[column - 1] + (first != second)))
        previous = current
    return previous[-1]


def topics_in_use(project: Path, *, leaving: str | None = None) -> dict[str, list[Session]]:
    """The topics PROJECT's sessions carry, each with its sessions; LEAVING is a session id left out of the count."""
    found: dict[str, list[Session]] = {}
    for session in find_sessions(project=project):
        topic = topic_of(session.front)
        if topic and session.id != leaving:
            found.setdefault(topic, []).append(session)
    return found


def near_topics(topic: str, project: Path, *, leaving: str | None = None) -> list[str]:
    """The topics in use in PROJECT within `NEAR_EDITS` of TOPIC; none when TOPIC is itself in use or empty."""
    if not topic:
        return []
    in_use = topics_in_use(project, leaving=leaving)
    if topic in in_use:
        return []
    return sorted(other for other in in_use if edit_distance(topic, other) <= NEAR_EDITS)


def warn_near(topic: str, project: Path, session_id: str) -> None:
    """Say, for each topic of PROJECT close to TOPIC, that it is near it and how to re-tag; the topic is written all the same."""
    for other in near_topics(topic, project, leaving=session_id):
        note(
            f"warning: topic {topic} is near {other}, which is in use in this project; "
            f"if they are one subject, re-tag with `memar session topic {session_id} {other}`"
        )


def set_session_topic(session_id: str, value: str) -> None:
    """`topic`: write VALUE as SESSION_ID's topic (empty removes it), and say what it was."""
    topic = checked_topic(value)
    folder = folder_of(session_id)
    plan = folder / PLAN_NAME
    if not is_session_folder(folder) or not plan.is_file():
        fail(f"no session {session_id} with a {PLAN_NAME}, so there is no topic to set")
    front = read_plan(plan).front
    was = topic_of(front) or "(none)"
    set_topic(plan, topic)
    print(f"{session_id}  topic {topic or '(none)'}, was {was}")
    project = (front or {}).get("project", "").strip()
    if topic and project:
        warn_near(topic, Path(project), session_id)


def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar session topic`."""
    tagger = verbs.add_parser(
        TOPIC_COMMAND,
        help="set what a session is about, or remove it: the subject `claims` batches by",
        description=(
            "Set the session ID's topic to T: the one subject the task is about, so\n"
            "that `claims` hands one agent the queued tasks of one subject. A topic is\n"
            "a subject one context can hold, narrower than a project. It is free\n"
            "text, written in lower case with spaces as hyphens; an empty T removes\n"
            "it. A topic within one or two edits of one the project already uses is\n"
            "warned about and written all the same; `memar session topics` lists the\n"
            "topics in use: run it first, to reuse a topic rather than write the same\n"
            "subject another way. A topic is not copied from a session's parent. Give\n"
            "each queued task one, here or with `new --topic`: tasks that share a\n"
            "topic are taken together, and a task with no topic is taken by priority\n"
            "and age alone. Anyone, a person or an agent, may change it, whatever the\n"
            "session's status."
        ),
    )
    tagger.add_argument("session_id", metavar="ID", help="the session to tag")
    tagger.add_argument("topic", metavar="T", help="the subject, or an empty string to remove it")
    return run


def run(args: argparse.Namespace) -> None:
    set_session_topic(args.session_id, args.topic)
