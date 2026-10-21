#!/usr/bin/env python3
# For license and copyright information please see the LEGAL file in the code repository

"""modules/knowledge/label/services/plan_labels.py — a plan's labels: the kinds a plan carries, the project's label registry, and writing one label in place.

A plan's `Labels` are the words that link it to other sessions outside the
structure of their ids (`modules/knowledge/documentation/primitive/label.py`),
each written with its identifier, `design(01a14a04-...)`. A label is defined
once and its definition takes labels: `design` takes `TaskKind`, a topic takes
`Topic`. The closed kinds (`TaskKind`, in `modules/knowledge/documentation/plan/labels/task_kind.py`) define their
words in code; the free kind (`Topic`, in `modules/knowledge/documentation/plan/labels/topic.py`) defines a word
when it is first used, and the project keeps that definition, with its
identifier, in `.agents/memar/labels.md`, tracked with the project, so every
clone reads one identifier for one label and a plain search for the identifier
finds every plan that took it. This file gathers the kinds a plan carries and
adds none of its own. A plan takes as many labels as it needs and none it does
not: a label is added only when another session is to be found by it.

The rule `start` applies to say how able an agent a kind needs is transitional,
with its reason below, until the plan names its own AI (the Labels design's
`AIModel`, its own field, not done here).

A label is written one line at a time, as a priority is, through
`session_plan_rewrite`: the block under the key is found, the label's line added
or removed, and every other line kept as written.
"""
from __future__ import annotations
from pathlib import Path
from machine.console import fail
from modules.knowledge.documentation.plan.primitive.plan_key import PlanKey
from modules.knowledge.documentation.primitive.label import FLAG_SEPARATOR, Label, LabelDefinition, LabelProblem, LabelRegistry, Labels
from modules.knowledge.documentation.plan.labels import task_kind, topic
from modules.knowledge.documentation.plan.labels.task_kind import TaskKind
from modules.knowledge.documentation.plan.services.plan import front_matter
from modules.knowledge.documentation.plan.services.rewrite import key_of, line_end, rewrite
KINDS = (task_kind.LABEL_KIND, topic.LABEL_KIND)
TASK_KIND = task_kind.LABEL_KIND_NAME
TOPIC = topic.LABEL_KIND_NAME
REGISTRY_FILE = Path('.agents') / 'memar' / 'labels.md'
REGISTRY_HEADER = "# Labels\nThe labels this project's records take that are free text (topics), each defined once, one line a label: `- word(identifier): kind(identifier)`. `memar label add` adds a line when a word is first used; the identifier is what a search finds every record that took the label by.\n\n"
TASK_KINDS = TaskKind.words(carried=True)
CHEAPER_KINDS = (TaskKind.MECHANICAL.word,)
STRONG_KINDS = tuple((word for word in TaskKind.words() if word not in CHEAPER_KINDS))
_cache: dict[tuple[str, float], LabelRegistry] = {}

def kinds_listing() -> str:
    """The kinds a plan carries as one line for a help text, e.g. `TaskKind, Topic`."""
    return ', '.join((kind.name for kind in KINDS))

def registry_for(project: Path | None) -> LabelRegistry:
    """The label registry of PROJECT: the kinds' own definitions and those its `.agents/memar/labels.md` keeps; the kinds alone without a project or a file."""
    file = project / REGISTRY_FILE if project else None
    if file is None or not file.is_file():
        return LabelRegistry(KINDS)
    stamp = (str(file), file.stat().st_mtime)
    if stamp not in _cache:
        _cache[stamp] = LabelRegistry(KINDS, LabelRegistry.parse(file.read_text(encoding='utf-8')))
    return _cache[stamp]

def project_of(front: dict[str, str] | None) -> Path | None:
    """The project FRONT matter names, or None."""
    named = (front or {}).get(PlanKey.PROJECT.key, '').strip()
    return Path(named) if named else None

