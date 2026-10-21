#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/label.py — a session's label added or removed, and what is said when a topic nearly matches another.

Why a verb of its own, as `priority` is. What a task is about is known when it
is queued, but is also seen later: the owner reads the labels in use
(`session_labels`) and finds one subject written two ways, or a task filed
under too wide a subject. Anyone may re-label it, so it is a verb, not a hand
edit that would be one more place the block could be written two ways. What a
label is, and how a plan carries it, is `session_plan_labels`'s; this file finds
the session, says what changed, and says when a new topic is close to one
already in use.

Why a warning and not a refusal. Topics are free text so that a new subject is
never stopped; the cost is that a typo makes a second topic for one subject, and
`claims` then batches the two apart. A topic one or two edits from another one
the project uses is probably that typo, so it is named with the one it
resembles and written anyway: refusing would stop a subject that really is
different (`docs` and `doc-tests`), and the person can always re-label. Only the
project's own topics are compared, and only topics: a word of another kind is
not a topic.

A label is added only when another session is to be found by it, and a plan
takes as many as it needs. Any status is accepted, as a priority is: a session
open or blocked now may be queued later.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Callable
from machine.console import fail, note
from machine.modules_import import load as modules_load
_task_list = modules_load('management', 'task', 'services', 'list')
_task_folder = modules_load('management', 'task', 'services', 'folder')
find_sessions = _task_list.find_sessions
Session = _task_folder.Session
folder_of = _task_folder.folder_of
is_task_folder = _task_folder.is_task_folder
from modules.knowledge.documentation.plan.services.plan import PLAN_NAME, read_plan
from modules.knowledge.label.services.plan_labels import TOPIC, add_label, checked_label, keep_definition, kinds_listing, labels_of, project_of, remove_label, topics_of
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
LABEL_COMMAND = 'add'
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

def topics_in_use(project: Path, *, leaving: str | None=None) -> dict[str, list[Session]]:
    """The topics PROJECT's sessions carry, each with its sessions; LEAVING is a session id left out of the count."""
    found: dict[str, list[Session]] = {}
    for session in find_sessions(project=project):
        if session.id == leaving:
            continue
        for topic in dict.fromkeys(topics_of(session.front)):
            found.setdefault(topic, []).append(session)
    return found

def near_topics(topic: str, project: Path, *, leaving: str | None=None) -> list[str]:
    """The topics in use in PROJECT within `NEAR_EDITS` of TOPIC; none when TOPIC is itself in use or empty."""
    if not topic:
        return []
    in_use = topics_in_use(project, leaving=leaving)
    if topic in in_use:
        return []
    return sorted((other for other in in_use if edit_distance(topic, other) <= NEAR_EDITS))

def warn_near(topic: str, project: Path, task_id: str) -> None:
    """Say, for each topic of PROJECT close to TOPIC, that it is near it and how to re-label; the topic is written all the same."""
    for other in near_topics(topic, project, leaving=task_id):
        note(f'warning: topic {topic} is near {other}, which is in use in this project; if they are one subject, re-label with `memar label {LABEL_COMMAND} {task_id} {TOPIC}={other}` and `--remove {TOPIC}={topic}`')

def carried(task_id: str, plan: Path) -> str:
    """What the plan at PLAN carries, one line: `labels: docs, design`, or `labels: (none)`."""
    labels = labels_of(read_plan(plan).front)
    return f'{task_id}  labels: ' + (', '.join((label.word for label in labels)) or '(none)')

def set_session_label(task_id: str, text: str, remove: bool) -> None:
    """`label`: add the label TEXT (`KIND=WORD`) to TASK_ID's plan, or with REMOVE take it out, and say what the plan carries now."""
    folder = folder_of(task_id)
    plan = folder / PLAN_NAME
    if not is_task_folder(folder) or not plan.is_file():
        fail(f"no session {task_id} with a {PLAN_NAME}, so there is no label to {('remove' if remove else 'add')}")
    front = read_plan(plan).front
    project = project_of(front)
    label, fresh = checked_label(text, project)
    has = any((item.id == label.id for item in labels_of(front)))
    if remove:
        remove_label(plan, label)
        print(f'{task_id}  removed {label.word}' if has else f'{task_id}  does not carry {label.word}')
    else:
        if fresh is not None and project is not None:
            keep_definition(project, fresh)
        add_label(plan, label)
        print(f'{task_id}  added {label.word}' if not has else f'{task_id}  already carries {label.word}')
    print(carried(task_id, plan))
    if not remove and (not has) and (text.partition('=')[0].strip() == TOPIC) and project:
        warn_near(label.word, project, task_id)

def describe(verbs) -> Callable[[argparse.Namespace], None]:
    """`memar label add`."""
    tagger = verbs.add_parser(LABEL_COMMAND, help='add a label to a session, or remove one', description=f"Add the label KIND=WORD to the session ID's plan, or with --remove take\nit out. A label links the session to others outside the structure of\ntheir ids: Topic=T is the subject the task is about, so that `claims`\nhands one agent the queued tasks of one topic; TaskKind=K is the act the\ntask is. The kinds are {kinds_listing()}. A topic is free text,\nwritten in lower case with spaces as hyphens; one within one or two\nedits of a topic the project already uses is warned about and written\nall the same; `memar label list` lists the labels in use: run it\nfirst, to reuse a topic rather than write the same subject another way.\nA plan takes as many labels as it needs and none it does not: add one\nonly when another session is to be found by it. Labels are not copied\nfrom a session's parent. Anyone may change them, whatever the session's\nstatus.")
    tagger.add_argument('task_id', metavar='ID', help='the session to label')
    tagger.add_argument('label', metavar='KIND=WORD', help='the label to add, e.g. Topic=memar-scripts')
    tagger.add_argument('--remove', action='store_true', help='take the label out instead of adding it')
    return run

def run(args: argparse.Namespace) -> None:
    set_session_label(args.task_id, args.label, args.remove)