def registry_of(front: dict[str, str] | None) -> LabelRegistry:
    """The registry of the project a plan's FRONT matter names."""
    return registry_for(project_of(front))

def labels_of(front: dict[str, str] | None) -> Labels:
    """The labels FRONT matter gives its plan, as written; none when it has none. They are not checked: a plan is edited by hand."""
    return Labels.read((front or {}).get(PlanKey.LABELS.key, ''))

def topics_of(front: dict[str, str] | None) -> tuple[str, ...]:
    """The words of the topics FRONT matter gives its plan, in the order written."""
    return registry_of(front).words(labels_of(front), TOPIC)

def task_kind_of(front: dict[str, str] | None) -> str:
    """The task kind FRONT matter gives its plan, lower case as written; empty when it has none.

    A plan with several task kinds is read as its first judgment kind, so that
    a task that is also mechanical is not moved to a cheaper model.
    """
    words = [word.strip().lower() for word in registry_of(front).words(labels_of(front), TASK_KIND)]
    return next((word for word in words if word in STRONG_KINDS), words[0] if words else '')

def checked_label(text: str, project: Path | None, registry: LabelRegistry | None=None) -> tuple[Label, LabelDefinition | None]:
    """TEXT, `KIND=WORD`, as a label of a kind a plan carries in PROJECT, and the definition it needs kept (None when defined already); refused with the kind's words when it is none."""
    try:
        return (registry or registry_for(project)).resolve(text)
    except LabelProblem as problem:
        fail(str(problem))

def keep_definition(project: Path, definition: LabelDefinition) -> None:
    """Append DEFINITION to PROJECT's label registry file, creating it with its header."""
    file = project / REGISTRY_FILE
    file.parent.mkdir(parents=True, exist_ok=True)
    text = file.read_text(encoding='utf-8') if file.is_file() else REGISTRY_HEADER
    if not text.endswith('\n'):
        text += '\n'
    file.write_text(text + definition.line() + '\n', encoding='utf-8', newline='\n')
    _cache.clear()

def _block(lines: list[str], start: int) -> tuple[int, int] | None:
    """Where the `Labels:` block lies among the front matter's LINES (before START): the header's index and the index after its last line; None without one."""
    for index in range(1, start - 1):
        if key_of(lines[index]) == PlanKey.LABELS.written and lines[index].split(':', 1)[1].strip() == '':
            end = index + 1
            while end < start - 1 and lines[end][:1] in (' ', '\t'):
                end += 1
            return (index, end)
    return None

def _written(labels: Labels, newline: str) -> list[str]:
    return [f'{PlanKey.LABELS.written}:{newline}', *(f'{line}{newline}' for line in labels.lines())] if labels else []

def _change(path: Path, edit) -> None:
    """Rewrite PATH's labels as EDIT makes them from the ones it holds; every other line is kept."""

    def change(lines: list[str]) -> list[str]:
        _, start = front_matter([line.rstrip('\r\n') for line in lines])
        if not start:
            fail(f'{path} has no front matter, so its labels cannot be set')
        newline = line_end(lines[0])
        found = _block(lines, start)
        was = Labels.read('\n'.join((line.strip() for line in lines[found[0] + 1:found[1]]))) if found else Labels()
        written = _written(edit(was), newline)
        if found:
            return [*lines[:found[0]], *written, *lines[found[1]:]]
        return [*lines[:start - 1], *written, *lines[start - 1:]]
    rewrite(path, change)

def add_label(path: Path, label: Label) -> None:
    """Add LABEL to PATH's labels, last; unchanged when the plan already carries it. LABEL has been checked (`checked_label`)."""
    _change(path, lambda was: was.with_label(label))

def remove_label(path: Path, label: Label) -> None:
    """Remove LABEL from PATH's labels, the block with the last one; unchanged when the plan does not carry it."""
    _change(path, lambda was: was.without(label))
